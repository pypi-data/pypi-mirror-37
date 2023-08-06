from functools import wraps


class Validator:
    def __init__(self, *rules):
        self.__rules = rules

    def validate(self, data):
        result = ValidationResult()
        
        for x in self.__rules:
            x(data, result)

        return result

    def raise_if_failed(self, data):
        result = self.validate(data)

        if result.has_errors():
            raise ValidationException(result)


class ValidationException(Exception):
    __result = None

    def __init__(self, result):
        self.__result = result

    @property
    def result(self):
        return self.__result


class ValidationResult:
    def __init__(self):
        self.__model_errors = []
        self.__field_errors = {}

    def add_model_error(self, error):
        self.__model_errors.append(error)

    def add_field_error(self, name, error):
        if name not in self.__field_errors:
            self.__field_errors[name] = []

        self.__field_errors[name].append(error)

    def has_errors(self):
        return self.has_model_errors() or self.has_field_errors()

    def has_model_errors(self):
        return len(self.__model_errors) > 0

    def has_field_errors(self, field=None):
        return len(self.__field_errors) > 0 \
            if not field \
            else len(self.__field_errors.get(field, [])) > 0

    def get_model_errors(self):
        return self.__model_errors.copy()

    def get_field_errors(self, field=None):
        return self.__field_errors.copy() \
            if not field \
            else self.__field_errors.get(field, []).copy()

    def to_dict(self):
        return {
            'model': self.__model_errors.copy(),
            'fields': self.__field_errors.copy()
        }


def validated(validator, param_name='data'):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if param_name in kwargs:
                data = kwargs.get('data')
                if data:
                    validator.raise_if_failed(data)
            else:
                print('No data')

            return f(*args, **kwargs)

        return wrapper

    return decorator
