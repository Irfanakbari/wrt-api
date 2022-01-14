import json


def error(error_code, error_message):
    return json.dumps({'error': {'code': error_code, 'message': error_message}})
