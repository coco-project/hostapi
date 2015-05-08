from flask import Blueprint, make_response, request, url_for
from ipynbsrv.contract.backends import *
from ipynbsrv.hostapi import config
from ipynbsrv.hostapi.http.responses import *

'''
'''
blueprint = Blueprint('containers', __name__, url_prefix='/containers')


@blueprint.route('/<container>/clone', methods=['POST'])
def clone_container(container):
    '''
    Creates a clone of an already existing container as per the specification from the request body.

    TODO: hmm.....
    '''
    if not isinstance(config.container_backend, CloneableContainerBackend):
        return error_precondition_required("Cloneable backend required")

    return error_not_implemented()


@blueprint.route('/<container>/exec', methods=['POST'])
def exec_in_container(container):
    '''
    Executes the command from the request body inside the container and returns its output.
    '''
    try:
        command = request.get_json(force=True).get('command')
        if command:
            try:
                output = config.container_backend.exec_in_container(container, command)
                return success_ok(output)
            except ContainerNotFoundError:
                return error_not_found("Container not found")
            except IllegalContainerStateError:
                return error_precondition_failed("Container in illegal state for requested action")
            except ContainerBackendError:
                return error_unexpected_error("Unexpected backend error")
            except NotImplementedError:
                return error_not_implemented()
            except:
                return error_unexpected_error()
        else:
            return error_unprocessable_entity("Command missing")
    except:
        return error_bad_request()


@blueprint.route('/images/<image>', methods=['GET'])
def get_image(image):
    '''
    Returns information about a single image.

    Note: If the backend does not support images, a precondition required error is returned.
    '''
    if not isinstance(config.container_backend, ImageBasedContainerBackend):
        return error_precondition_required("Image based backend required")

    try:
        image = config.container_backend.get_image(image)
        return success_ok(image)
    except ContainerImageNotFoundError:
            return error_not_found("Container image not found")
    except ContainerBackendError:
        return error_unexpected_error("Unexpected backend error")
    except NotImplementedError:
        return error_not_implemented()
    except:
        return error_unexpected_error()


@blueprint.route('/images/<image>', methods=['DELETE'])
def delete_image(image):
    '''
    Deletes the referenced image from the backend.

    Note: If the backend does not support images, a precondition required error is returned.
    '''
    if not isinstance(config.container_backend, ImageBasedContainerBackend):
        return error_precondition_required("Image based backend required")

    try:
        config.container_backend.delete_image(image)
        return success_no_content()
    except ContainerImageNotFoundError:
        return error_not_found("Container image not found")
    except ContainerBackendError:
        return error_unexpected_error("Unexpected backend error")
    except NotImplementedError:
        return error_not_implemented()
    except:
        return error_unexpected_error()


@blueprint.route('/images', methods=['GET'])
def get_images():
    '''
    Returns a list of images the container backend can bootstrap containers from.

    Note: If the backend does not support images, a precondition required error is returned.
    '''
    if not isinstance(config.container_backend, ImageBasedContainerBackend):
        return error_precondition_required("Image based backend required")

    try:
        images = config.container_backend.get_images()
        return success_ok(images)
    except ContainerBackendError:
        return error_unexpected_error("Unexpected backend error")
    except NotImplementedError:
        return error_not_implemented()
    except:
        return error_unexpected_error()


@blueprint.route('/images', methods=['POST'])
def create_image():
    '''
    Creates a container image as per the specification included in the POST body.
    '''
    if not isinstance(config.container_backend, ImageBasedContainerBackend):
        return error_precondition_required("Image based backend required")

    try:
        json = request.get_json(force=True).copy()
        try:
            image_pk = config.container_backend.create_image(json)
            return success_created(image_pk, url_for('.get_image', image=image_pk))
        except IllegalContainerSpecificationError:
            return error_unprocessable_entity("Invalid image specification")
        except ContainerBackendError:
            return error_unexpected_error("Unexpected backend error")
        except NotImplementedError:
            return error_not_implemented()
        except:
            return error_unexpected_error()
    except:
        return error_bad_request()


@blueprint.route('/<container>/logs', methods=['GET'])
def get_container_logs(container):
    '''
    Returns a list of log messages the container has produced.
    '''
    try:
        logs = config.container_backend.get_container_logs(container)
        return success_ok(logs)
    except ContainerNotFoundError:
        return error_not_found("Container not found")
    except IllegalContainerStateError:
        return error_precondition_failed("Container in illegal state for requested action")
    except ContainerBackendError:
        return error_unexpected_error("Unexpected backend error")
    except NotImplementedError:
        return error_not_implemented()
    except:
        return error_unexpected_error()


@blueprint.route('/<container>/public_key', methods=['GET'])
def get_public_key(container):
    '''
    Returns the public RSA key of the container.

    TODO: hmmmm....
    '''
    try:
        public_key = config.container_backend.exec_in_container(
            container,
            # TODO: magic string; depends on EncryptionService...
            "cat /etc/ssh/ssh_host_rsa_key.pub"
        )
        return success_ok(public_key)
    except ContainerNotFoundError:
        return error_not_found("Container not found")
    except IllegalContainerStateError:
        return error_precondition_failed("Container in illegal state for requested action")
    except ContainerBackendError:
        return error_unexpected_error("Unexpected backend error")
    except NotImplementedError:
        return error_not_implemented()
    except:
        return error_unexpected_error()


