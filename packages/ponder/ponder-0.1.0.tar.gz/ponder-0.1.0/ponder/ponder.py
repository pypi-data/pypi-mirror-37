
import pandas as pd
import numpy as np
import inspect


# via stackoverflow and blog post... from Mark Byers / Jeff Atwood (?)
def sorted_alphanumeric(l, reverse=False):
    """
    Sorts the given iterable alphanumerically.
    If values are numeric, sort numerically; if strings, alphanumerically.
    If string operations don't work we just sort normally; this works for
    numeric types.
    """
    try:
        convert = lambda text: int(text) if text.isdigit() else text
        alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
        return sorted(l, key=alphanum_key, reverse=reverse)
    except TypeError:
        return sorted(l, reverse=reverse)


def guess_positive(categories):
    # try to guess which category should be 1 (vs 0)
    # go through positive-looking values in order of priority (somewhat arbitrary)
    for positive_value in ['true','yes','y','positive','pos','2','1']: # never
        # go through categories in order, since with case-insensitive string
        # representations, we could conceivably have more than one match
        for category in reversed(categories):
            if str(category).lower()==positive_value:
                return category
    # we didn't see a likely guess
    return None

def guess_negative(categories):
    # try to guess which category should be encoded as 0
    # go through positive-looking values in order of priority (somewhat arbitrary)
    for negative_value in ['false', 'no', 'negative', 'neg', 'n', '0', '1']:
        # go through categories in order, since with case-insensitive string
        # representations, we could conceivably have more than one match
        for category in categories:
            if str(category).lower()==negative_value:
                return category
    # we didn't see a likely guess
    return None


def one_hot_single(data, categories=None, expand_binary=False,
        name=None, base_category=None, treat_missing_as_zero=False):
    """
    Given a series of M categorical values,
    with N categories,
    return (encoded, categories, base_category), where
    - encoded is a binary-encoded MxN DataFrame of 0's and 1's,
    where each column corresponds to a category
    (or Mx(N-1) if we have a base category),
    - categories is the list of categories used for encoding,
    - base_category is the category that was encoded as a row of
    zeroes, or None if no base was used.

    The category name is encoded in the columns of the returned DataFrame,
    i.e. each column name is of form {OriginalFieldName}_{CategoryName}.

    If base_category is provided, encode this category as all zeroes, so that
    one less column is created and there is no redundancy.

    If expand_binary is False, and input series has only two levels,
    keep it as one binary column even if base_category is not provided. In this case,
    try to guess which of the two categories is which. The category treated
    as base will be returned in base_category and will not appear in the output.
    """
    if len(data.shape)>1:
        data = data.iloc[:,0] # make Series

    vec = data.astype('category')

    if categories is None:
        categories = vec.cat.categories
    else:
        # when categories are supplied, check they account for all data
        # if user-supplied categories don't cover data,
        # pandas' default behaviour will be to create missing data
        # we instead want to raise an error
        if not set(data).issubset(set(categories)):
            print('data', data)
            print('supplied categories', categories)
            raise ValueError(
                "Cannot encode data as categories in categorical field {}".format(name)
                + " do not match categories in previously-fit data. You must set your"
                + " categorical Series to have all expected category levels."
                + " New categories were: {}".format(set(data)-set(categories)))
        vec.cat.set_categories(categories, inplace=True)

    # Do encoding, with one column per category
    # This will incorrectly encode missing values using index of code, i.e. index -1
    encoded = pd.DataFrame(np.eye(len(categories), dtype=int)[vec.cat.codes])
    # Fix missing values: set to zero or to missing
    missing_rows = data.isnull()
    if np.any(missing_rows):
        if treat_missing_as_zero:
            encoded.loc[list(missing_rows),:] = 0
        else:
            encoded.loc[list(missing_rows),:] = None

    if name is None:
        name = data.name
    encoded.columns = ['{}_{}'.format(name, c) for c in vec.cat.categories]
    encoded.index = data.index

    # If base_category is None for >2 categories, use no base (create all columns)
    # When there are 2 categories and expand_binary=False, we must pick a base
    # If we are encoding for transform, in this situation, it will be set already
    # If we are encoding for fit we may have to choose based on the data

    if base_category is None and not expand_binary and len(categories)==2:
        if vec.cat.ordered:
            base_category = vec.cat.categories[0]
        else:
            # try to guess binary base_category (actually, guess positive)
            positive_category = guess_positive(categories)
            assert positive_category is None or positive_category in categories
            # this will be the first category if positive_category was None,
            # otherwise the non-positive category
            base_category = [c for c in categories if c != positive_category][0]

    # If we know or have picked base_category, encode this as zeroes by deleting that column
    if base_category is not None:
        encoded.drop("{}_{}".format(name, base_category), axis=1, inplace=True)

    return (encoded,categories,base_category)


