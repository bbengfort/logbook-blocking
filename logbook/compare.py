from fuzzywuzzy import fuzz
from collections import defaultdict

def field_pairs(n1, n2, empty=""):
    """
    Yields field pairs for both nodes, and empty if the node doesn't have
    that particular field. This function will also normalize the fields, e.g.
    by converting everything to lowercase or removing the domain from email.
    """

    def normalize_field(value):
        """
        For now, just make everything lowercase and strip white space.
        """
        return value.lower().replace(" ", "")


    def normalize_email(email):
        """
        Only return the username, not the domain.
        """
        return normalize_field(email.split("@")[0])


    normalize = defaultdict(lambda: normalize_field)
    normalize['email'] = normalize_email

    fields = set(n1._fields) | set(n2._fields)
    for field in fields:
        norm = normalize[field]
        yield norm(getattr(n1, field, empty)), norm(getattr(n2, field, empty))


def similarity(n1, n2):
    """
    Returns the mean of the partial_ratio score for each field in the two
    entities. Note that if they don't have fields that match, the score will
    be zero.
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
    e2 = Entity('Ben Bengfort', 'benjamin@bengfort.com')
    e3 = Detail('Introduction to Machine Learning')

    print similarity(e1, e2)
    print similarity(e1, e3)


    for field in field_pairs(e1, e2):
        print field
