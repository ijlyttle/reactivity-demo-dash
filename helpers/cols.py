import pandas as pd

def cols_choice (df, include):
    col_names = df.select_dtypes(include=include).columns.to_list()
  
    return col_names

def cols_header (data_records):
    cols = []
    if (len(data_records) > 0):
        cols = [{'name': i, 'id': i} for i in data_records[0].keys()]

    return cols
