
'''
Utilities for testing.
'''

import pandas as pd

def parse_test_df(f):
    '''
    Given a filehandle or filename for a CSV file,
    return the dataframe, assuming our standard dtypes
    for standard column names.
    '''
    df = pd.read_csv(f)
    df['Boolean'] = df['Boolean'].astype('bool')
    df['Binary'] = pd.Categorical(df['Binary'], categories=['No','Yes'])
    df['Ordinal'] = pd.Categorical(df['Ordinal'],
        categories=['Small','Medium','Large'], ordered=True)
    df['Nominal'] = pd.Categorical(df['Nominal'],
        categories=['Red','Yellow','Green'])
    df['Nominal2'] = pd.Categorical(df['Nominal2'],
        categories=['Negative','PositiveA','PositiveB'])
    return df
