from bgpack.map import MapError
from bgpack.utils import combine_groups


def optimize_sets(sets, bits_function, map_writer_class):
    """If 2 sets can be combined into a single one without increasing the number of bits: do it.
    The number of sets is kept, the only difference is that now both point to the same object in memory.

    The reason is that if combining two set we do not increase the number of bits needed to store
    the info, and assuming the time to search in larger map is independent of its size,
    combining the sets reduces the size of the map in memory"""
    distinct = {i: s for i, s in enumerate(sets)}  # TODO if isinstance(s, set) to remove indexes that have gone beyond the limits
    nbits = sum([bits_function(len(s)) for s in sets])
    combination = {}
    for grouped, ungrouped in combine_groups(list(distinct.keys()), []):
        if not grouped:  # skip the option of not grouping (as is the default)
            continue
        distinct_ = {}
        nbits_ = 0
        combination_ = {}
        for group in grouped:
            it = iter(group)
            key = next(it)
            distinct_[key] = sets[key].copy()
            for i in it:
                distinct_[key].update(sets[i])
                combination_[i] = key
            nbits_ += bits_function(len(distinct_[key])) * len(group)  # It is the same set for the whole group
        for i in ungrouped:
            distinct_[i] = sets[i]
            nbits_ += bits_function(len(distinct_[i]))
        if nbits_ == nbits:  # if the number of bits is kept, assume we have saved memory by combaining (for that combine_groups should return increasing size of groups)
            distinct = distinct_
            nbits = nbits_
            combination = combination_
        elif nbits_ < nbits:
            raise MapError('It should not be possible to reduce the number of bits by combining sets')  # TODO

    list_of_maps = [None ] *len(sets)
    for i, s in distinct.items():
        list_of_maps[i] = map_writer_class(s)
    for i, ii in combination.items():
        list_of_maps[i] = list_of_maps[ii]  # point to the same items
    if None in list_of_maps:
        raise MapError('Something went wrong during optimization')
    return list_of_maps
