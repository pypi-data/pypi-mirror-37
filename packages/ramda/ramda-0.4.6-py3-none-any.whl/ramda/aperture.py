from ramda.curry import curry


@curry
def aperture(n, xs):
    """Returns a new list, composed of n-tuples of consecutive elements. If n is
greater than the length of the list, an empty list is returned.
Acts as a transducer if a transformer is given in list position"""

    if n > len(xs):
        return []

    return [xs[i:i + n] for i in range(0, len(xs), n)]