@blueprint.route('/<container>/restart', methods=['POST'])
def restart_container(container):
    '''
    Restarts the container.
    '''
    try:
        config.container_backend.restart_container(container, force=True)
        return success_no_content()
    except ContainerNotFoundError:
        return error_not_found("Container not found")
    except IllegalContainerStateError:
        return error_precondition_failed("Container in illegal state for requested action")
    except ContainerBackendError:
        return error_unexpected_error("Unexpected backend error")
    except NotImplementedError:
        return error_not_implemented()
    except:
        return error_unexpected_error()


@blueprint.route('/<container>/resume', methods=['POST'])
def resume_container(container):
    '''
    Resumes a suspended container.

    Note: Backends may have preconditions before this operation can be run.
    '''
    if not isinstance(config.container_backend, SuspendableContainerBackend):
        return error_precondition_required("Suspendable backend required")

    try:
        config.container_backend.resume_container(container)
        return success_no_content()
    except ContainerNotFoundError:
        return error_not_found("Container not found")
    except IllegalContainerStateError:
        return error_precondition_failed("Container in illegal state for requested action")
    except ContainerBackendError:
        return error_unexpected_error("Unexpected backend error")
    except NotImplementedError:
        return error_not_implemented()
    except:
        return error_unexpected_error()


@blueprint.route('/<container>/snapshots/<snapshot>/restore', methods=['POST'])
def restore_container_snapshots(container, snapshot):
    '''
    Restores the referenced container snapshot.

    Note: Backends may have preconditions before this operation can be run.
    '''
    if not isinstance(config.container_backend, SnapshotableContainerBackend):
        return error_precondition_required("Snapshotable backend required")

    try:
        restored_snapshot = config.container_backend.restore_container_snapshot(container, snapshot)
        return success_ok(restored_snapshot)
    except ContainerNotFoundError:
        return error_not_found("Container not found")
    except ContainerSnapshotNotFoundError:
        return error_not_found("Container snapshot not found")
    except IllegalContainerStateError:
        return error_precondition_failed("Container in illegal state for requested action")
    except ContainerBackendError:
        return error_unexpected_error("Unexpected backend error")
    except NotImplementedError:
        return error_not_implemented()
    except:
        return error_unexpected_error()


@blueprint.route('/<container>/snapshots/<snapshot>', methods=['DELETE'])
def delete_container_snapshots(container, snapshot):
    '''
    Deletes the referenced container snapshot from the container backend.

    Note: If the backend does not snapshots, a precondition required error is returned.
    '''
    if not isinstance(config.container_backend, SnapshotableContainerBackend):
        return error_precondition_required("Snapshotable backend required")

    try:
        config.container_backend.delete_container_snapshot(container, snapshot)
        return success_no_content()
    except ContainerNotFoundError:
        return error_not_found("Container not found")
    except ContainerSnapshotNotFoundError:
        return error_not_found("Container snapshot not found")
    except IllegalContainerStateError:
        return error_precondition_failed("Container in illegal state for requested action")
    except ContainerBackendError:
        return error_unexpected_error("Unexpected backend error")
    except NotImplementedError:
        return error_not_implemented()
    except:
        return error_unexpected_error()


@blueprint.route('/<container>/snapshots/<snapshot>', methods=['GET'])
def get_container_snapshot(container, snapshot):
    '''
    Returns information about a single snapshot of the given container.

    Note: If the backend does not snapshots, a precondition required error is returned.
    '''
    if not isinstance(config.container_backend, SnapshotableContainerBackend):
        return error_precondition_required("Snapshotable backend required")

    try:
        snapshot = config.container_backend.get_container_snapshot(container, snapshot)
        return success_ok(snapshot)
    except ContainerNotFoundError:
        return error_not_found("Container not found")
    except ContainerSnapshotNotFoundError:
        return error_not_found("Container snapshot not found")
    except ContainerBackendError:
        return error_unexpected_error("Unexpected backend error")
    except NotImplementedError:
        return error_not_implemented()
    except:
        return error_unexpected_error()


@blueprint.route('/<container>/snapshots', methods=['GET'])
def get_container_snapshots(container):
    '''
    Returns a list of all snapshots for the given container.

    Note: If the backend does not snapshots, a precondition required error is returned.
    '''
    if not isinstance(config.container_backend, SnapshotableContainerBackend):
        return error_precondition_required("Snapshotable backend required")

    try:
        snapshots = config.container_backend.get_container_snapshots(container)
        return success_ok(snapshots)
    except ContainerNotFoundError:
        return error_not_found("Container not found")
    except ContainerSnapshotNotFoundError:
        return error_not_found("Container snapshot not found")
    except ContainerBackendError:
        return error_unexpected_error("Unexpected backend error")
    except NotImplementedError:
        return error_not_implemented()
    except:
        return error_unexpected_error()


