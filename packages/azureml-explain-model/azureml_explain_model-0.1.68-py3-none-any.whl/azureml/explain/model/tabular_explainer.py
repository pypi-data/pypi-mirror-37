# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Defines the tabular explainer for getting model explanations from tabular data."""

import numpy as np
import pandas as pd
import scipy as sp
import shap

from .common import module_logger, _sort_features
from .base_explainer import BaseExplainer


def summarize_data(X, k, to_round_values=True):
    """Summarize a dataset.
    For dense dataset, use k mean samples weighted by the number of data points they
    each represent.
    For sparse dataset, use a sparse row for the background with calculated
    median for dense columns.

    :param X: Matrix of data samples to summarize (# samples x # features).
    :type X: numpy.array or pandas.DataFrame or scipy.sparse.csr_matrix
    :param k: Number of cluster centroids to use for approximation.
    :type k: int
    :param to_round_values: When using kmeans, for each element of every cluster centroid to match the nearest value
        from X in the corresponding dimension. This ensures discrete features
        always get a valid value.  Ignored for sparse data sample.
    :type to_round_values: bool
    :return: DenseData or SparseData object.
    :rtype: iml.datatypes.DenseData or iml.datatypes.SparseData
    """
    from shap.common import DenseData
    is_sparse = sp.sparse.issparse(X)
    if not isinstance(X, DenseData):
        if is_sparse:
            # instead of using kmeans, pass in background of zeros
            # for dense columns, calculate median of data
            # TODO: calculate median of data here
            return sp.sparse.csr_matrix((1, X.shape[1]), dtype=X.dtype)
        elif len(X) > 10 * k:
            # use kmeans to summarize the examples for initialization
            # if there are more than 10 x k of them
            return shap.kmeans(X, k, to_round_values)
    return X