def one_hot_group(data, categories=None, expand_binary=False, base_category=None,
            name=None, treat_missing_as_zero=False):
    """
    Given a dataframe of only categorical values, with M rows,
    and a total of N distinct categories,
    return (encoded, categories, base_category), where
    - encoded is a binary-encoded MxN DataFrame of 0's and 1's,
    where each column corresponds to a category
    (or Mx(N-1) if we have a base category),
    - categories is the list of categories used for encoding,
    - base_category is the category that was encoded as a row of
    zeroes, or None if no base was used. For one_hot_group this will be the
    same base_category that was passed in.

    All columns are treated as entries in the *same* category,
    i.e. more than one column in a row of the output encoding may be 1.
    If any input column is null, it is ignored and fewer 1's are set for that row.
    However, if treat_missing_as_zero==False (the default), and ALL inputs for
    a row are null, return a row of None's - i.e. assume data is missing.
    If treat_missing_as_zero==True, return a row of zeroes - i.e. assume the values
    for that row are not missing, but that there are truly no categories set.

    The category name is encoded in the columns of the returned DataFrame,
    i.e. each column name is of form {name}_{CategoryName}, where name is provided.

    If category levels between input columns are not identical, the union of
    categories will be used, sorted alphanumerically in output.

    If base_category is provided, encode this category as all zeroes, so that
    one less column is created and there is no redundancy.
    """
    # First make sure categorical; re-encode consistently later
    for c in data:
        data[c] = data[c].astype('category')

    # Get all categories in all columns
    category_list = [data[c].cat.categories for c in data]

    observed_categories = set(sum(category_list,[]))
    # If categories were provided, check they cover data
    if categories is not None:
        if not set(observed_categories).issubset(set(categories)):
            raise ValueError(
                "Cannot encode data as categories in categorical field {}".format(name)
                + " do not match expected categories."
                + " If you used fit_df, you must set your training data Categorical dtype"
                + " to have all expected category levels."
                + " New categories were: {}".format(set(observed_categories)-set(categories)))
    else:
        # if any one category-set is a superset of all the others, use that
        for cats in category_list:
            if set(cats) == all_categories:
                categories = cats
                break
        # if still no valid category set, use union of all
        if categories is None:
            categories = sorted_alphanumeric(set.union(*[set(cats) for cats in category_list]))

    # Re-encode category codes consistently
    # (and unordered - this should not matter?)
    for c in data:
        data[c].cat.set_categories(categories, inplace=True)

    # Encode each column and take union
    encoded = np.zeros((len(data), len(categories)), dtype=int)
    for c in data:
        # NB this sets missing values to code -1, which will be mis-encoded by np indexing
        vec = data[c].cat.codes
        encoded_var = np.eye(len(categories))[vec]
        # Fix missing values: set to zero for sake of OR operation
        encoded_var[data[c].isnull(),:] = 0
        encoded = np.logical_or(encoded, encoded_var)
    encoded = pd.DataFrame(encoded.astype(int))
    # If desired, set entirely missing values to missing
    if not treat_missing_as_zero:
        missing_rows = np.all(data.isnull(),axis=1)
        if np.any(missing_rows):
            encoded.loc[list(missing_rows),:] = None
    if name is None:
        name = '_'.join(data.columns)
    encoded.columns = ['{}_{}'.format(name, c) for c in categories]
    encoded.index = data.index

    # If we know base_category, encode this as zeroes by deleting that column
    if base_category is not None:
        encoded.drop("{}_{}".format(name, base_category), axis=1, inplace=True)

    return (encoded,categories,base_category)


