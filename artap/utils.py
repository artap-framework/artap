import collections

def flatten(l):
    output = []
    for item in l:
        if isinstance(item, collections.Iterable):
            for subitem in item:
                output.append(subitem)
        else:
            output.append(item)
    return output
