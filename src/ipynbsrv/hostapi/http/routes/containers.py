from flask import Blueprint, request
from ipynbsrv.contract.backends import *
from ipynbsrv.hostapi.backends.container_backends import Docker
from ipynbsrv.hostapi.http.routes.common import error_response, success_response
import rsa

'''
'''
blueprint = Blueprint('containers', __name__, url_prefix='/containers')
container_backend = Docker(version="1.18")


@blueprint.route('/<container>/clone', methods=['POST'])
def clone_container(container):
    '''
    '''
    return error_response(501, "Not implemented")


@blueprint.route('/<container>/exec', methods=['POST'])
def exec_in_container(container):
    '''
    Executes the command defined in 'command' within the container
    with the given identifier.
    '''
    try:
        command = request.get_json(force=True).get('command')
    except Exception as ex:
        return error_response(400, ex)
    else:
        if command:
            try:
                output = container_backend.exec_in_container(
                    container,
                    command
                )
            except ContainerNotFoundError:
                return error_response(404, "Container not found")
            except IllegalContainerStateError:
                return success_response(412, "Container in illegal state for requested action")
            except ContainerBackendError:
                return error_response(500, "Unexpected container backend error")
            except Exception as ex:
                return error_response(500, ex)
            else:
                return success_response(output)
        else:
            return error_response(400, "Command missing")


@blueprint.route('/<container>/logs', methods=['GET'])
def get_container_logs(container):
    '''
    Returns a list of log messages from the given container.
    '''
    try:
        logs = container_backend.get_container_logs(container)
    except ContainerNotFoundError:
        return error_response(404, "Container not found")
    except IllegalContainerStateError:
        return success_response(412, "Container in illegal state for requested action")
    except ContainerBackendError:
        return error_response(500, "Unexpected container backend error")
    except Exception as ex:
        return error_response(500, ex)
    else:
        return success_response(logs)


@blueprint.route('/<container>/public_key', methods=['GET'])
def get_public_key(container):
    '''
    Returns the container's public key.
    '''
    try:
        public_key = container_backend.exec_in_container(
            container,
            # TODO: magic string; depends on EncryptionService...
            "cat /etc/ssh/ssh_host_rsa_key.pub"
        )
    except ContainerNotFoundError:
        return error_response(404, "Container not found")
    except IllegalContainerStateError:
        return success_response(412, "Container in illegal state for requested action")
    except ContainerBackendError:
        return error_response(500, "Unexpected container backend error")
    except Exception as ex:
        return error_response(500, ex)
    else:
        return success_response(public_key)


@blueprint.route('/<container>/restart', methods=['GET'])
def restart_container(container):
    '''
    Restarts or starts (if stopped) the container.
    '''
    try:
        feedback = container_backend.restart_container(container, force=True)
    except ContainerNotFoundError:
        return error_response(404, "Container not found")
    except IllegalContainerStateError:
        return success_response(412, "Container in illegal state for requested action")
    except ContainerBackendError:
        return error_response(500, "Unexpected container backend error")
    except Exception as ex:
        return error_response(500, ex)
    else:
        return success_response(feedback)


@blueprint.route('/<container>/start', methods=['POST'])
def start_container(container):
    '''
    Starts the container.
    '''
    try:
        json = request.get_json(force=True).copy()
    except:
        return error_response(400, "Bad request")
    else:
        # make sure the backend gets all the fields it wants
        spec = {'identifier': container}
        json.update(spec)
        for required_name, required_type in container_backend.get_required_start_fields():
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
            started = container_backend.start_container(spec)
        except ContainerBackendError:
            return error_response(500, "Unexpected container backend error")
        except Exception as ex:
            return error_response(500, ex)
        else:
            return success_response()


@blueprint.route('/<container>/stop', methods=['GET'])
def stop_container(container):
    '''
    Stops the container if it is running, does nothing otherwise.
    '''
    try:
        feedback = container_backend.stop_container(container, force=True)
    except ContainerNotFoundError:
        return error_response(404, "Container not found")
    except IllegalContainerStateError:
        return success_response(412, "Container in illegal state for requested action")
    except ContainerBackendError:
        return error_response(500, "Unexpected container backend error")
    except Exception as ex:
        return error_response(500, ex)
    else:
        return success_response(container)


@blueprint.route('/<container>', methods=['GET'])
def get_container(container):
    '''
    Returns information about the container.
    '''
    try:
        container = container_backend.get_container(container)
    except ContainerNotFoundError:
        return error_response(404, "Container not found")
    except IllegalContainerStateError:
        return success_response(412, "Container in illegal state for requested action")
    except ContainerBackendError:
        return error_response(500, "Unexpected container backend error")
    except Exception as ex:
        return error_response(500, ex)
    else:
        return success_response(container)


@blueprint.route('/<container>', methods=['DELETE'])
def delete_container(container):
    '''
    Deletes the container.

    Note: A running container needs to be stopped first.
    '''
    try:
        feedback = container_backend.delete_container(container)
    except ContainerNotFoundError as ex:
        return error_response(404, "Container not found")
    except IllegalContainerStateError:
        return success_response(412, "Container in illegal state for requested action")
    except ContainerBackendError:
        return error_response(500, "Unexpected container backend error")
    except:
        return error_response(500, "Something unexpected happened")
    else:
        return success_response(feedback)


@blueprint.route('', methods=['POST'])
def create_container():
    '''
    Creates a new container using the arguments from the request body.

    Note: There is no guarantee the created container is started after creation.
    '''
    try:
        json = request.get_json(force=True)
    except:
        return error_response(400, "Bad request")
    else:
        # make sure the backend gets all the fields it wants
        spec = {}
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
            created = container_backend.create_container(spec)
        except ContainerBackendError:
            return error_response(500, "Unexpected container backend error")
        except Exception as ex:
            return error_response(500, ex)
        else:
            return success_response(created)


@blueprint.route('', methods=['GET'])
def get_containers():
    '''
    Returns an array of all containers the backend knows.
    '''
    try:
        containers = container_backend.get_containers()
    except ContainerBackendError:
        return error_response(500, "Unexpected container backend error")
    except Exception as ex:
        return error_response(500, ex)
    else:
        return success_response(containers)
