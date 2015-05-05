from flask import jsonify


def error_response(code, error=None):
    '''
    '''
    response = {'status': code}
    if error:
        response['error'] = error
    return jsonify(response)


def success_response(data=None):
    '''
    '''
    response = {'status': 200}
    if data:
        response['data'] = data
    return jsonify(response)
