def stringify_keys(d):
    """Convert a dict's keys to strings if they are not."""
    if hasattr(d, 'keys'):
        for key in d.keys():

            # check inner dict
            if isinstance(d[key], dict):
                value = stringify_keys(d[key])
            else:
                value = d[key]

            # convert nonstring to string if needed
            if not isinstance(key, str):
                # noinspection PyBroadException
                try:
                    d[str(key)] = value
                except Exception:
                    try:
                        d[repr(key)] = value
                    except Exception:
                        raise

                # delete old k
                del d[key]

    if hasattr(d, '__dict__'):
        for k in d.__dict__:
            if isinstance(getattr(d, k), dict):
                setattr(d, k, stringify_keys(getattr(d, k)))

    return d
