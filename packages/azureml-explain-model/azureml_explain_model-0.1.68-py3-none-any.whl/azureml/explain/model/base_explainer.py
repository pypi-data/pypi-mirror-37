# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Defines the base explainer to explain and visualize the feature importances of a model."""

import os
import pickle
from math import ceil

from .common import MAX_NUM_BLOCKS, BLOCK_SIZE, NUM_FEATURES, NUM_BLOCKS, module_logger, \
    new_shap_api, minimum_shap_version


class BaseExplainer:
    """The base class for explainers."""
    def __init__(self, workspace=None, experiment_name=None, run_id=None):
        """Initializes the explainer.

        :param workspace: An object that represents a workspace.
        :type workspace: azureml.core.workspace.Workspace
        :param experiment_name: The name of an experiment.
        :type experiment_name: str
        :param run_id: A GUID that represents a run.
        :type run_id: str
        """
        self.run = None
        self.storage_policy = {MAX_NUM_BLOCKS: 3, BLOCK_SIZE: 100}
        args_none = [arg is None for arg in [workspace, experiment_name]]
        # Validate either all the arguments above are specified or all are None
        if not any(args_none):
            try:
                from azureml.core import Experiment, Run
            except ImportError as exp:
                module_logger.error(
                    "Could not import azureml.core, required if specifying workspace and experiment name")
                raise exp
            experiment = Experiment(workspace, experiment_name)
            if run_id is None:
                # Create a new run
                self.run = experiment.start_logging()
            else:
                # Create a run object to reference the original one with the same run_id
                self.run = Run(experiment, run_id=run_id)
        elif not all(args_none):
            raise ValueError("Both or neither of workspace and experiment name need to be specified")

    def _order_imp(self, summary):
        if new_shap_api:
            return summary.argsort()[..., ::-1]
        else:
            module_logger.debug(
                "An older version of SHAP than the mimimum requirement %s is used", minimum_shap_version)
            return summary[..., 0:-1].argsort()[..., ::-1]

    def _create_upload_dir(self):
        # create the outputs folder
        upload_dir = './upload_explanation/'
        os.makedirs(upload_dir, exist_ok=True)
        return upload_dir

    def _upload_artifact(self, upload_dir, artifact_name, values):
        # serialize the shap values on disk in the special 'outputs' folder
        path = os.path.join(upload_dir, artifact_name + '.pkl')
        f = open(path, 'wb')
        pickle.dump(values, f)
        f.close()
        self.run.upload_file(artifact_name + '.pkl', path)

    def _get_num_of_blocks(self, num_of_columns):
        block_size = self.storage_policy[BLOCK_SIZE]
        num_blocks = ceil(num_of_columns / block_size)
        max_num_blocks = self.storage_policy[MAX_NUM_BLOCKS]
        if num_blocks > max_num_blocks:
            num_blocks = max_num_blocks
        return num_blocks

    def _upload_model_summary(self, upload_dir, name, summary):
        num_columns = summary.shape[len(summary.shape) - 1]
        num_blocks = self._get_num_of_blocks(num_columns)
        block_size = self.storage_policy[BLOCK_SIZE]
        storage_metadata = dict()
        storage_metadata[MAX_NUM_BLOCKS] = [self.storage_policy[MAX_NUM_BLOCKS]]
        storage_metadata[BLOCK_SIZE] = [self.storage_policy[BLOCK_SIZE]]
        storage_metadata[NUM_FEATURES] = [num_columns]
        storage_metadata[NUM_BLOCKS] = [num_blocks]
        # Save metadata for this summary to Run History
        self.run.log_table(name, storage_metadata)
        # Chunk the summary and save it to Artifact
        start = 0
        for idx in range(num_blocks - 1):
            cols = slice(start, start + block_size)
            block = summary[..., cols]
            block_name = name + "_" + str(idx)
            self._upload_artifact(upload_dir, block_name, block)
            start += block_size
        # The last block
        cols = slice(start, num_columns)
        block = summary[..., cols]
        block_name = name + "_" + str(num_blocks - 1)
        self._upload_artifact(upload_dir, block_name, block)

    def get_storage_policy(self):
        """Returns the current storage policy.

        :rtype: dict
        :return: The storage policy represented as a dictionary of settings.
        """
        # return the current storage policy
        return self.storage_policy

    def set_storage_policy(self, block_size=None, max_num_blocks=None):
        """Sets the current storage policy.

        :param block_size: The size of each block for the summary stored in artifacts storage.
        :type block_size: int
        :param max_num_blocks: The maximum number of blocks to store.
        :type max_num_blocks: int
        """
        if block_size is not None:
            self.storage_policy[BLOCK_SIZE] = block_size
        if max_num_blocks is not None:
            self.storage_policy[MAX_NUM_BLOCKS] = max_num_blocks