def one_hot(data, categories=None, expand_binary=False, base_category=None,
            name=None, treat_missing_as_zero=False):
    """
    Binary-encode categorical data.
    We can handle a single Series or a categorical DataFrame where each column
    is to be encoded into the same output variable.

    Calls one_hot_single() and one_hot_group().
    """

    if base_category is not None and treat_missing_as_zero:
        raise ValueError("Cannot use base_category when treat_missing_as_zero "
                         + "is True; meaning of all-zero row is overloaded.")

    if len(data.shape)==1 or data.shape[1]==1:
        # We have a single column
        return one_hot_single(data, categories=categories,
            expand_binary=expand_binary, base_category=base_category,
            name=name, treat_missing_as_zero=treat_missing_as_zero)

    else:
        # We have a group of multiple columns
        return one_hot_group(data, categories=categories,
            expand_binary=expand_binary, base_category=base_category,
            name=name, treat_missing_as_zero=treat_missing_as_zero)


def one_hot_many(df,
                 expand_binary=False,
                 base_categories=None,
                 grouped_columns=None,
                 treat_missing_as_zero=False,
                 map_features=None):
    """
    Given a dataframe containing all categorical columns,
    one-hot encode them all.
    dtypes which can be converted to categories (e.g. strings and booleans) will
    also be handled, although any categories missing in the data will not be known.
    Convenient usage is to pass in your df with .select_dtypes([np.object, 'category', 'bool']).
    If base_categories is provided, it should be a dict mapping
    df column names to the category representing the null value for that column.
    These will be passed as base_category to one_hot()
    grouped_columns should be a dict of the form {outputfieldname:[listofinputfields]}.
    Any fields in these lists will be encoded as if they were one binary-encoded
    variable, with the union of their values treated as levels in the variable.
    """
    if base_categories is None:
        base_categories = {}
    if grouped_columns is None:
        grouped_columns = {}
    if map_features is None:
        map_features = {}

    grouped_inputs = set(sum(grouped_columns.values(),[]))
    for field in df.columns:
        if field not in grouped_inputs:
            grouped_columns[field] = [field]

    for field in grouped_inputs:
        if field not in df.columns:
            raise ValueError('Grouped field {} not in input dataframe'.format(field))
    encoded_list = []

    feature_mapping = dict()
    base_categories_used = dict()
    for (fieldname,inputlist) in grouped_columns.items():
        encoded_field, categories, base_category = one_hot(
            df[inputlist],
            treat_missing_as_zero=treat_missing_as_zero,
            categories=map_features.get(fieldname,None),
            base_category=base_categories.get(fieldname,None),
            name=fieldname)
        encoded_list.append(encoded_field)
        feature_mapping[fieldname] = list(categories)
        base_categories_used[fieldname] = base_category # may be none

    return (pd.concat(encoded_list, axis=1),
            feature_mapping,
            base_categories_used)


# datetimes are not yet handled

def encode(df,
           expand_binary=False,
           base_categories=None,
           grouped_columns=None,
           treat_missing_as_zero=False,
           drop_unhandled=False,
           map_features=None):
    """
    Encode columns of a dataframe numerically, according to their Series dtype.
    Return
    - the encoded dataframe
    - a dict giving any mappings from original columns to encoded columns
    - any base categories used for categoricals to remove redundant columns

    Encodings are:
    - categoricals, objects/strings and booleans will be binary (one-hot) encoded
    - numeric columns will be unchanged
    - datetimes are currently not handled correctly and will be unchanged, and
    a warning will be issued
    """
    # Categories
    category_columns = df.select_dtypes([np.object, 'category', 'bool']).columns
    if len(category_columns) > 1:
        encoded_categories, feature_mapping, base_categories_used = one_hot_many(
            df.select_dtypes([np.object, 'category', 'bool']),
            expand_binary=expand_binary,
            base_categories=base_categories,
            grouped_columns=grouped_columns,
            treat_missing_as_zero=treat_missing_as_zero,
            map_features = map_features)
    else:
        encoded_categories = pd.DataFrame(index=df.index)
        feature_mapping = dict()

    # Numbers
    numeric_columns = df.select_dtypes([np.number]).columns

    # Dates
    date_columns = df.select_dtypes(['datetime']).columns
    if len(date_columns) > 0:
        print("Warning: dates not yet handled by encoding: {}".format(date_columns))

    encoded_columns = set.union(
        set(category_columns),set(numeric_columns),set(date_columns))
    unhandled_columns = list(set(df.columns) - encoded_columns)
    if len(unhandled_columns) > 0:
        print("Warning: some column types were not recognised during encoding: {}".format(unhandled_columns))

    if drop_unhandled:
        result = pd.concat([encoded_categories,
                           df[numeric_columns],
                           df[date_columns]], axis=1),
    else:
        # we are keeping these columns as the user apparently thinks numpy will handle them
        result = pd.concat([encoded_categories,
                           df[numeric_columns],
                           df[date_columns],
                           df[unhandled_columns]], axis=1)

    return (result, feature_mapping, base_categories_used)


