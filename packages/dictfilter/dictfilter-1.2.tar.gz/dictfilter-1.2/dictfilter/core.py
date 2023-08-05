def _filter(data, fields):
    out = {}

    for field in fields:
        key, *rest = field.split('.', maxsplit=1)

        if key not in data:
            # TODO: maybe add a 'strict' option to raise an exception here.
            continue

        if rest:
            many = isinstance(data[key], list)
            sub_element = query(data[key], rest)

            existing_element = out.get(key, [] if many else {})
            if many and existing_element:
                for current, new in zip(out[key], sub_element):
                    current.update(new)
            elif not many and existing_element:
                out[key].update(sub_element)
            else:
                out[key] = sub_element
        else:
            out[key] = data[key]

    return out


def query(data, fields):
    many = isinstance(data, list)
    if many:
        return [_filter(d, fields) for d in data]
    else:
        return _filter(data, fields)
