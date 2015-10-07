from flask import make_response
import json


def success_ok(body):
    """
    Return a 200 - OK response object.
    """
    return json_response(body, 200)


def success_created(body, location=None):
    """
    Return a 201 - Created response object.
    """
    headers = {}
    if location:
        headers['Location'] = location
    return json_response(body, 201, headers)


def success_no_content():
    """
    Return a 204 - No Content response object.
    """
    return make_response(('', 204, None))


def error_bad_request(body=None):
    """
    Return a 400 - Bad request response object.
    """
    body = {'error': body}
    return json_response(body, 400)


def error_not_found(body=None):
    """
    Return a 404 - Not Found response object.
    """
    body = {'error': body}
    return json_response(body, 404)


def error_precondition_failed(body=None):
    """
    Return a 412 - Precondition Failed response object.
    """
    body = {'error': body}
    return json_response(body, 412)


def error_unprocessable_entity(body=None):
    """
    Return a 422 - Unprocessable Entity response object.
    """
    body = {'error': body}
    return json_response(body, 422)


def error_precondition_required(body=None):
    """
    Return a 428 - Precondition Required response object.
    """
    body = {'error': body}
    return json_response(body, 428)


def error_unexpected_error(body=None):
    """
    Return a 500 - Internal server error response object.
    """
    body = {'error': body}
    return json_response(body, 500)


def error_not_implemented(body=None):
    """
    Return a 501 - Not Implemented response object.
    """
    body = {'error': body}
    return json_response(body, 501)


def json_response(body, code, headers=None):
    """
    TODO: write doc.
    """
    response_headers = {
        'Content-Type': 'application/json'
    }
    if headers:
        response_headers.update(headers)

    return make_response((json.dumps(body), code, response_headers))
