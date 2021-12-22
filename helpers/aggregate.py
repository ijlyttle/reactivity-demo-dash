import pandas as pd

def aggregate_df (df, cols_group, cols_agg, func_agg):
    if (not cols_group is None):
        df = df.groupby(cols_group)

    if (cols_agg is None or len(cols_agg) == 0):
        return []
    
    dict_agg = {}
    for col in cols_agg:
        dict_agg[col] = func_agg
    
    # aggregate DataFrame
    df = df.agg(dict_agg).reset_index()

    return df