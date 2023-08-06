def __value_by_path(data, path):
    tokens = path.split('.')

    r = data
    for x in tokens:
        if x not in r:
            return None

        r = r[x]

    return r


def field(path, *field_rules):
    def validate(data, result):
        v = __value_by_path(data, path)

        for x in field_rules:
            x(path, v, result)

    return validate


def required():
    def validate(name, value, result):
        if not value:
            result.add_field_error(name, 'required')

    return validate


def min_length(count):
    def validate(name, value, result):
        if not value or type(value) != str:
            return

        if len(value) < count:
            result.add_field_error(name, 'min_length:{}'.format(count))
    
    return validate


def max_length(count):
    def validate(name, value, result):
        if not value or type(value) != str:
            return

        if len(value) > count:
            result.add_field_error(name, 'max_length:{}'.format(count))
    
    return validate
