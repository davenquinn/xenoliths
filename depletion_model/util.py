from periodictable import elements

def element(id):
    """
    Get symbol of element from number, or number
    from symbol. Function is its own inverse.
    """
    try:
        return elements[id].symbol
    except KeyError:
        return getattr(elements, id).number

def ree_data(df):
    La, Lu, Tm = element('La'), element('Lu'), element('Tm')

    def __should_delete(col):
        try:
            n = element(col)
        except AttributeError:
            return True
        if n < La: return True
        if n > Lu: return True
        if n == Tm: return True
        return False

    cols = filter(__should_delete, df.columns)
    df = df.drop(cols, axis=1)
    # Convert to numeric representation of elements
    df.columns = map(element, df.columns)
    return df[df.columns.sort_values()]