class TabularExplainer(BaseExplainer):
    """Explain a model trained on a tabular dataset."""
    def __init__(self, workspace=None, experiment_name=None, run_id=None):
        """Initializes the Tabular Explainer.
        If workspace and experiment_name are provided, a new Run will be created and the model
        explanation data will be stored and managed by Run History service. The explanation
        data will be associated with this new Run and can be retrieved at a later time,
        for example, through its ID. If workspace, experiment_name and run_id are all provided,
        the explanation data will be associated with the Run that has the same Run ID.
        Otherwise, the data are only available locally.

        :param workspace: An object that represents a workspace.
        :type workspace: azureml.core.workspace.Workspace
        :param experiment_name: The name of an experiment.
        :type experiment_name: str
        :param run_id: A GUID that represents a run.
        :type run_id: str
        """
        BaseExplainer.__init__(self, workspace, experiment_name, run_id)
        self.neighbors = None
        self.scaler = None
        self.nn_shap_values = None

    def _reduce_eval_examples(self, evaluation_examples, max_dim_clustering=50):
        """Reduces the dimensionality of the evaluation examples if dimensionality is higher
        than max_dim_clustering.  If the dataset is sparse, we mean-scale the data and then run
        truncated SVD to reduce the number of features to max_dim_clustering.  For dense
        dataset, we also scale the data and then run PCA to reduce the number of features to
        max_dim_clustering.
        This is used to get better clustering results in _find_k.
        """
        from sklearn.decomposition import TruncatedSVD, PCA
        from sklearn.preprocessing import StandardScaler
        num_cols = evaluation_examples.shape[1]
        # Run PCA or SVD on input data and reduce to about 50 features prior to clustering
        components = min(max_dim_clustering, num_cols)
        reduced_eval_examples = evaluation_examples
        if components != num_cols:
            if sp.sparse.issparse(evaluation_examples):
                normalized_eval_examples = StandardScaler(with_mean=False).fit_transform(evaluation_examples)
                reducer = TruncatedSVD(n_components=components)
            else:
                normalized_eval_examples = StandardScaler().fit_transform(evaluation_examples)
                reducer = PCA(n_components=components)
            module_logger.info("reducing dimensionality to " + str(components) + " components for clustering")
            reduced_eval_examples = reducer.fit_transform(normalized_eval_examples)
        return reduced_eval_examples

    def _find_k_kmeans(self, evaluation_examples, max_dim_clustering=50):
        """Uses k-means to downsample the evaluation examples.
        Starting from k_upper_bound, cuts k in half each time and run k-means
        clustering on the evaluation_examples.  After each run, computes the
        silhouette score and stores k with highest silhouette score.
        We use optimal k to determine how much to downsample the evaluation_examples.
        """
        from sklearn.cluster import KMeans
        from sklearn.metrics import silhouette_score
        from math import log, isnan, ceil
        reduced_eval_examples = self._reduce_eval_examples(evaluation_examples, max_dim_clustering)
        num_rows = evaluation_examples.shape[0]
        k_upper_bound = 2000
        k_list = []
        k = min(num_rows / 2, k_upper_bound)
        for i in range(int(ceil(log(num_rows, 2) - 7))):
            k_list.append(int(k))
            k /= 2
        prev_highest_score = -1
        prev_highest_index = 0
        opt_k = int(k)
        for k_index, k in enumerate(k_list):
            module_logger.info("running KMeans with k: " + str(k))
            km = KMeans(n_clusters=k).fit(reduced_eval_examples)
            clusters = km.labels_
            num_clusters = len(set(clusters))
            k_too_big = num_clusters <= 1
            if k_too_big or num_clusters == reduced_eval_examples.shape[0]:
                score = -1
            else:
                score = silhouette_score(reduced_eval_examples, clusters)
            if isnan(score):
                score = -1
            module_logger.info("KMeans silhouette score: " + str(score))
            # Find k with highest silhouette score for optimal clustering
            if score >= prev_highest_score and not k_too_big:
                prev_highest_score = score
                prev_highest_index = k_index
        opt_k = k_list[prev_highest_index]
        module_logger.info("best silhouette score: " + str(prev_highest_score))
        module_logger.info("found optimal k for KMeans: " + str(opt_k))
        return opt_k

    def _find_k_hdbscan(self, evaluation_examples, max_dim_clustering=50):
        """Uses hdbscan to downsample the evaluation examples.
        We use optimal k to determine how much to downsample the evaluation_examples.
        """
        import hdbscan
        num_rows = evaluation_examples.shape[0]
        reduced_eval_examples = self._reduce_eval_examples(evaluation_examples, max_dim_clustering)
        hdbs = hdbscan.HDBSCAN(min_cluster_size=2).fit(reduced_eval_examples)
        clusters = hdbs.labels_
        opt_k = len(set(clusters))
        clustering_threshold = 5
        samples = opt_k * clustering_threshold
        module_logger.info("found optimal k for hdbscan: " + str(opt_k) +
                           ", will use clustering_threshold * k for sampling: " + str(samples))
        return min(samples, num_rows)

    def _sample_evaluation_examples(self, evaluation_examples, max_dim_clustering=50, sampling_method="hdbscan"):
        """Samples the evaluation examples.  First does random downsampling to upper_bound rows,
        then tries to find the optimal downsample based on how many clusters can be constructed
        from the data.  If sampling_method is hdbscan, uses hdbscan to cluster the evaluation
        data and then downsamples to that number of clusters.  If sampling_method is k-means,
        uses different values of k, cutting in half each time, and chooses the k with highest
        silhouette score to determine how much to downsample the data.
        The danger of using only random downsampling is that we might downsample too much
        or too little, so the clustering approach is a heuristic to give us some idea of
        how much we should downsample to.
        """
        from sklearn.utils import resample
        lower_bound = 200
        upper_bound = 10000
        num_rows = evaluation_examples.shape[0]
        module_logger.info("sampling evaluation examples")
        # If less than lower_bound rows, just return the full dataset
        if num_rows < lower_bound:
            return evaluation_examples
        # If more than upper_bound rows, sample randomly
        elif num_rows > upper_bound:
            module_logger.info("randomly sampling to 10k rows")
            evaluation_examples = resample(evaluation_examples, n_samples=upper_bound, random_state=7)
            num_rows = upper_bound
        if sampling_method == "hdbscan":
            try:
                opt_k = self._find_k_hdbscan(evaluation_examples, max_dim_clustering)
            except Exception as ex:
                module_logger.warning("Failed to use hdbscan due to error: " + str(ex) +
                                      "\nEnsure hdbscan is installed with: pip install hdbscan")
                opt_k = self._find_k_kmeans(evaluation_examples, max_dim_clustering)
        else:
            opt_k = self._find_k_kmeans(evaluation_examples, max_dim_clustering)
        # Resample based on optimal number of clusters
        if (opt_k < num_rows):
            return resample(evaluation_examples, n_samples=opt_k, random_state=7)
        return evaluation_examples

    def _get_dense_examples(self, examples):
        if sp.sparse.issparse(examples):
            return examples.toarray()
        return examples

    def _run_tree_explainer(self, model, evaluation_examples, explain_subset):
        try:
            module_logger.debug("Attempting to use TreeExplainer")
            explainer = shap.TreeExplainer(model)

            # for now convert evaluation examples to dense format if they are sparse
            # until TreeExplainer sparse support is added
            shap_values = explainer.shap_values(self._get_dense_examples(evaluation_examples))
            classification = isinstance(shap_values, list)
            if explain_subset:
                if classification:
                    for i in range(shap_values.shape[0]):
                        shap_values[i] = shap_values[i][:, explain_subset]
                else:
                    shap_values = shap_values[:, explain_subset]
            return shap_values, classification, explainer
        except Exception as ex:
            module_logger.debug("Encountered error when using TreeExplainer: " + str(ex))
            return None

    def _run_deep_explainer(self, model, summary, evaluation_examples, **kwargs):
        try:
            explain_subset = kwargs.get("explain_subset", None)
            module_logger.debug("Attempting to use DeepExplainer")
            explainer = shap.DeepExplainer(model, summary)
            # sample the evaluation examples
            allow_eval_sampling = kwargs.get('allow_eval_sampling', False)
            if allow_eval_sampling:
                max_dim_clustering = kwargs.get("max_dim_clustering", 50)
                sampling_method = kwargs.get("sampling_method", "hdbscan")
                evaluation_examples = self._sample_evaluation_examples(evaluation_examples, max_dim_clustering,
                                                                       sampling_method=sampling_method)

            # for now convert evaluation examples to dense format if they are sparse
            # until DeepExplainer sparse support is added
            shap_values = explainer.shap_values(self._get_dense_examples(evaluation_examples))
            classification = isinstance(shap_values, list)
            if explain_subset:
                if classification:
                    for i in range(shap_values.shape[0]):
                        shap_values[i] = shap_values[i][:, explain_subset]
                else:
                    shap_values = shap_values[:, explain_subset]
            return shap_values, classification, explainer
        except Exception as ex:
            module_logger.debug("Encountered error when using DeepExplainer: " + str(ex))
            return None

    def _run_kernel_explainer(self, model, summary, evaluation_examples, original_evaluation, **kwargs):
        explain_subset = kwargs.get("explain_subset", None)

        def shap_values_on_prediction(f, summary):
            # Note: we capture index and f in the wrapper function below around the model prediction function.
            # When enumerating over the examples this values is updated and the update is visible in the
            # wrapper function below.  This is necessary to determine which example to tile when translating
            # back to the model's input domain.
            idx = 0

            def wrapper(data):
                """
                A private wrapper around the prediction function to add back in the removed columns
                when using the explain_subset parameter.
                We tile the original evaluation row by the number of samples generated
                and replace the subset of columns the user specified with the result from shap,
                which is the input data passed to the wrapper.
                :return: The prediction function wrapped by a helper method.
                """
                tiles = int(data.shape[0])
                evaluation_row = original_evaluation[idx]
                if sp.sparse.issparse(evaluation_row):
                    if not sp.sparse.isspmatrix_csr(evaluation_row):
                        evaluation_row = evaluation_row.tocsr()
                    nnz = evaluation_row.nnz
                    rows, cols = evaluation_row.shape
                    rows *= tiles
                    shape = rows, cols
                    if nnz == 0:
                        examples = sp.sparse.csr_matrix(shape, dtype=evaluation_row.dtype).tolil()
                    else:
                        new_indptr = np.arange(0, rows * nnz + 1, nnz)
                        new_data = np.tile(evaluation_row.data, rows)
                        new_indices = np.tile(evaluation_row.indices, rows)
                        examples = sp.sparse.csr_matrix((new_data, new_indices, new_indptr),
                                                        shape=shape).tolil()
                else:
                    examples = np.tile(original_evaluation[idx], tiles).reshape((data.shape[0],
                                                                                original_evaluation.shape[1]))
                examples[:, explain_subset] = data
                return f(examples)

            model_func = f
            if explain_subset:
                model_func = wrapper
            explainer = shap.KernelExplainer(model_func, summary)
            if explain_subset:
                output_shap_values = None
                for ex_idx, example in enumerate(evaluation_examples):
                    idx = ex_idx
                    tmp_shap_values = explainer.shap_values(example, **kwargs)
                    classification = isinstance(tmp_shap_values, list)
                    if classification:
                        if output_shap_values is None:
                            output_shap_values = tmp_shap_values
                            for i in range(len(output_shap_values)):
                                cols_dim = len(output_shap_values[i].shape)
                                concat_cols = output_shap_values[i].shape[cols_dim - 1]
                                output_shap_values[i] = output_shap_values[i].reshape(1, concat_cols)
                        else:
                            for i in range(len(output_shap_values)):
                                cols_dim = len(tmp_shap_values[i].shape)
                                # col_dim can only be 1 or 2 here, depending on data passed to shap
                                if cols_dim != 2:
                                    out_cols_dim = len(output_shap_values[i].shape)
                                    output_size = output_shap_values[i].shape[out_cols_dim - 1]
                                    tmp_shap_values_2d = tmp_shap_values[i].reshape(1, output_size)
                                else:
                                    tmp_shap_values_2d = tmp_shap_values[i]
                                # Append rows
                                output_shap_values[i] = np.append(output_shap_values[i],
                                                                  tmp_shap_values_2d, axis=0)
                    else:
                        if output_shap_values is None:
                            output_shap_values = tmp_shap_values
                        else:
                            output_shap_values = np.append(output_shap_values, tmp_shap_values, axis=0)
                return output_shap_values, explainer
            else:
                return explainer.shap_values(evaluation_examples, **kwargs), explainer

        def classification_shap_values(model, summary):
            f = model.predict_proba
            return shap_values_on_prediction(f, summary)

        def regression_shap_values(model, summary):
            f = model.predict
            return shap_values_on_prediction(f, summary)

        try:
            # try to use predict_proba for classification scenario
            shap_values, explainer = classification_shap_values(model, summary)
        except AttributeError as ae:
            module_logger.info(
                "predict_proba not supported by given model, assuming regression model and trying predict: " +
                str(ae))
            # try predict instead since this is likely a regression scenario
            shap_values, explainer = regression_shap_values(model, summary)
        classification = isinstance(shap_values, list)
        return shap_values, classification, explainer

    # Single node explain model function
    def explain_model(self, model, initialization_examples, evaluation_examples=None,
                      features=None, classes=None, nclusters=10,
                      top_k=None, create_scoring_model=False, **kwargs):
        """Explain a model by explaining its predictions on samples.
        :param model: An object that represents a model. It is assumed that for the classification case \
            it has a method of predict_proba() returning the prediction probabilities for each \
            class and for the regression case a method of predict() returning the prediction value.
        :type model: object
        :param initialization_examples: A matrix of feature vector examples (# examples x # features) for
            initializing the explainer. For small problems this set of examples for initialization can be
            the whole training set, but for larger problems consider using a single reference value or using
            the built-in kmeans function to summarize the whole or downsampled training set by
            specifying nclusters (the number of cluster centroids). A function summarize_data is
            also provided to summarize the initialization_examples separately. The output of this
            function can be passed to this method.
        :type initialization_examples: numpy.array or pandas.DataFrame or iml.datatypes.DenseData or
                                      scipy.sparse.csr_matrix
        :param evaluation_examples: A matrix of feature vector examples (# examples x # features) on which
            to explain the model's output.
        :type evaluation_examples: numpy.array or pandas.DataFrame or scipy.sparse.csr_matrix
        :param features: A list of feature names.
        :type features: list[str]
        :param classes: Class names, in any form that can be converted to an array of str. This includes
            lists, lists of tuples, tuples, tuples of tuples, tuples of lists and ndarrays. The order of
            the class names should match that of the model output.
        :type classes: array_like[str]
        :param nclusters: Number of means to use for approximation. A dataset is summarized with nclusters mean
            samples weighted by the number of data points they each represent. When the number of initialization
            examples is larger than (10 x nclusters), those examples will be summarized with k-means where
            k = nclusters.
        :type nclusters: int
        :param top_k: Number of the top most important features in model summary. If specified, only the model
            summary data corresponding to the top K most important features will be returned/stored.
        :type top_k: int
        :param create_scoring_model: Creates a model that can be used for scoring to approximate the feature
            importance values of data faster than SHAP.  See explain_from_scoring_model for more details.
        :type create_scoring_model: bool
        :return: tuple(run, feature_importance_values, expected_values, overall_feature_importance_values,
            overall_important_features, per_class_feature_importance_values, per_class_important_features)
            where
            - run = An object that represents an model explanation run. Only availabe if workspace
            and experiment_name are both provided.
            - feature_importance_values = For a model with a single output such as regression, this returns
            a matrix of feature importance values. For models with vector outputs this function returns a
            list of such matrices, one for each output. The dimension of this matrix is (# examples x # features).
            - expected_values = The expected value of the model applied to the set of initialization examples.
            For SHAP values, when a version older than 0.20.0 is used, this value is None. The expected
            values are in the last columns of the matrices in feature_importance_values. In this case, the
            dimension of those matrix is (# examples x (# features + 1)). This causes each row to sum to
            the model output for that example.
            - overall_feature_importance_values = The model level feature importance values sorted in
            descending order.
            - overall_important_features = The feature names sorted in the same order as in overall_summary
            or the indexes that would sort overall_summary.
            - per_class_feature_importance_values = The class level feature importance values sorted in
            descending order where a binary classification (this class or not) is evaluated. Only available
            for the classification case.
            - per_class_important_features = The feature names sorted in the same order as in per_class_summary
            or the indexes that would sort per_class_summary. Only available for the classification case.
        :rtype: (azureml.core.run.Run, Union[numpy.ndarray, list[numpy.ndarray]], numpy.ndarray, numpy.ndarray,
            numpy.ndarray, numpy.ndarray, numpy.ndarray)
        """
        if evaluation_examples is None:
            raise ValueError("evaluation_examples is required")
        explainer = None
        expected_values = None
        explain_subset = kwargs.get("explain_subset", None)
        # try to use TreeExplainer which is more accurate first
        result = self._run_tree_explainer(model, evaluation_examples, explain_subset)
        # if model is not a Tree-based model, try to use the Deep Explainer
        if (result is None):
            summary = summarize_data(initialization_examples, nclusters)
            module_logger.debug("Could not use TreeExplainer, using DeepExplainer instead")
            result = self._run_deep_explainer(model, summary, evaluation_examples, **kwargs)
            # otherwise, use the KernelExplainer as the default for least-specific-model
            if (result is None):
                module_logger.debug("Could not use TreeExplainer and DeepExplainer, using KernelExplainer instead")
                # Compute subset info prior
                original_evaluation = None
                if explain_subset:
                    original_evaluation = evaluation_examples
                    eval_is_df = isinstance(original_evaluation, pd.DataFrame)
                    eval_is_series = isinstance(original_evaluation, pd.Series)
                    if eval_is_df or eval_is_series:
                        original_evaluation = original_evaluation.values
                    evaluation_examples = original_evaluation[:, explain_subset]
                    init_is_df = isinstance(initialization_examples, pd.DataFrame)
                    init_is_series = isinstance(initialization_examples, pd.Series)
                    if init_is_df or init_is_series:
                        initialization_examples = initialization_examples.values
                    initialization_examples = initialization_examples[:, explain_subset]
                    # Edge case: Take the subset of the summary in this case,
                    # more optimal than recomputing the summary!
                    from shap.common import DenseData
                    if isinstance(summary, DenseData):
                        summary = DenseData(summary.data[:, explain_subset], summary.group_names[explain_subset])
                    else:
                        summary = summary[:, explain_subset]
                # sample the evaluation examples
                # note: the sampled data is also used by KNN below
                allow_eval_sampling = kwargs.get('allow_eval_sampling', False)
                if allow_eval_sampling:
                    max_dim_clustering = kwargs.get("max_dim_clustering", 50)
                    sampling_method = kwargs.get("sampling_method", "hdbscan")
                    evaluation_examples = self._sample_evaluation_examples(evaluation_examples, max_dim_clustering,
                                                                           sampling_method=sampling_method)
                result = self._run_kernel_explainer(model, summary, evaluation_examples, original_evaluation,
                                                    **kwargs)
        shap_values, classification, explainer = result
        if explainer is not None and hasattr(explainer, "expected_value"):
            expected_values = explainer.expected_value
        is_projection_required = False if top_k is None else True
        if classification:
            # calculate the summary
            per_class_summary = np.mean(np.absolute(shap_values), axis=1)
            i = np.arange(len(per_class_summary))[:, np.newaxis]
            per_class_order = self._order_imp(per_class_summary)
            overall_summary = np.mean(per_class_summary, axis=0)
            overall_order = self._order_imp(overall_summary)
            if is_projection_required and len(overall_order) > top_k:
                overall_order = overall_order[0:top_k]
                per_class_order = per_class_order[:, 0:top_k]
            # sort the per class summary
            per_class_summary = per_class_summary[i, per_class_order]
            # sort the overall summary
            overall_summary = overall_summary[overall_order]
        else:
            overall_summary = np.mean(np.absolute(shap_values), axis=0)
            overall_order = self._order_imp(overall_summary)
            if is_projection_required and len(overall_order) > top_k:
                overall_order = overall_order[0:top_k]
            # sort the overall summary
            overall_summary = overall_summary[overall_order]
        if features is not None:
            overall_imp = _sort_features(features, overall_order)
            if classification:
                per_class_imp = _sort_features(features, per_class_order)
        elif isinstance(initialization_examples, pd.DataFrame):
            features = initialization_examples.columns
            overall_imp = _sort_features(features, overall_order)
            if classification:
                per_class_imp = _sort_features(features, per_class_order)
        else:
            # return order of importance
            overall_imp = overall_order
            if classification:
                per_class_imp = per_class_order
        if create_scoring_model:
            # normalize features prior to using knn
            from sklearn.preprocessing import StandardScaler
            if sp.sparse.issparse(evaluation_examples):
                self.scaler = StandardScaler(with_mean=False).fit(evaluation_examples)
            else:
                self.scaler = StandardScaler().fit(evaluation_examples)
            # compute nearest neighbors, can be used in scoring path
            from sklearn.neighbors import NearestNeighbors
            scaled_data = self.scaler.transform(evaluation_examples)
            self.neighbors = NearestNeighbors(n_neighbors=1, algorithm='ball_tree').fit(scaled_data)
            self.nn_shap_values = shap_values
        if self.run is not None:
            # log the values to run history
            model_type = "classification" if classification else "regression"
            self.run.log('model_type', model_type)
            self.run.log('explainer', 'tabular')
            # upload the shap values, overall summary, per class summary, classes and feature names
            upload_dir = self._create_upload_dir()
            self._upload_artifact(upload_dir, 'shap_values', shap_values)
            if expected_values is not None:
                self._upload_artifact(upload_dir, 'expected_values', expected_values)
            if features is not None:
                self._upload_artifact(upload_dir, 'feature_names', features)
            self._upload_model_summary(upload_dir, 'overall_summary', overall_summary)
            self._upload_model_summary(upload_dir, 'overall_importance_order', overall_order)
            if classification:
                self._upload_model_summary(upload_dir, 'per_class_summary', per_class_summary)
                self._upload_model_summary(upload_dir, 'per_class_importance_order', per_class_order)
                if classes is not None:
                    self._upload_artifact(upload_dir, 'classes', np.asarray(classes))
                return self.run, shap_values, expected_values, overall_summary, overall_imp, \
                    per_class_summary, per_class_imp
            else:
                return self.run, shap_values, expected_values, overall_summary, overall_imp
        else:
            if classification:
                return shap_values, expected_values, overall_summary, overall_imp, per_class_summary, per_class_imp
            else:
                return shap_values, expected_values, overall_summary, overall_imp

    def explain_from_scoring_model(self, evaluation_examples):
        """Uses the model generated by explain_model for scoring to approximate the feature importance
        values of data faster than SHAP.

        :param evaluation_examples: A matrix of feature vector examples (# examples x # features) on
            which to explain the model's output.
        :type evaluation_examples: numpy.array or pandas.DataFrame or scipy.sparse.csr_matrix
        :return feature_importance_values: For a model with a single output such as regression,
            this returns a matrix of feature importance values. For models with vector outputs
            this function returns a list of such matrices, one for each output. The dimension
            of this matrix is (# examples x # features).
        :rtype feature_importance_values: numpy.ndarray or list[numpy.ndarray]
        """
        _, indices = self.neighbors.kneighbors(self.scaler.transform(evaluation_examples))
        # flatten indices for 1-NN
        indices = [index for row in indices for index in row]
        classification = isinstance(self.nn_shap_values, list)
        if classification:
            shap_values = []
            for i in range(len(self.nn_shap_values)):
                shap_values.append(self.nn_shap_values[i][indices])
            return shap_values
        else:
            return self.nn_shap_values[indices]