fit_docstring = '''
fit_df wraps the fit method, allowing X to be a pandas.DataFrame.

Refer to the fit method documentation for functionality details.
fit parameters are: {}
'''

transform_docstring = '''
transform_df wraps the transform method, allowing X to be a pandas.DataFrame.

Refer to the transform method documentation for functionality details.
transform parameters are: {}
'''

predict_docstring = '''
predict_df wraps the predict method, allowing X to be a pandas.DataFrame.
This method returns a Series of class predictions.

Refer to the predict method documentation for functionality details.
predict parameters are: {}
'''

predict_log_proba_docstring = '''
predict_log_proba_df wraps the predict_log_proba method, allowing X to be a pandas.DataFrame.
This method returns a DataFrame of log-probabilities.

Refer to the predict_log_proba method documentation for functionality details.
predict_log_proba parameters are: {}
'''

predict_proba_docstring = '''
predict_proba_df wraps the predict_proba method, allowing X to be a pandas.DataFrame.
This method returns a DataFrame of probabilities.

Refer to the predict_proba method documentation for functionality details.
predict_proba parameters are: {}
'''

feature_importances_docstring = '''
feature_importances_df_ is a property wrapping feature_importances_,
allowing X to be a pandas.DataFrame. It returns feature importances
as a pandas Series representing the original dataframe fields.
For categorical variables, importances are calculated using the
sqrt of the sum of squares of mapped feature importances.

Refer to the feature_importances_ property documentation for functionality details.
'''

def encode_for_fit(model,
                   X,
                   expand_binary=False,
                   base_categories=None,
                   grouped_columns=None,
                   treat_missing_as_zero=False,
                   drop_unhandled=False):
    '''
    Encode a dataframe as numerical values, and store all needed metadata
    about the encoding in the model.

    feature_mapping stored specifies the categories used in the fit, which will
    be taken from the Series.cat categories if available, and their order in
    the encoding, with the first category considered the base category.
    If expand_binary=False and there are two categories for some feature,
    the first of the categories in the list will not occur in the encoded data
    and will be stored in feature_mapping but not feature_lookup.

    feature_lookup covers encoded fieldnames of all types, not just categories,
    and allows us to look up the feature name from the original fit dataframe.
    '''
    # we don't pass in map_features; this will be based on category dtypes
    encoded, feature_mapping, base_categories_used = encode(X,
        expand_binary=expand_binary, treat_missing_as_zero=treat_missing_as_zero,
        base_categories=base_categories, grouped_columns=grouped_columns,
        drop_unhandled=drop_unhandled)
    model.expand_binary = expand_binary
    if grouped_columns is None:
        grouped_columns = {}
    model.grouped_columns = grouped_columns
    model.treat_missing_as_zero = treat_missing_as_zero
    model.drop_unhandled = drop_unhandled
    model.base_categories_used = base_categories_used
    model.features_original = list(X.columns)
    model.features_encoded = list(encoded.columns)
    model.feature_mapping = feature_mapping
    # store lookup of original feature names for all encoded columns
    model.feature_lookup = {}
    for (feature,mappedlist) in feature_mapping.items():
        if not expand_binary and len(mappedlist)==2:
            mappedlist = mappedlist[1:]
        for mapped in mappedlist:
            model.feature_lookup['{}_{}'.format(feature,mapped)] = feature
    # store lookup of original feature names for unmapped features (i.e. non-categorical)
    for feature in model.features_encoded:
        if feature not in model.feature_lookup:
            model.feature_lookup[feature] = feature

    return encoded


