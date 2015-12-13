def element_data(data,columns='element'):
    all_cols = data.reset_index()

    ix = ['sample_id','mineral']
    n = all_cols.groupby(ix)['n'].max()
    df = all_cols.pivot_table(
            rows=ix,
            columns=columns,
            values=['average'],
            aggfunc=lambda x: x)
    df.columns = df.columns.get_level_values(1)
    return df.join(n)
