

class ParamsUtils:

    @staticmethod
    def update_params(params, query_string):
        if query_string and query_string != '':
            for param in query_string.split('&'):
                sorts = param.split('=')
                params.update({sorts[0]: int(sorts[1])})
        return params
