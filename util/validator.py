from jsonschema import validate, ValidationError


class Validator:

    @staticmethod
    def validate_body(body, schema):
        try:
            validate(body, schema)
        except ValidationError as e:
            raise e

    @staticmethod
    def validate_params(headers, params):
        if headers is not None and headers.environ is not None:
            if headers.environ['QUERY_STRING'] is not None and headers.environ['QUERY_STRING'] != "":
                for param in headers.environ['QUERY_STRING'].split('&'):
                    sorts = param.split('=')
                    if sorts.__len__() == 2:
                        if sorts[0] not in params:
                            raise ValidationError('Filter not allowed.')
                        elif sorts[0] == 'maxItemsPerPage' and (int(sorts[1]) > 50 or int(sorts[1]) <= 0):
                            raise ValidationError('maxItemsPerPage value not allowed, must be greater than 0 and less or equal 50.')
                        elif sorts[0] == 'currentPage' and int(sorts[1]) <= 0:
                            raise ValidationError('currentPage value not allowed, must be greater than or equal 1.')
                    else:
                        raise ValidationError('Filter not allowed.')
