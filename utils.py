import pandas as pd
import numpy as np
from scipy import stats

def get_right_whisker(df: pd.DataFrame, field: str) -> pd.DataFrame:
    q3 = np.percentile(df[field], 75)
    iqr =  q3 - np.percentile(df[field], 25)
    
    return q3 + 1.5 * iqr


def missing_values_table(df):
    '''eturns a DataFrame representing the amount of missing data among each column'''
    mis_val = df.isnull().sum()
    mis_val_percent = 100 * df.isnull().sum() / len(df)
    mis_val_table = pd.concat([mis_val, mis_val_percent], axis=1)
    mis_val_table_ren_columns = mis_val_table.rename(columns = {0 : 'Missing Values', 1 : '% of Total Values'})
    mis_val_table_ren_columns = mis_val_table_ren_columns[mis_val_table_ren_columns.iloc[:,1] != 0].sort_values('% of Total Values', ascending=False).round(1)
    print("Your selected dataframe has " + str(df.shape[1]) + " columns.\n"
          "There are " + str(mis_val_table_ren_columns.shape[0]) +
          " columns that have missing values.")
    return mis_val_table_ren_columns


def get_percent_missing(df: pd.DataFrame, columns=None):
    percent_missing = df.isnull().sum() * 100 / len(df)
    if not columns:
        return percent_missing

    return percent_missing[columns]


def trimmed_mean(df: pd.DataFrame, column: str, limit: float):
    '''Calculates the trimmed mean of the given column and with the given limit'''
    col_sorted = df.column.sort_values()
    col_sorted = col_sorted.reset_index(drop=True, inplace=False)
    upper_limit = col_sorted.quantile(1-limit)
    lower_limit = col_sorted.quantile(limit)
    limits = (lower_limit, upper_limit)
    trimmed_mean = stats.tmean(col_sorted, limits=limits)
    return trimmed_mean


def mean_absolute_deviation(df: pd.DataFrame, column: str):
    '''Calculates the mean absolute deviation of the given column'''
    mean = df.column.mean()
    num = np.sum(np.abs(df.column.values - mean)) / len(df.column)
    return num


def median_absolute_deviation(df: pd.DataFrame, column: str):
    '''Calculates the median absolute deviation of the given column'''
    median = df.column.median()
    num = np.sum(np.abs(df.column.values - median)) / len(df.column)
    return num


def variability_measures(df: pd.DataFrame, column: str, limit: float):
    '''Calculates some measures of variability on the given column of the given pandas dataframe'''
    print(f'Mean on column {column}: {df.column.mean()}')
    print(f'Median on column {column}: {df.column.median()}')
    print(f'Mode on column {column}: {df.column.mode()}')
    print(f'Variance on column {column}: {df.column.var()}')
    print(f'Standard deviation on column {column}: {df.column.std()}')
    print(f'Trimmed mean on column {column} with limit {limit}: {trimmed_mean(df, column, limit)}')
    print(f'Mean absolute deviation on column {column}: {mean_absolute_deviation(df, column)}')
    print(f'Median absolute deviation on column {column}: {median_absolute_deviation(df, column)}')