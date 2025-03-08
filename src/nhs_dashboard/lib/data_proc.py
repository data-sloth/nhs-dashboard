import pandas as pd

def import_data(file_path, header=0):
    '''
    Import data from a CSV file, with the option to specify the number of header rows.
    Special characters and spaces in column names are removed.
    '''
    df = pd.read_csv(file_path, header=header)
    simplify_feature_names(df)
    
    return df


def simplify_feature_names(df):
    '''
    Simplify pandas column names for display in UI. 
    Remove spaces and special characters for pydeck compatibility.
    '''
    df.columns = df.columns.str.replace(' ', '')
    df.columns = df.columns.str.replace('<', 'lessthan')
    df.columns = df.columns.str.replace('>', 'morethan')
    df.columns = df.columns.str.replace('(', 'of')
    df.columns = df.columns.str.replace(')', '')

def select_features(df, regex):
    '''
    Select features from a DataFrame based on a regular expression, and convert them to numeric
    '''
    features = (df.filter(regex=regex))
    for feature in features.columns:
        df[feature] = pd.to_numeric(df[feature], errors='coerce')

    return features