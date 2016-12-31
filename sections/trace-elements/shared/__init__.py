def mineral_data(data, mineral):
    """
    Gets dataframe for a specific mineral
    """
    px_data = data[
        data.index.map(lambda x: x[1] == mineral)]
    #del px_data['n']
    px_data.index = px_data.index.droplevel(1)
    return px_data