def encode_for_transform(model, X):
    '''
    Encode a dataframe as numerical values, using the same encoding as used
    in the fit.
    '''
    encoded, _feature_mapping, _base_categories = encode(
        X,
        expand_binary=model.expand_binary,
        base_categories=model.base_categories_used,
        map_features=model.feature_mapping,
        grouped_columns=model.grouped_columns,
        treat_missing_as_zero=model.treat_missing_as_zero,
        drop_unhandled=model.drop_unhandled)
    return encoded


def add_fit(model):
    parameters = inspect.signature(model.fit).parameters
    if 'y' in parameters and parameters['y'].default == inspect._empty:

        # if we define this elsewhere, model.fit_df.__name__ will be wrong
        def fit_df(self,
                   X,
                   y,
                   expand_binary=False,
                   base_categories=None,
                   grouped_columns=None,
                   treat_missing_as_zero=False,
                   drop_unhandled=False,
                   **kwargs):
            '''
            fit_df method to be added to the model.
            This docstring should be overwritten - if it's visible,
            please report a bug.
            '''
            encoded = encode_for_fit(self, X, expand_binary=expand_binary,
                base_categories=base_categories, grouped_columns=grouped_columns,
                treat_missing_as_zero=treat_missing_as_zero,
                drop_unhandled=drop_unhandled)
            return self.fit(encoded, y, **kwargs)

    elif 'y' in parameters:

        def fit_df(self,
                   X,
                   y=parameters['y'].default,
                   expand_binary=False,
                   base_categories=None,
                   grouped_columns=None,
                   treat_missing_as_zero=False,
                   drop_unhandled=False,
                   **kwargs):
            '''
            fit_df method to be added to the model.
            This docstring should be overwritten - if it's visible,
            please report a bug.
            '''
            encoded = encode_for_fit(self, X, expand_binary=expand_binary,
                base_categories=base_categories, grouped_columns=grouped_columns,
                treat_missing_as_zero=treat_missing_as_zero,
                drop_unhandled=drop_unhandled)
            return self.fit(encoded, y, **kwargs)

    else:

        def fit_df(self,
                   X,
                   expand_binary=False,
                   base_categories=None,
                   grouped_columns=None,
                   treat_missing_as_zero=False,
                   drop_unhandled=False,
                   **kwargs):
            '''
            fit_df method to be added to the model.
            This docstring should be overwritten - if it's visible,
            please report a bug.
            '''
            encoded = encode_for_fit(self, X, expand_binary=expand_binary,
                base_categories=base_categories, grouped_columns=grouped_columns,
                treat_missing_as_zero=treat_missing_as_zero,
                drop_unhandled=drop_unhandled)
            return self.fit(encoded, **kwargs)

    model.fit_df = fit_df.__get__(model)
    model.fit_df.__func__.__qualname__ = '.'.join(
        model.fit.__qualname__.split('.')[:-1] + ['fit_df'])
    model.fit_df.__func__.__doc__ = fit_docstring.format(
        str(inspect.signature(model.fit)))
    # if preserving original docstring would add model.fit.__doc__


def add_transform(model):

    def transform_df(self, X, **kwargs):
        '''
        transform_df method to be added to the model.
        This docstring should be overwritten - if it's visible,
        please report a bug.
        '''
        encoded = encode_for_transform(self, X)
        return self.transform(encoded, **kwargs)

    model.transform_df = transform_df.__get__(model)
    model.transform_df.__func__.__qualname__ = '.'.join(
        model.transform.__qualname__.split('.')[:-1] + ['transform_df'])
    model.transform_df.__func__.__doc__ = transform_docstring.format(
        str(inspect.signature(model.transform)))


