import math
import itertools


def bits2bytes(bits):
    math.ceil(bits/8)


def required_bits(distinct_values):
    """
    Number of bits required to store n values
    """
    if distinct_values == 1:
        return 1
    else:
        return math.ceil(math.log(distinct_values, 2))


def required_bytes(distinct_values):
    """
    Number of bits required to store n values
    """
    nbits = required_bits(distinct_values)
    return math.ceil(nbits/8)


def bytes4bits(nbits):
    return math.ceil(nbits / 8)


def get_groups(items):
    """Get all possible combinations of a list of items in groups of 2, 3,..., n and ungrouped items"""
    for i in range(2, len(items) + 1):
        for combo in itertools.combinations(items, i):
            ungrouped = [it for it in items if it not in combo]
            for it in combo:
                if it not in ungrouped:
                    in_combo = combo.count(it)
                    in_items = items.count(it)
                    ungrouped += [it] * (in_items-in_combo)
            yield combo, ungrouped


def combine_groups(items, groups):
    """
    Get all possible combinations of items into grouped
    (which is a list of groups, where each groups contains the empty keys)
    and not grouped items.
    For the first call use groups=[]
    """
    for group, rest in get_groups(items):
        for v in combine_groups(rest, groups + [group]):
            yield v
    else:
        yield groups, items
