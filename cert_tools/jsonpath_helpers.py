from jsonpath_rw import parse, Root, Child, Fields


def additional_global_fields(config, raw_json):
    if config.additional_global_fields:
        for field in config.additional_global_fields:
            jp = parse(field['path'])
            matches = jp.find(raw_json)
            if matches:
                for match in matches:
                    jsonpath_expr = get_path(match)
                    raw_json = update_json(raw_json, jsonpath_expr, field['value'])
            else:
                fields = []
                recurse(jp, fields)
                temp_json = raw_json
                for idx, f in enumerate(fields):
                    if f in temp_json:
                        temp_json = temp_json[f]
                    elif idx == len(fields) - 1:
                        temp_json[f] = field['value']
                    else:
                        print('path is not valid! : %s', '.'.join(fields))
    return raw_json


def get_path(match):
    """
    return an iterator based upon MATCH.PATH. Each item is a path component, start from outer most item.
    :param match:
    :return:
    """
    if match.context is not None:
        for path_element in get_path(match.context):
            yield path_element
        yield str(match.path)


def recurse(child, fields_reverse):
    if isinstance(child, Fields):
        fields_reverse.append(child.fields[0])
    else:
        if not isinstance(child, Child):
            raise Exception('unexpected input')
        if not isinstance(child.left, Root):
            recurse(child.left, fields_reverse)
        recurse(child.right, fields_reverse)


def update_json(json, path, value):
    '''Update JSON dictionary PATH with VALUE. Return updated JSON'''
    try:
        first = next(path)
        # check if item is an array
        if first.startswith('[') and first.endswith(']'):
            try:
                first = int(first[1:-1])
            except ValueError:
                pass
        json[first] = update_json(json[first], path, value)
        return json
    except StopIteration:
        return value


def set_field(raw_json, path, value):
    jp = parse(path)
    matches = jp.find(raw_json)
    if matches:
        for match in matches:
            jsonpath_expr = get_path(match)
            raw_json = update_json(raw_json, jsonpath_expr, value)
    else:
        fields = []
        recurse(jp, fields)
        temp_json = raw_json
        for idx, f in enumerate(fields):
            if f in temp_json:
                temp_json = temp_json[f]
            elif idx == len(fields) - 1:
                temp_json[f] = value
            else:
                msg = 'path is not valid! : ' + '.'.join(fields)
                print(msg)
                raise (Exception(msg))
    return raw_json
