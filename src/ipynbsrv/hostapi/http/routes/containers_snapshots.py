from flask import Blueprint, request
from ipynbsrv.contract.backends import *
from ipynbsrv.hostapi.backends.container_backends import Docker
from ipynbsrv.hostapi.http.routes.common import error_response, success_response

'''
'''
blueprint = Blueprint('containers_snapshots', __name__, url_prefix='/containers')
container_backend = Docker(version="1.18")


@blueprint.route('/<container>/snapshots/<snapshot>/restore', methods=['GET'])
def restore_container_snapshot(container, snapshot):
    '''
    Returns information about the snapshot of the given container.
    '''
    try:
        restored = container_backend.restore_container_snapshot(container, snapshot)
        return success_response(restored)
    except ContainerNotFoundError:
        return error_response(404, "Container not found")
    except ContainerSnapshotNotFoundError:
        return error_response(404, "Container snapshot not found")
    except IllegalContainerStateError:
        return success_response(412, "Container in illegal state for requested action")
    except ContainerBackendError:
        return error_response(500, "Unexpected container backend error")
    except:
        return error_response(500, "Something unexpected happened")


@blueprint.route('/<container>/snapshots/<snapshot>', methods=['DELETE'])
def delete_container_snapshot(container, snapshot):
    '''
    Deletes the snapshot of the container.
    '''
    try:
        deleted = container_backend.delete_container_snapshot(container, snapshot)
        return success_response(deleted)
    except ContainerNotFoundError:
        return error_response(404, "Container not found")
    except ContainerSnapshotNotFoundError:
        return error_response(404, "Container snapshot not found")
    except IllegalContainerStateError:
        return success_response(412, "Container in illegal state for requested action")
    except ContainerBackendError:
        return error_response(500, "Unexpected container backend error")
    except:
        return error_response(500, "Something unexpected happened")


@blueprint.route('/<container>/snapshots/<snapshot>', methods=['GET'])
def get_container_snapshot(container, snapshot):
    '''
    Returns information about the snapshot of the given container.
    '''
    try:
        snapshot = container_backend.get_container_snapshot(container, snapshot)
        return success_response(snapshot)
    except ContainerNotFoundError:
        return error_response(404, "Container not found")
    except ContainerSnapshotNotFoundError:
        return error_response(404, "Container snapshot not found")
    except IllegalContainerStateError:
        return success_response(412, "Container in illegal state for requested action")
    except ContainerBackendError:
        return error_response(500, "Unexpected container backend error")
    except:
        return error_response(500, "Something unexpected happened")


@blueprint.route('/<container>/snapshots', methods=['GET'])
def get_container_snapshots(container):
    '''
    Returns a list of snapshots for the container.
    '''
    try:
        snapshots = container_backend.get_container_snapshots(container)
        return success_response(snapshots)
    except ContainerNotFoundError:
        return error_response(404, "Container not found")
    except ContainerSnapshotNotFoundError:
        return error_response(404, "Container snapshot not found")
    except IllegalContainerStateError:
        return success_response(412, "Container in illegal state for requested action")
    except ContainerBackendError:
        return error_response(500, "Unexpected container backend error")
    except:
        return error_response(500, "Something unexpected happened")


@blueprint.route('/<container>/snapshots', methods=['POST'])
def create_container_snapshot(container):
    '''
    Creates a new snapshot of the container.
    '''
    try:
        json = request.get_json()
        try:
            snapshot = container_backend.create_container_snapshot(container, json.get('snapshot'))
            return success_response(snapshot)
        except ContainerNotFoundError:
            return error_response(404, "Container not found")
        except ContainerSnapshotNotFoundError:
            return error_response(404, "Container snapshot not found")
        except IllegalContainerStateError:
            return success_response(412, "Container in illegal state for requested action")
        except ContainerBackendError:
            return error_response(500, "Unexpected container backend error")
        except:
            return error_response(500, "Something unexpected happened")
    except:
        return error_response(400, "Bad request")
