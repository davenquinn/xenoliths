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

