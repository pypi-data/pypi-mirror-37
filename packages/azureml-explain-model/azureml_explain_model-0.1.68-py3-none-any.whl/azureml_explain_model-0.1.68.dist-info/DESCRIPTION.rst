Microsoft Azure Machine Learning Explain Model API for Python
===================================================

This package has been tested with Python 2.7 and 3.6.

This is a preview release
=========================

The SDK is being released as a preview, for gathering feedback.

**Future releases are subject to breaking changes.**

Machine learning (ML) explain model package is used to explain black box ML models.

 * The TabularExplainer can be used to give local and global feature importances
 * Local feature importances are for each evaluation row
 * Global feature importances summarize the most importance features at the model-level
 * Model explanations can be operationalized via explain_from_scoring_model
 * The API supports both dense (numpy or pandas) and sparse (scipy) datasets
 * The best explainer is automatically chosen for the user based on the model




