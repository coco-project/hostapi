from coco.contract.backends import ContainerBackend
from coco.hostapi import config
from coco.hostapi.http.responses import *
from flask import Blueprint
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
        status = get_status()
        if status.get('backends').get('container').get('status') is ContainerBackend.BACKEND_STATUS_OK:
            return success_no_content()
        else:
            return error_unexpected_error("Container backend not OK")
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
