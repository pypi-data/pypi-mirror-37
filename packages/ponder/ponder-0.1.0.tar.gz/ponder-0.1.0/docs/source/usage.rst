=====
Usage
=====

This documentation is preliminary and only a usage outline exists.

The main function in ponder is :func:`~ponder.use_dataframes`.
This function binds extra methods to a scikit-learn model instance,
allowing it to easily handle Pandas DataFrames. ponder takes advantage of scikit-learn's consistent API interface, and Pandas' column dtypes.

For example:

.. code-block:: python

    from ponder import use_dataframes
    from sklearn.decomposition import PCA

    pca = use_dataframes(PCA())

The :py:obj:`pca` object will now have a :func:`fit_df()` method, a :func:`transform_df()` method, etc. These methods automatically encode the columns of a DataFrame according to their dtype, so that they can be treated as numeric. For instance, categorical fields will be binary/one-hot encoded.

Detailed documentation for the extra functions added by :func:`~ponder.use_dataframes`
is TBD. Currently we add, whenever the underlying functions exist:

- :func:`fit_df()`
- :func:`transform_df()`
- :func:`predict_df()`
- :func:`predict_proba_df()`
- :func:`predict_log_proba_df()`
- :func:`feature_importances_df()` (note that this wraps the :py:attr:`feature_importances_` property, but is a method rather than a property).

Currently, dtypes handled sensibly are:

- numeric: left as they are
- categorical, boolean and object/string: binary (one-hot) encoded. Category levels are respected if the dtype is category.

Datetimes are not yet handled.

Remaining parts of the scikit-learn API are in progress - please create a github issue if you would like particular features to be prioritised.
