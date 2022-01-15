import json


def success():
    return json.dumps({
        'code': 200,
        'status': 'success',
    }, indent=4)


def error_connection():
    return json.dumps({
        'code': 500,
        'status': 'error',
        'message': 'Server Connection Error'
    }, indent=4)
