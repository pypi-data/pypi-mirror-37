from functools import wraps
from inspect import signature

from flask import jsonify, request, Response

from ..validation.validator import ValidationException

def rest(f):
    param_name='data'

    @wraps(f)
    def wrapper(*args, **kwargs):
        fsig = signature(f)

        try:
            if param_name in fsig.parameters.keys():
                fkwargs = kwargs.copy()
                fkwargs[param_name] = request.json
                result = f(*args, **fkwargs)
            else:
                result = f(*args, **kwargs)

            return jsonify(result) if type(result) != Response else result

        except ValidationException as ex:
            response = jsonify(ex.result.to_dict())
            response.status_code = 500

            return response

        except Exception as ex:
            response = jsonify(str(ex))
            response.status_code = 500

            return response

    return wrapper
