from flask import jsonify


def success_ok(body=None):
    '''
    Returns a 200 - OK response object.
    '''
    code = 200
    headers = {}
    return serialize(make_response((body, code, headers)))


def success_created(pk, location=None):
    '''
    Returns a 201 - Created response object.
    '''
    body = {'pk': pk}
    code = 201
    headers = {}
    if location:
        headers['location'] = location
    return serialize(make_response((body, code, headers)))


def success_no_content():
    '''
    Returns a 204 - No Content response object.
    '''
    code = 204
    headers = {}
    return serialize(make_response((None, code, headers)))


def error_bad_request(body=None):
    '''
    Returns a 400 - Bad request response object.
    '''
    code = 400
    headers = {}
    return serialize(make_response((body, code, headers)))


def error_not_found(body=None):
    '''
    Returns a 404 - Not Found response object.
    '''
    code = 404
    headers = {}
    return serialize(make_response((body, code, headers)))


def error_precondition_failed(body=None):
    '''
    Returns a 412 - Precondition Failed response object.
    '''
    code = 412
    headers = {}
    return serialize(make_response((body, code, headers)))


def error_unprocessable_entity(body=None):
    '''
    Returns a 422 - Unprocessable Entity response object.
    '''
    code = 422
    headers = {}
    return serialize(make_response((body, code, headers)))


def error_precondition_required(body=None):
    '''
    Returns a 428 - Precondition Required response object.
    '''
    code = 428
    headers = {}
    return serialize(make_response((body, code, headers)))


def error_unexpected_error(body=None):
    '''
    Returns a 500 - Internal server error response object.
    '''
    code = 500
    headers = {}
    return serialize(make_response((body, code, headers)))


def error_not_implemented(body=None):
    '''
    Returns a 501 - Not Implemented response object.
    '''
    code = 501
    headers = {}
    return serialize(make_response((body, code, headers)))


def serialize(response):
    '''
    '''
    return jsonify(response)
