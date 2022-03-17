import pandas as pd
import numpy as np

def get_right_whisker(df: pd.DataFrame, field: str) -> pd.DataFrame:
    q3 = np.percentile(df[field], 75)
    iqr =  q3 - np.percentile(df[field], 25)
    
    return q3 + 1.5 * iqr