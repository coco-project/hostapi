from flask import Blueprint
from ipynbsrv.hostapi.http.responses import error_not_implemented


"""
Flask blueprint collecting the /health routes.
"""
blueprint = Blueprint('health', __name__, url_prefix='/health')


@blueprint.route('', methods=['GET'])
def get_health(container):
    """
    Return the node's health (report).

    The main application is querying this entry-point from time to time to determinate
    either the node is still up (and healthy) or if it has problems.

    TODO: return general health information (e.g. OK, out of memory), container backend (is running),
          diskspace etc.
    """
    return error_not_implemented()
