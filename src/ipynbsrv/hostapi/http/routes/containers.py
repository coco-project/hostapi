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
    Creates a clone of an already existing container as per the specification from the request body.

    TODO: hmm.....
    '''
    if not isinstance(container_backend, CloneableContainerBackend):
        return error_response(428, "Container backend does not support the clone operation")

    return error_response(501, "Not implemented")


@blueprint.route('/<container>/exec', methods=['POST'])
def exec_in_container(container):
    '''
    Executes the command from the request body inside the container and returns its output.
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


@blueprint.route('/images/<image>', methods=['GET'])
def get_image(image):
    '''
    Returns information about a single image.

    Note: If the backend does not support images, a precondition required error is returned.
    '''
    if not isinstance(container_backend, ImageBasedContainerBackend):
        return error_response(428, "Container backend is not image based")

    try:
        image = container_backend.get_image(image)
        return success_response(image)
    except ContainerImageNotFoundError:
        return error_response(404, "Container image not found")
    except ContainerBackendError:
        return error_response(500, "Unexpected container backend error")
    except NotImplementedError:
        return error_response(501, "Not implemented")
    except:
        return error_response(500, "Unexpected error")


@blueprint.route('/images/<image>', methods=['DELETE'])
def delete_image(image):
    '''
    Deletes the referenced image from the backend.

    Note: If the backend does not support images, a precondition required error is returned.
    '''
    if not isinstance(container_backend, ImageBasedContainerBackend):
        return error_response(428, "Container backend is not image based")

    try:
        ret = container_backend.delete_image(image)
        return success_response(ret)
    except ContainerImageNotFoundError:
        return error_response(404, "Container image not found")
    except ContainerBackendError:
        return error_response(500, "Unexpected container backend error")
    except NotImplementedError:
        return error_response(501, "Not implemented")
    except:
        return error_response(500, "Unexpected error")


@blueprint.route('/images', methods=['GET'])
def get_images():
    '''
    Returns a list of images the container backend can bootstrap containers from.

    Note: If the backend does not support images, a precondition required error is returned.
    '''
    if not isinstance(container_backend, ImageBasedContainerBackend):
        return error_response(428, "Container backend is not image based")

    try:
        images = container_backend.get_images()
        return success_response(images)
    except ContainerBackendError:
        return error_response(500, "Unexpected container backend error")
    except NotImplementedError:
        return error_response(501, "Not implemented")
    except:
        return error_response(500, "Unexpected error")


@blueprint.route('/<container>/logs', methods=['GET'])
def get_container_logs(container):
    '''
    Returns a list of log messages the container has produced.
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
    Returns the public RSA key of the container.

    TODO: hmmmm....
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
    Restarts the container.
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
    Resumes a suspended container.

    Note: Backends may have preconditions before this operation can be run.
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
    Restores the referenced container snapshot.

    Note: Backends may have preconditions before this operation can be run.
    '''
    if not isinstance(container_backend, SnapshotableContainerBackend):
        return error_response(428, "The container backend has no built-in support for snapshots")

    try:
        ret = container_backend.restore_container_snapshot(container, snapshot)
        return success_response(ret)
    except ContainerNotFoundError:
        return error_response(404, "Container not found")
    except ContainerSnapshotNotFoundError:
        return error_response(404, "Container snapshot not found")
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
    Deletes the referenced container snapshot from the container backend.

    Note: If the backend does not snapshots, a precondition required error is returned.
    '''
    if not isinstance(container_backend, SnapshotableContainerBackend):
        return error_response(428, "The container backend has no built-in support for snapshots")

    try:
        ret = container_backend.delete_container_snapshot(container, snapshot)
        return success_response(ret)
    except ContainerNotFoundError:
        return error_response(404, "Container not found")
    except ContainerSnapshotNotFoundError:
        return error_response(404, "Container snapshot not found")
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
    Returns information about a single snapshot of the given container.

    Note: If the backend does not snapshots, a precondition required error is returned.
    '''
    if not isinstance(container_backend, SnapshotableContainerBackend):
        return error_response(428, "The container backend has no built-in support for snapshots")

    try:
        snapshot = container_backend.get_container_snapshot(container, snapshot)
        return success_response(snapshot)
    except ContainerNotFoundError:
        return error_response(404, "Container not found")
    except ContainerSnapshotNotFoundError:
        return error_response(404, "Container snapshot not found")
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
    Returns a list of all snapshots for the given container.

    Note: If the backend does not snapshots, a precondition required error is returned.
    '''
    if not isinstance(container_backend, SnapshotableContainerBackend):
        return error_response(428, "The container backend has no built-in support for snapshots")

    try:
        snapshots = container_backend.get_container_snapshots(container)
        return success_response(snapshots)
    except ContainerNotFoundError:
        return error_response(404, "Container not found")
    except ContainerSnapshotNotFoundError:
        return error_response(404, "Container snapshot not found")
    except IllegalContainerStateError:
        return error_response(412, "Container in illegal state for requested action")
    except ContainerBackendError:
        return error_response(500, "Unexpected container backend error")
    except NotImplementedError:
        return error_response(501, "Not implemented")
    except:
        return error_response(500, "Unexpected error")


@blueprint.route('/<container>/snapshots', methods=['POST'])
def create_container_snapshot(container):
    '''
    Creates a new container snapshot for the container.

    Note: If the backend does not snapshots, a precondition required error is returned.
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
    Starts the container.

    Note: Backends may have preconditions before this operation can be run.
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
    Stops the running container.

    Note: Backends may have preconditions before this operation can be run.
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
    Suspends the container.

    Note: Backends may have preconditions before this operation can be run.
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
    Returns information about the requested container.
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
    Deletes the references container from the backend.
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
    Returns a list of all containers the backend knows of.
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
    Creates a container as per the specification included in the POST body.

    Note: There is no guarantee the created container is started/stopped after the
    operation has completed.
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
