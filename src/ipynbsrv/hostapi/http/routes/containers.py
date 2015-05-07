from flask import Blueprint, request
from ipynbsrv.contract.backends import *
from ipynbsrv.hostapi.backends.container_backends import Docker
from ipynbsrv.hostapi.http.routes.common import error_response, success_response

'''
'''
blueprint = Blueprint('containers', __name__, url_prefix='/containers')
container_backend = Docker(version="1.18")


@blueprint.route('/<container>/clone', methods=['POST'])
def clone_container(container):
    '''
    '''
    if not isinstance(container_backend, CloneableContainerBackend):
        return error_response(428, "Container backend does not support the clone operation")

    return error_response(501, "Not implemented")


@blueprint.route('/<container>/exec', methods=['POST'])
def exec_in_container(container):
    '''
    '''
    try:
        command = request.get_json(force=True).get('command')
        if command:
            try:
                output = container_backend.exec_in_container(container, command)
                return success_response(output)
            except ContainerNotFoundError:
                return error_response(404, "Container not found")
            except IllegalContainerStateError:
                return error_response(412, "Container in illegal state for requested action")
            except ContainerBackendError:
                return error_response(500, "Unexpected container backend error")
            except NotImplementedError:
                return error_response(501, "Not implemented")
            except:
                return error_response(500, "Unexpected error")
        else:
            return error_response(400, "Command missing")
    except:
        return error_response(400, "Bad request")


@blueprint.route('/<container>/logs', methods=['GET'])
def get_container_logs(container):
    '''
    '''
    try:
        logs = container_backend.get_container_logs(container)
        return success_response(logs)
    except ContainerNotFoundError:
        return error_response(404, "Container not found")
    except IllegalContainerStateError:
        return error_response(412, "Container in illegal state for requested action")
    except ContainerBackendError:
        return error_response(500, "Unexpected container backend error")
    except NotImplementedError:
        return error_response(501, "Not implemented")
    except:
        return error_response(500, "Unexpected error")


@blueprint.route('/<container>/public_key', methods=['GET'])
def get_public_key(container):
    '''
    '''
    try:
        public_key = container_backend.exec_in_container(
            container,
            # TODO: magic string; depends on EncryptionService...
            "cat /etc/ssh/ssh_host_rsa_key.pub"
        )
        return success_response(public_key)
    except ContainerNotFoundError:
        return error_response(404, "Container not found")
    except IllegalContainerStateError:
        return error_response(412, "Container in illegal state for requested action")
    except ContainerBackendError:
        return error_response(500, "Unexpected container backend error")
    except NotImplementedError:
        return error_response(501, "Not implemented")
    except:
        return error_response(500, "Unexpected error")


@blueprint.route('/<container>/restart', methods=['POST'])
def restart_container(container):
    '''
    '''
    try:
        ret = container_backend.restart_container(container, force=True)
        return success_response(ret)
    except ContainerNotFoundError:
        return error_response(404, "Container not found")
    except IllegalContainerStateError:
        return error_response(412, "Container in illegal state for requested action")
    except ContainerBackendError:
        return error_response(500, "Unexpected container backend error")
    except NotImplementedError:
        return error_response(501, "Not implemented")
    except:
        return error_response(500, "Unexpected error")


@blueprint.route('/<container>/resume', methods=['POST'])
def resume_container(container):
    '''
    '''
    if not isinstance(container_backend, SuspendableContainerBackend):
        raise error_response(428, "Container backend does not support the resume operation")

    try:
        ret = container_backend.resume_container(container)
        return success_response(ret)
    except ContainerNotFoundError:
        return error_response(404, "Container not found")
    except IllegalContainerStateError:
        return error_response(412, "Container in illegal state for requested action")
    except ContainerBackendError:
        return error_response(500, "Unexpected container backend error")
    except NotImplementedError:
        return error_response(501, "Not implemented")
    except:
        return error_response(500, "Unexpected error")


