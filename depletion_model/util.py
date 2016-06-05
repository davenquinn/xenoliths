from periodictable import elements

def element_name(number):
    return elements[number].symbol

def element_number(name):
    return getattr(elements, name).number

