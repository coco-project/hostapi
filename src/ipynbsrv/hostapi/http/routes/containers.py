from flask import Blueprint, request
from ipynbsrv.hostapi.backends import DockerContainerBackend
from ipynbsrv.hostapi.http.routes.common import error_response, success_response

'''
'''
blueprint = Blueprint('name', __name__, url_prefix='/containers')
container_backend = DockerContainerBackend(version="1.18")


@blueprint.route('/<identifier>/clone', methods=['POST'])
def clone_container(identifier):
    '''
    '''
    return error_response(501, "Not implemented")


@blueprint.route('/<identifier>/exec', methods=['POST'])
def exec_in_container(identifier):
    '''
    Executes the command defined in 'command' within the container
    with the given ID.
    '''
    command = request.get_json().get('command')
    if command:
        container = {'identifier': identifier}
        if container_backend.container_exists(container):
            if container_backend.container_is_running(container):
                try:
                    return success_response(container_backend.exec_in_container(
                        {'identifier': identifier},
                        command
                    ))
                except:
                    return error_response(500, "Unexpected container backend error")
            else:
                return error_response(412, "Container not running")
        else:
            return error_response(404, "Container not found")
    else:
        return error_response(400, "Command missing")


@blueprint.route('/<identifier>/logs', methods=['GET'])
def get_container_logs(identifier):
    '''
    Returns a list of log messages from the given container.
    '''
    container = {'identifier': identifier}
    if container_backend.container_exists(container):
        try:
            return success_response(container_backend.get_container_logs(container))
        except:
            return error_response(500, "Unexpected container backend error")
    else:
        return error_response(404, "Container not found")


@blueprint.route('/<identifier>/public_key', methods=['GET'])
def get_public_key(identifier):
    '''
    Returns the container's public key.
    '''
    container = {'identifier': identifier}
    if container_backend.container_exists(container):
        if container_backend.container_is_running(container):
            try:
                return success_response(container_backend.exec_in_container(
                    container,
                    # TODO: magic string; depends on EncryptionService...
                    "cat /etc/ssh/ssh_host_rsa_key.pub"
                ))
            except:
                return error_response(500, "Unexpected container backend error")
        else:
            return error_response(412, "Container not running")
    else:
        return error_response(404, "Container not found")


@blueprint.route('/<identifier>/restart', methods=['GET'])
def restart_container(identifier):
    '''
    Restarts or starts (if stopped) the container.
    '''
    container = {'identifier': identifier}
    if container_backend.container_exists(container):
        try:
            return success_response(container_backend.restart_container(container, force=True))
        except:
            return error_response(500, "Unexpected container backend error")
    else:
        return error_response(404, "Container not found")


# TODO: DELETE, POST and <snapshot> routes
@blueprint.route('/<identifier>/snapshots', methods=['GET'])
def get_container_snapshots(identifier):
    '''
    Returns a list of snapshots for the container.
    '''
    container = {'identifier': identifier}
    if container_backend.container_exists(container):
        try:
            return success_response(container_backend.get_container_snapshots(container))
        except:
            return error_response(500, "Unexpected container backend error")
    else:
        return error_response(404, "Container not found")


@blueprint.route('/<identifier>/start', methods=['POST'])
def start_container(identifier):
    '''
    Starts the container.
    '''
    return error_response(501, "Not implemented")


@blueprint.route('/<identifier>/stop', methods=['GET'])
def stop_container(identifier):
    '''
    Stops the container if it is running, does nothing otherwise.
    '''
    container = {'identifier': identifier}
    if container_backend.container_exists(container):
        if container_backend.container_is_running(container):
            try:
                return success_response(container_backend.get_container_snapshots(container))
            except:
                return error_response(500, "Unexpected container backend error")
        else:
            return success_response("Container already stopped")
    else:
        return error_response(404, "Container not found")


@blueprint.route('/<identifier>', methods=['GET'])
def get_container(identifier):
    '''
    Returns information about the container.
    '''
    container = {'identifier': identifier}
    if container_backend.container_exists(container):
        try:
            return success_response(container_backend.get_container(container))
        except:
            return error_response(500, "Unexpected container backend error")
    else:
        return error_response(404, "Container not found")


@blueprint.route('/<identifier>', methods=['DELETE'])
def delete_container(identifier):
    '''
    Deletes the container.

    Note: A running container needs to be stopped first.
    '''
    container = {'identifier': identifier}
    if container_backend.container_exists(container):
        if not container_backend.container_is_running(container):
            try:
                return success_response(container_backend.delete_container(container, force=True))
            except:
                return error_response(500, "Unexpected container backend error")
        else:
            return success_response(412, "Container not stopped")
    else:
        return error_response(404, "Container not found")


@blueprint.route('', methods=['POST'])
def create_container():
    '''
    Creates a new container using the arguments from the request body.

    Note: There is no guarantee the created container is started after creation.
    '''
    json = request.get_json()
    spec = {}  # create_container input
    for required_name, required_type in container_backend.get_required_creation_fields():
        field = json.get(required_name)
        if not field:
            return error_response(400, "Missing required field %s" % required_name)
        elif not isinstance(field, required_type):
            return error_response(
                400,
                "Bad input type for field %s. %s expected, %s given." % (required_name, required_type, type(field))
            )
        else:
            spec[required_name] = field

    try:
        return success_response(container_backend.create_container(spec))
    except:
        return error_response(500, "Unexpected container backend error")


@blueprint.route('', methods=['GET'])
def get_containers():
    '''
    Returns an array of all containers the backend knows.
    '''
    try:
        containers = container_backend.get_containers()
        return success_response(containers)
    except:
        return error_response(500, "Unexpected container backend error")