@blueprint.route('/<container>/snapshots/<snapshot>/restore', methods=['POST'])
def restore_container_snapshots(container, snapshot):
    '''
    '''
    if not isinstance(container_backend, SnapshotableContainerBackend):
        return error_response(428, "The container backend has no built-in support for snapshots")

    try:
        ret = container_backend.restore_container_snapshot(container, snapshot)
        return success_response(ret)
    except ContainerSnapshotNotFoundError:
        return error_response(404, "Container snapshot not found")
    except ContainerNotFoundError:
        return error_response(404, "Container not found")
    except IllegalContainerStateError:
        return error_response(412, "Container in illegal state for requested action")
    except ContainerBackendError:
        return error_response(500, "Unexpected container backend error")
    except NotImplementedError:
        return error_response(501, "Not implemented")
    except:
        return error_response(500, "Unexpected error")


@blueprint.route('/<container>/snapshots/<snapshot>', methods=['DELETE'])
def delete_container_snapshots(container, snapshot):
    '''
    '''
    if not isinstance(container_backend, SnapshotableContainerBackend):
        return error_response(428, "The container backend has no built-in support for snapshots")

    try:
        ret = container_backend.delete_container_snapshot(container, snapshot)
        return success_response(ret)
    except ContainerSnapshotNotFoundError:
        return error_response(404, "Container snapshot not found")
    except ContainerNotFoundError:
        return error_response(404, "Container not found")
    except IllegalContainerStateError:
        return error_response(412, "Container in illegal state for requested action")
    except ContainerBackendError:
        return error_response(500, "Unexpected container backend error")
    except NotImplementedError:
        return error_response(501, "Not implemented")
    except:
        return error_response(500, "Unexpected error")


@blueprint.route('/<container>/snapshots/<snapshot>', methods=['GET'])
def get_container_snapshot(container, snapshot):
    '''
    '''
    if not isinstance(container_backend, SnapshotableContainerBackend):
        return error_response(428, "The container backend has no built-in support for snapshots")

    try:
        snapshot = container_backend.get_container_snapshot(container, snapshot)
        return success_response(snapshot)
    except ContainerSnapshotNotFoundError:
        return error_response(404, "Container snapshot not found")
    except ContainerNotFoundError:
        return error_response(404, "Container not found")
    except IllegalContainerStateError:
        return error_response(412, "Container in illegal state for requested action")
    except ContainerBackendError:
        return error_response(500, "Unexpected container backend error")
    except NotImplementedError:
        return error_response(501, "Not implemented")
    except:
        return error_response(500, "Unexpected error")


@blueprint.route('/<container>/snapshots', methods=['GET'])
def get_container_snapshots(container):
    '''
    '''
    if not isinstance(container_backend, SnapshotableContainerBackend):
        return error_response(428, "The container backend has no built-in support for snapshots")

    try:
        snapshots = container_backend.get_container_snapshots(container)
        return success_response(snapshots)
    except ContainerSnapshotNotFoundError:
        return error_response(404, "Container snapshot not found")
    except ContainerNotFoundError:
        return error_response(404, "Container not found")
    except IllegalContainerStateError:
        return error_response(412, "Container in illegal state for requested action")
    except ContainerBackendError:
        return error_response(500, "Unexpected container backend error")
    except NotImplementedError:
        return error_response(501, "Not implemented")
    except:
        return error_response(500, "Unexpected error")


@blueprint.route('/<container>/snapshots', methods=['POST'])
def create_container_snapshots(container):
    '''
    '''
    if not isinstance(container_backend, SnapshotableContainerBackend):
        return error_response(428, "The container backend has no built-in support for snapshots")

    try:
        specs = request.get_json(force=True).copy()
        try:
            snapshot = container_backend.create_container_snapshot(container, specs)
            return success_response(snapshot)
        except ContainerNotFoundError:
            return error_response(404, "Container not found")
        except IllegalContainerSpecificationError:
            return error_response(400, "Illegal specification for container snapshot creation")
        except IllegalContainerStateError:
            return error_response(412, "Container in illegal state for requested action")
        except ContainerBackendError:
            return error_response(500, "Unexpected container backend error")
        except NotImplementedError:
            return error_response(501, "Not implemented")
        except:
            return error_response(500, "Unexpected error")
    except:
        return error_response(400, "Bad request")


