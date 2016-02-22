from fuzzywuzzy import fuzz

def field_pairs(n1, n2, empty=""):
    """
    Yields field pairs for both nodes, and empty if the node doesn't have
    that particular field.
    """
    fields = set(n1._fields) | set(n2._fields)
    for field in fields:
        yield getattr(n1, field, empty), getattr(n2, field, empty)


def similarity(n1, n2):
    """
    Returns the mean of the partial_ratio score for
    """

    scores = [
        fuzz.partial_ratio(f1, f2)
        for f1, f2 in field_pairs(n1, n2)
    ]

    return float(sum(s for s in scores)) / float(len(scores))


def fuzzblock(n1, n2, threshold=65):
    """
    Returns True if the similarity of n1 and n2 is above the threshold.
    """
    return similarity(n1, n2) > threshold
    

if __name__ == '__main__':
    from reader import Entity, Action, Detail

    e1 = Entity('Benjamin Bengfort', 'bbengfort@districtdatalabs.com')
    e2 = Entity('Ben Bengfort', 'bbengfort@districtdatalabs.com')
    e3 = Detail('Introduction to Machine Learning')

    print similarity(e1, e2)
    print similarity(e1, e3)
