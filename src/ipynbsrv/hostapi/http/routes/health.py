from flask import Blueprint
from ipynbsrv.hostapi import config
from ipynbsrv.hostapi.http.responses import success_ok
import psutil


"""
Flask blueprint collecting the /health routes.
"""
blueprint = Blueprint('health', __name__, url_prefix='/health')


@blueprint.route('', methods=['GET'])
def get_health():
    """
    Return the node's health (report).

    The main application is querying this entry-point from time to time to determinate
    either the node is still up (and healthy) or if it has problems.

    TODO: return general health information (e.g. OK, out of memory), container backend (is running),
          diskspace etc.
    """
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