@blueprint.route('/<container>/start', methods=['POST'])
def start_container(container):
    '''
    '''
    try:
        spec = request.get_json(force=True).copy()
        spec.update({'identifier': container})  # TODO: no hard coding
        try:
            ret = container_backend.start_container(spec)
            return success_response(ret)
        except IllegalContainerSpecificationError:
            return error_response(400, "Illegal specification for container creation")
        except IllegalContainerStateError:
            return error_response(412, "Container in illegal state for requested action")
        except ContainerBackendError:
            return error_response(500, "Unexpected container backend error")
        except NotImplementedError:
            return error_response(501, "Not implemented")
        except:
            return error_response(500, "Unexpected error")
    except:
        return error_response(400, "Bad request")


@blueprint.route('/<container>/stop', methods=['POST'])
def stop_container(container):
    '''
    '''
    try:
        ret = container_backend.stop_container(container, force=True)
        return success_response(ret)
    except ContainerNotFoundError:
        return error_response(404, "Container not found")
    except IllegalContainerStateError:
        return error_response(412, "Container in illegal state for requested action")
    except ContainerBackendError:
        return error_response(500, "Unexpected container backend error")
    except NotImplementedError:
        return error_response(501, "Not implemented")
    except:
        return error_response(500, "Unexpected error")


@blueprint.route('/<container>/suspend', methods=['POST'])
def suspend_container(container):
    '''
    '''
    if not isinstance(container_backend, SuspendableContainerBackend):
        raise error_response(428, "Container backend does not support the suspend operation")

    try:
        ret = container_backend.suspend_container(container)
        return success_response(ret)
    except ContainerNotFoundError:
        return error_response(404, "Container not found")
    except IllegalContainerStateError:
        return error_response(412, "Container in illegal state for requested action")
    except ContainerBackendError:
        return error_response(500, "Unexpected container backend error")
    except NotImplementedError:
        return error_response(501, "Not implemented")
    except:
        return error_response(500, "Unexpected error")


@blueprint.route('/<container>', methods=['GET'])
def get_container(container):
    '''
    '''
    try:
        container = container_backend.get_container(container)
        return success_response(container)
    except ContainerNotFoundError:
        return error_response(404, "Container not found")
    except IllegalContainerStateError:
        return error_response(412, "Container in illegal state for requested action")
    except ContainerBackendError:
        return error_response(500, "Unexpected container backend error")
    except NotImplementedError:
        return error_response(501, "Not implemented")
    except:
        return error_response(500, "Unexpected error")


@blueprint.route('/<container>', methods=['DELETE'])
def delete_container(container):
    '''
    '''
    try:
        ret = container_backend.delete_container(container)
        return success_response(ret)
    except ContainerNotFoundError:
        return error_response(404, "Container not found")
    except IllegalContainerStateError:
        return error_response(412, "Container in illegal state for requested action")
    except ContainerBackendError:
        return error_response(500, "Unexpected container backend error")
    except NotImplementedError:
        return error_response(501, "Not implemented")
    except:
        return error_response(500, "Unexpected error")


@blueprint.route('', methods=['GET'])
def get_containers():
    '''
    '''
    try:
        containers = container_backend.get_containers()
        return success_response(containers)
    except ContainerBackendError:
        return error_response(500, "Unexpected container backend error")
    except NotImplementedError:
        return error_response(501, "Not implemented")
    except:
        return error_response(500, "Unexpected error")


@blueprint.route('', methods=['POST'])
def create_container():
    '''
    '''
    try:
        json = request.get_json(force=True).copy()
        try:
            container = container_backend.create_container(json)
            return success_response(container)
        except IllegalContainerSpecificationError:
            return error_response(400, "Illegal specification for container creation")
        except ContainerBackendError:
            return error_response(500, "Unexpected container backend error")
        except NotImplementedError:
            return error_response(501, "Not implemented")
        except:
            return error_response(500, "Unexpected error")
    except:
        return error_response(400, "Bad request")
