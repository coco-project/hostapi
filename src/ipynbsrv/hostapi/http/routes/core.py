from flask import Blueprint
from ipynbsrv.hostapi import config
from ipynbsrv.hostapi.http.responses import *
import psutil


"""
Flask blueprint collecting the core (/) routes.
"""
blueprint = Blueprint('core', __name__)


@blueprint.route('/health', methods=['GET'])
def get_health():
    """
    Endpoint to be queried to check the node's health.

    Everything other than a 2xx response (could) indicate a problem
    and further actions should be performed to find the reason and/or fix it.
    """
    try:
        return success_no_content()
    except Exception:
        return error_unexpected_error()


@blueprint.route('/status', methods=['GET'])
def get_status():
    """
    Return the node's status report.

    The main application is querying this entry-point from time to time to determinate
    the nodes status.
    """
    try:
        return success_ok({
            'backends': {
                'container': {
                    'status': config.container_backend.get_status()
                }
            },
            'resources': {
                'cpu': {
                    'count': psutil.cpu_count(),
                    'usage': psutil.cpu_percent()
                },
                'disk': psutil.disk_usage('/').__dict__,
                'memory': psutil.virtual_memory().__dict__,
                'swap': psutil.swap_memory().__dict__
            }
        })
    except Exception:
        return error_unexpected_error()
