import pandas as pd

def cols_choice (df, include):
    return df.select_dtypes(include=include).columns.to_list()

def cols_header (data_records):
  
    if (len(data_records) == 0):
        return []

    return [{'name': v, 'id': v} for v in data_records[0].keys()]
