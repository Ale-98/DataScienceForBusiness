import pandas as pd
import numpy as np

def get_right_whisker(df: pd.DataFrame, field: str) -> pd.DataFrame:
    q3 = np.percentile(df[field], 75)
    iqr =  q3 - np.percentile(df[field], 25)
    
    return q3 + 1.5 * iqr


def missing_values_table(df):
    '''args:
        df: input dataframe on which calculate the missing values
       return: a DataFrame representing the amount of missing data among each column
    '''
    mis_val = df.isnull().sum()
    mis_val_percent = 100 * df.isnull().sum() / len(df)
    mis_val_table = pd.concat([mis_val, mis_val_percent], axis=1)
    mis_val_table_ren_columns = mis_val_table.rename(columns = {0 : 'Missing Values', 1 : '% of Total Values'})
    mis_val_table_ren_columns = mis_val_table_ren_columns[mis_val_table_ren_columns.iloc[:,1] != 0].sort_values('% of Total Values', ascending=False).round(1)
    print("Your selected dataframe has " + str(df.shape[1]) + " columns.\n"
          "There are " + str(mis_val_table_ren_columns.shape[0]) +
          " columns that have missing values.")
    return mis_val_table_ren_columns