@blueprint.route('/<container>/snapshots', methods=['POST'])
def create_container_snapshot(container):
    '''
    Creates a new container snapshot for the container as per the specification in the request body.

    Note: If the backend does not snapshots, a precondition required error is returned.
    '''
    if not isinstance(config.container_backend, SnapshotableContainerBackend):
        return error_precondition_required("Snapshotable backend required")

    try:
        specs = request.get_json(force=True).copy()
        try:
            snapshot_pk = config.container_backend.create_container_snapshot(container, specs)
            return success_created(snapshot_pk, url_for('.get_container_snapshot', container=container, snapshot=snapshot_pk))
        except ContainerNotFoundError:
            return error_not_found("Container not found")
        except IllegalContainerSpecificationError:
            return error_unprocessable_entity("Invalid snapshot specification")
        except IllegalContainerStateError:
            return error_precondition_failed("Container in illegal state for requested action")
        except ContainerBackendError:
            return error_unexpected_error("Unexpected backend error")
        except NotImplementedError:
            return error_not_implemented()
        except:
            return error_unexpected_error()
    except:
        return error_bad_request()


@blueprint.route('/<container>/start', methods=['POST'])
def start_container(container):
    '''
    Starts the container.

    Note: Backends may have preconditions before this operation can be run.
    '''
    try:
        try:
            config.container_backend.start_container(container)
            return success_no_content()
        except ContainerNotFoundError:
            return error_not_found("Container not found")
        except IllegalContainerStateError:
            return error_precondition_failed("Container in illegal state for requested action")
        except ContainerBackendError:
            return error_unexpected_error("Unexpected backend error")
        except NotImplementedError:
            return error_not_implemented()
        except:
            return error_unexpected_error()
    except:
        return error_bad_request()


@blueprint.route('/<container>/stop', methods=['POST'])
def stop_container(container):
    '''
    Stops the running container.

    Note: Backends may have preconditions before this operation can be run.
    '''
    try:
        config.container_backend.stop_container(container, force=True)
        return success_no_content()
    except ContainerNotFoundError:
        return error_not_found("Container not found")
    except IllegalContainerStateError:
        return error_precondition_failed("Container in illegal state for requested action")
    except ContainerBackendError:
        return error_unexpected_error("Unexpected backend error")
    except NotImplementedError:
        return error_not_implemented()
    except:
        return error_unexpected_error()


@blueprint.route('/<container>/suspend', methods=['POST'])
def suspend_container(container):
    '''
    Suspends the container.

    Note: Backends may have preconditions before this operation can be run.
    '''
    if not isinstance(config.container_backend, SuspendableContainerBackend):
        return error_precondition_required("Suspendable backend required")

    try:
        config.container_backend.suspend_container(container)
        return success_no_content()
    except ContainerNotFoundError:
        return error_not_found("Container not found")
    except IllegalContainerStateError:
        return error_precondition_failed("Container in illegal state for requested action")
    except ContainerBackendError:
        return error_unexpected_error("Unexpected backend error")
    except NotImplementedError:
        return error_not_implemented()
    except:
        return error_unexpected_error()


@blueprint.route('/<container>', methods=['GET'])
def get_container(container):
    '''
    Returns information about the requested container.
    '''
    try:
        container = config.container_backend.get_container(container)
        return success_ok(container)
    except ContainerNotFoundError:
        return error_not_found("Container not found")
    except ContainerBackendError:
        return error_unexpected_error("Unexpected backend error")
    except NotImplementedError:
        return error_not_implemented()
    except:
        return error_unexpected_error()


@blueprint.route('/<container>', methods=['DELETE'])
def delete_container(container):
    '''
    Deletes the referenced container from the backend.
    '''
    try:
        config.container_backend.delete_container(container)
        return success_no_content()
    except ContainerNotFoundError:
        return error_not_found("Container not found")
    except IllegalContainerStateError:
        return error_precondition_failed("Container in illegal state for requested action")
    except ContainerBackendError:
        return error_unexpected_error("Unexpected backend error")
    except NotImplementedError:
        return error_not_implemented()
    except:
        return error_unexpected_error()


@blueprint.route('', methods=['GET'])
def get_containers():
    '''
    Returns a list of all containers the backend knows.
    '''
    try:
        containers = config.container_backend.get_containers()
        return success_ok(containers)
    except ContainerBackendError:
        return error_unexpected_error("Unexpected backend error")
    except NotImplementedError:
        return error_not_implemented()
    except:
        return error_unexpected_error()


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
            container_pk = config.container_backend.create_container(json)
            return success_created(container_pk, url_for('.get_container', container=container_pk))
        except IllegalContainerSpecificationError:
            return error_unprocessable_entity("Invalid container specification")
        except ContainerBackendError:
            return error_unexpected_error("Unexpected backend error")
        except NotImplementedError:
            return error_not_implemented()
        except:
            return error_unexpected_error()
    except:
        return error_bad_request()