def add_predict(model):

    def predict_df(self, X, **kwargs):
        '''
        predict_df method to be added to the model.
        This docstring should be overwritten - if it's visible, please report a bug.
        '''
        encoded = encode_for_transform(self, X)
        # TODO: encode with categorical matching input y?
        # will already do classes based on classes_
        result = self.predict(encoded, **kwargs)
        return pd.Series(result, index=X.index)

    model.predict_df = predict_df.__get__(model)
    model.predict_df.__func__.__qualname__ = '.'.join(
        model.predict.__qualname__.split('.')[:-1] + ['predict_df'])
    model.predict_df.__func__.__doc__ = transform_docstring.format(
        str(inspect.signature(model.predict)))


def add_predict_proba(model):

    def predict_proba_df(self, X, **kwargs):
        '''
        predict_proba_df method to be added to the model.
        This docstring should be overwritten - if it's visible,
        please report a bug.
        '''
        encoded = encode_for_transform(self, X)
        result = self.predict_proba(encoded, **kwargs)
        return pd.DataFrame(result, index=X.index, columns=self.classes_)

    model.predict_proba_df = predict_proba_df.__get__(model)
    model.predict_proba_df.__func__.__qualname__ = '.'.join(
        model.predict_proba.__qualname__.split('.')[:-1]
        + ['predict_proba_df'])
    model.predict_proba_df.__func__.__doc__ = transform_docstring.format(
        str(inspect.signature(model.predict_proba)))


def add_predict_log_proba(model):

    def predict_log_proba_df(self, X, **kwargs):
        '''
        predict_log_proba_df method to be added to the model.
        This docstring should be overwritten - if it's visible, please report a bug.
        '''
        encoded = encode_for_transform(self, X)
        result = self.predict_log_proba(encoded, **kwargs)
        return pd.DataFrame(result, index=X.index, columns=self.classes_)

    model.predict_log_proba_df = predict_log_proba_df.__get__(model)
    model.predict_log_proba_df.__func__.__qualname__ = '.'.join(
        model.predict_log_proba.__qualname__.split('.')[:-1]
        + ['predict_log_proba_df'])
    model.predict_log_proba_df.__func__.__doc__ = transform_docstring.format(
        str(inspect.signature(model.predict_log_proba)))


def add_feature_importances(model):

    def feature_importances_df(self):
        '''
        feature_importances_df_ property to be added to the model.
        This docstring should be overwritten - if it's visible,
        please report a bug.
        '''
        raw_importances = pd.Series(self.feature_importances_, index=self.features_encoded)
        feature_positions = pd.Series(
            [self.feature_lookup[feature] for feature in self.features_encoded],
            index = self.features_encoded)
        original_importances = np.sqrt((raw_importances**2).groupby(feature_positions).sum())
        # sort by original feature order
        original_importances = original_importances[self.features_original]
        return original_importances

    model.feature_importances_df = feature_importances_df.__get__(model)
    # can we do this for a property?
    #model.feature_importances_df_.__func__.__qualname__ = '.'.join(
    #    model.feature_importances_.__qualname__.split('.')[:-1] + ['feature_importances_df_'])
    model.feature_importances_df.__func__.__doc__ = feature_importances_docstring


def use_dataframes(model):
    """
    Given an sklearn model object that implements any one or more of:
    - fit
    - transform
    - predict
    - predict_proba
    - predict_log_proba
    - feature_importances_
    return an object augmented with corresponding
    fit_df, transform_df etc methods
    which operate on and return Pandas DataFrames and Series.

    Auxilliary information needed to handle a fitted dataframe - e.g. column
    (feature) names and binary encodings of categorical variables - are stored
    in the fitted model instance.

    These methods make use of the DataFrame column dtypes, which must be set
    correctly.
    """
    members = set([f for (f, obj) in inspect.getmembers(model)])

    if 'fit' in members:
        print('Adding fit_df')
        add_fit(model)

    if 'transform' in members:
        print('Adding transform_df')
        add_transform(model)

    if 'predict' in members:
        print('Adding predict_df')
        add_predict(model)

    if 'predict_proba' in members:
        print('Adding predict_proba_df')
        add_predict_proba(model)

    if 'predict_log_proba' in members:
        print('Adding predict_log_proba_df')
        add_predict_log_proba(model)

    # feature_importances_ is a property
    # It is present before fitting but throws a NotFittedError
    # inspect ignores it due to this; use dir()
    if 'feature_importances_' in dir(model):
        print('Adding feature_importances_df')
        add_feature_importances(model)

    return model
