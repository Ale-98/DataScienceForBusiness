import pandas as pd
import numpy as np
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score

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
    col_sorted = df[column].sort_values()
    col_sorted = col_sorted.reset_index(drop=True, inplace=False)
    upper_limit = col_sorted.quantile(1-limit)
    lower_limit = col_sorted.quantile(limit)
    limits = (lower_limit, upper_limit)
    trimmed_mean = stats.tmean(col_sorted, limits=limits)
    return trimmed_mean


def mean_absolute_deviation(df: pd.DataFrame, column: str):
    '''Calculates the mean absolute deviation of the given column'''
    mean = df[column].mean()
    num = np.sum(np.abs(df[column].values - mean)) / len(df[column])
    return num


def median_absolute_deviation(df: pd.DataFrame, column: str):
    '''Calculates the median absolute deviation of the given column'''
    median = df[column].median()
    num = np.sum(np.abs(df[column].values - median)) / len(df[column])
    return num


def variability_measures(df: pd.DataFrame, column: str, limit: float):
    '''Calculates some measures of variability on the given column of the given pandas dataframe'''
    print(f'Mean on column {column}: {df[column].mean()}')
    print(f'Median on column {column}: {df[column].median()}')
    print(f'Mode on column {column}: {df[column].mode()}')
    print(f'Variance on column {column}: {df[column].var()}')
    print(f'Standard deviation on column {column}: {df[column].std()}')
    print(f'Trimmed mean on column {column} with limit {limit}: {trimmed_mean(df, column, limit)}')
    print(f'Mean absolute deviation on column {column}: {mean_absolute_deviation(df, column)}')
    print(f'Median absolute deviation on column {column}: {median_absolute_deviation(df, column)}')


def plot_frequency_table(df: pd.DataFrame, column: str):
    freq_table = df[column].value_counts()
    freq_table.plot.barh(
        x=freq_table.index,
        y=freq_table.values,
    )

def plot_frequency_pie(df: pd.DataFrame, column: str):
    freq_table = df[column].value_counts()
    colors = sns.color_palette('pastel')[0:5]
    plt.pie(freq_table.values, labels=freq_table.index, colors=colors, autopct='%.0f%%')
    plt.show()

def sort_by(df: pd.DataFrame, column: str):
    df = df.sort_values(by=column, ascending=True)
    df.reset_index(drop=True, inplace=True)
    min_ok = df.DATA.min() == df.DATA[0]
    max_ok = df.DATA.max() == df.DATA[len(df) - 1]
    print('Sorted' if min_ok and max_ok else 'Not sorted')

def overfit_eval(model, X, Y):
    
    """
    model: the trained model
    X: a tuple like (x_train, x_test)
    Y: a tuple like (Y_train, Y_test)
    """

    Y_pred_train = model.predict(X[0])
    Y_pred_test = model.predict(X[1])
    
    mse_train = mean_squared_error(Y[0], Y_pred_train)
    mse_test = mean_squared_error(Y[1], Y_pred_test)

    r2_train = r2_score(Y[0], Y_pred_train)
    r2_test = r2_score(Y[1], Y_pred_test)  
    
    print("Train set:  MSE="+str(mse_train)+" R2="+str(r2_train))
    print("Test set:  MSE="+str(mse_test)+" R2="+str(r2_test))

    return (mse_train, mse_test), (r2_train, r2_test)
    return (mse_train, mse_test), (r2_train, r2_test)
def create_prophet_features(df, label=None):
    df = df.copy()
    df['date'] = df.index
    df['hour'] = df['date'].dt.hour
    df['dayofweek'] = df['date'].dt.dayofweek
    df['quarter'] = df['date'].dt.quarter
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    df['dayofyear'] = df['date'].dt.dayofyear
    df['dayofmonth'] = df['date'].dt.day
    df['weekofyear'] = df['date'].dt.weekofyear
    
    X = df[['hour','dayofweek','quarter','month','year',
           'dayofyear','dayofmonth','weekofyear']]
    if label:
        y = df[label]
        return X, y
    return X
    return X
