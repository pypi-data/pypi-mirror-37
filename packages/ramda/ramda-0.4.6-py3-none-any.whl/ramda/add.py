from ramda.curry import curry


@curry
def add(x, y):
    """Adds two values"""
    return x + y
