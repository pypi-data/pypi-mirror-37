import copy


def none_to_emptystring(data):
    """convert None to ''

    https://stackoverflow.com/questions/11410896/python-how-json-dumps-none-to-empty-string
    """

    # Converts None to empty string
    ret = copy.deepcopy(data)
    # Handle dictionaries, lits & tuples. Scrub all values
    if isinstance(data, dict):
        for k, v in ret.items():
            ret[k] = none_to_emptystring(v)
    if isinstance(data, (list, tuple)):
        for k, v in enumerate(ret):
            ret[k] = none_to_emptystring(v)
    # Handle None
    if data is None:
        ret = ""
    # Finished scrubbing
    return ret
