from base64 import standard_b64decode
from coco.contract.backends import *
from coco.contract.errors import *
from coco.hostapi import config
from coco.hostapi.http.responses import *
from flask import Blueprint, request, url_for


"""
Flask blueprint collecting the /containers routes.
"""
blueprint = Blueprint('containers', __name__, url_prefix='/containers')


@blueprint.route('/images/<image>', methods=['DELETE'])
def delete_container_image(image):
    """
    Delete the referenced image from the backend.
    """
    try:
        config.container_backend.delete_container_image(standard_b64decode(image))
        return success_no_content()
    except ContainerImageNotFoundError:
        return error_not_found("Container image not found")
    except ContainerBackendError:
        return error_unexpected_error("Unexpected backend error")
    except NotImplementedError:
        return error_not_implemented()
    except:
        return error_unexpected_error()


@blueprint.route('/images/<image>', methods=['GET'])
def get_container_image(image):
    """
    Get information about a single image.
    """
    try:
        image = config.container_backend.get_container_image(standard_b64decode(image))
        return success_ok(image)
    except ContainerImageNotFoundError:
            return error_not_found("Container image not found")
    except ContainerBackendError:
        return error_unexpected_error("Unexpected backend error")
    except NotImplementedError:
        return error_not_implemented()
    except:
        return error_unexpected_error()


@blueprint.route('/images', methods=['GET'])
def get_container_images():
    """
    Get a list of images the container backend can bootstrap containers from.
    """
    try:
        images = config.container_backend.get_container_images()
        return success_ok(images)
    except ContainerBackendError:
        return error_unexpected_error("Unexpected backend error")
    except NotImplementedError:
        return error_not_implemented()
    except:
        return error_unexpected_error()


@blueprint.route('/images', methods=['POST'])
def create_container_image():
    """
    Create a container image as per the specification included in the POST body.
    """
    try:
        json = request.get_json(force=True).copy()
        try:
            image = config.container_backend.create_container_image(**json)
            return success_created(image, url_for('.get_container_image', image=image))
        except ContainerBackendError:
            return error_unexpected_error("Unexpected backend error")
        except NotImplementedError:
            return error_not_implemented()
        except:
            return error_unexpected_error()
    except:
        return error_bad_request()


@blueprint.route('/snapshots/<snapshot>', methods=['DELETE'])
def delete_container_snapshots(snapshot):
    """
    Delete the referenced container snapshot from the container backend.
    """
    if not isinstance(config.container_backend, SnapshotableContainerBackend):
        return error_precondition_required("Snapshotable backend required")

    try:
        config.container_backend.delete_container_snapshot(standard_b64decode(snapshot))
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


@blueprint.route('/snapshots/<snapshot>', methods=['GET'])
def get_container_snapshot(snapshot):
    """
    Get information about a single snapshot.
    """
    if not isinstance(config.container_backend, SnapshotableContainerBackend):
        return error_precondition_required("Snapshotable backend required")

    try:
        snapshot = config.container_backend.get_container_snapshot(standard_b64decode(snapshot))
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


@blueprint.route('/snapshots', methods=['GET'])
def get_container_snapshots():
    """
    Get a list of all containers' snapshots.
    """
    if not isinstance(config.container_backend, SnapshotableContainerBackend):
        return error_precondition_required("Snapshotable backend required")

    try:
        snapshots = config.container_backend.get_container_snapshots()
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


@blueprint.route('/<container>/exec', methods=['POST'])
def exec_in_container(container):
    """
    Execute the command from the request body inside the container and return its output.

    :param container: The container in which the command should be executed.
    :request_param command: The command to execute.
    """
    try:
        command = request.get_json(force=True).get('command')
        if command:
            try:
                output = config.container_backend.exec_in_container(
                    standard_b64decode(container),
                    command
                )
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


@blueprint.route('/<container>/logs', methods=['GET'])
def get_container_logs(container):
    """
    Get a list of log messages the container has produced.
    """
    try:
        logs = config.container_backend.get_container_logs(standard_b64decode(container))
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
    """
    Get the public RSA key of the container.

    TODO: hmmmm....
    """
    try:
        public_key = config.container_backend.exec_in_container(
            standard_b64decode(container),
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
    """
    Restart the container.
    """
    try:
        config.container_backend.restart_container(standard_b64decode(container))
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
    """
    Resume a suspended container.

    Note: Backends may have preconditions before this operation can be run.
    """
    if not isinstance(config.container_backend, SuspendableContainerBackend):
        return error_precondition_required("Suspendable backend required")

    try:
        config.container_backend.resume_container(standard_b64decode(container))
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
    """
    Restore the referenced container snapshot.

    Note: Backends may have preconditions before this operation can be run.
    """
    if not isinstance(config.container_backend, SnapshotableContainerBackend):
        return error_precondition_required("Snapshotable backend required")

    try:
        restored_snapshot = config.container_backend.restore_container_snapshot(
            standard_b64decode(container),
            standard_b64decode(snapshot)
        )
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


@blueprint.route('/<container>/snapshots', methods=['GET'])
def get_containers_snapshots(container):
    """
    Get a list of all snapshots for the given container.
    """
    if not isinstance(config.container_backend, SnapshotableContainerBackend):
        return error_precondition_required("Snapshotable backend required")

    try:
        snapshots = config.container_backend.get_containers_snapshots(standard_b64decode(container))
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
    """
    Create a new container snapshot for the container as per the specification in the request body.
    """
    if not isinstance(config.container_backend, SnapshotableContainerBackend):
        return error_precondition_required("Snapshotable backend required")

    try:
        json = request.get_json(force=True).copy()
        try:
            snapshot = config.container_backend.create_container_snapshot(
                standard_b64decode(container),
                **json
            )
            return success_created(snapshot, url_for('.get_container_snapshot', snapshot=snapshot))
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


@blueprint.route('/<container>/start', methods=['POST'])
def start_container(container):
    """
    Start the container.

    Note: Backends may have preconditions before this operation can be run.
    """
    try:
        try:
            config.container_backend.start_container(standard_b64decode(container))
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
    """
    Stop the running container.

    Note: Backends may have preconditions before this operation can be run.
    """
    try:
        config.container_backend.stop_container(standard_b64decode(container))
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
    """
    Suspend the container.

    Note: Backends may have preconditions before this operation can be run.
    """
    if not isinstance(config.container_backend, SuspendableContainerBackend):
        return error_precondition_required("Suspendable backend required")

    try:
        config.container_backend.suspend_container(standard_b64decode(container))
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
    """
    Get information about the requested container.
    """
    try:
        container = config.container_backend.get_container(standard_b64decode(container))
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
    """
    Delete the referenced container from the backend.
    """
    try:
        config.container_backend.delete_container(standard_b64decode(container))
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
    """
    Get a list of all containers the backend knows.
    """
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
    """
    Create a container as per the specification included in the POST body.

    Note: There is no guarantee the created container is started/stopped after the
    operation has completed.
    """
    try:
        json = request.get_json(force=True).copy()
        try:
            container = config.container_backend.create_container(**json)
            return success_created(container, url_for('.get_container', container=container))
        except ContainerBackendError:
            return error_unexpected_error("Unexpected backend error")
        except NotImplementedError:
            return error_not_implemented()
        except:
            return error_unexpected_error()
    except:
        return error_bad_request()
