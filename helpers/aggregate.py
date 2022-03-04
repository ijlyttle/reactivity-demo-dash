import pandas as pd

agg_function_choices = ['mean', 'min', 'max']

def aggregate_df (df, cols_group, cols_agg, func_agg,
                  str_fn_choices = agg_function_choices):
    
    if not func_agg in str_fn_choices:
        raise AssertionError(f"{func_agg} not a legal function-choice")
  
    if (cols_group != None):
        df = df.groupby(cols_group)

    if (cols_agg == None or len(cols_agg) == 0):
        return []
    
    # dictionary, keys: column-names, values: function-name
    dict_agg = {i: func_agg for i in cols_agg}
    
    df = df.agg(dict_agg).reset_index()

    return df
