import pandas as pd
from pathlib import Path

def import_data(dir_path: Path, header: int = 0):
    '''
    Import all csv files from directory dir_path data into a dictionary of dataframes, with the option to specify the number of header rows.
    The same number of header rows are assumed per file.
    Special characters and spaces in column names are removed.
    '''
    dfs = {}

    for file in dir_path.glob('*.csv'):
        df = import_csv(file, header=header)
        dfs[file.name] = df

    return dfs

def import_csv(file_path, header=0):
    '''
    Import data from a CSV file, with the option to specify the number of header rows.
    Special characters and spaces in column names are removed.
    '''
    df = pd.read_csv(file_path, header=header)
    simplify_feature_names(df)
    df = add_coords(df)
    
    return df


def add_coords(df) -> pd.DataFrame:
    '''
    Add coordinates to a DataFrame from coord_csv using the 'Code' column as the key.
    '''
    coord_csv = Path("src/nhs_dashboard/data/coordinates.csv")
    coords = pd.read_csv(coord_csv)
    
    df = df.merge(coords, on='Code', how='left')
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