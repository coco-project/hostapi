from flask import Blueprint, jsonify, request
from ipynbsrv.contract.dtos import ContainerDTO, ContainerImageDTO, CreatableContainerDTO
from ipynbsrv.hostapi.backends import DockerContainerBackend
from ipynbsrv.hostapi.routes.common import error_response, success_response
import time

'''
'''
blueprint = Blueprint('name', __name__, url_prefix='/containers')
container_backend = DockerContainerBackend(version="1.18")


@blueprint.route('/<ct_id>/clone', methods=['POST'])
def clone_container(ct_id):
    '''
    '''
    return "CLONE CONTAINER"


@blueprint.route('/<ct_id>/exec', methods=['POST'])
def exec_in_container(ct_id):
    '''
    '''
    try:
        container = ContainerDTO({'id': ct_id})
        container.is_valid():
            return success_response(container_backend.exec_in_container(
                container,
                request.get_json().get('command')
            ))
        else:
            return error_response(503, "Invalid date received")
    except:
        return error_response(503, "Something went wrong")


@blueprint.route('/<ct_id>/logs', methods=['GET'])
def get_container_logs(ct_id):
    '''
    '''
    try:
        container = ContainerDTO({'id': ct_id})
        container.is_valid():
            return success_response(container_backend.get_container_logs(container))
        else:
            return error_response(503, "Invalid date received")
    except:
        return error_response(503, "Something went wrong")


@blueprint.route('/<ct_id>/public_key', methods=['GET'])
def get_public_key(ct_id):
    '''
    '''
    return "PUBLIC KEY CONTAINER"


@blueprint.route('/<ct_id>/restart', methods=['GET'])
def restart_container(ct_id):
    '''
    '''
    try:
        container = ContainerDTO({'id': ct_id})
        if container.is_valid():
            return success_response(container_backend.restart_container(container))
        else:
            return error_response(503, "Invalid date received")
    except:
        return error_response(503, "Something went wrong")


@blueprint.route('/<ct_id>/snapshots', methods=['GET'])
def get_container_snapshots(ct_id):
    '''
    '''
    try:
        container = ContainerDTO({'id': ct_id})
        if container.is_valid():
            return success_response(container_backend.create_container_snapshot(
                container,
                request.get_json().get('name')
            ))
        else:
            return error_response(503, "Invalid date received")
    except:
        return error_response(503, "Something went wrong")


@blueprint.route('/<ct_id>/snapshots', methods=['POST'])
def create_container_snapshot(ct_id):
    '''
    '''
    try:
        container = ContainerDTO({'id': ct_id})
        if container.is_valid():
            return success_response(container_backend.create_container_snapshot(
                container,
                request.get_json().get('name')
            ))
        else:
            return error_response(503, "Invalid date received")
    except:
        return error_response(503, "Something went wrong")


@blueprint.route('/<ct_id>/start', methods=['POST'])
def start_container(ct_id):
    '''
    '''
    return "START CONTAINER"


@blueprint.route('/<ct_id>/stop', methods=['GET'])
def stop_container(ct_id):
    '''
    '''
    try:
        container = ContainerDTO({'id': ct_id})
        if container.is_valid():
            return success_response(container_backend.stop_container(container))
        else:
            return error_response(503, "Invalid date received")
    except:
        return error_response(503, "Something went wrong")


@blueprint.route('/<ct_id>', methods=['GET'])
def get_container(ct_id):
    '''
    '''
    try:
        container = ContainerDTO({'id': ct_id})
        if container.is_valid():
            return success_response(container_backend.get_container(container))
        else:
            return error_response(503, "Invalid date received")
    except:
        return error_response(503, "Something went wrong")


@blueprint.route('/<ct_id>', methods=['DELETE'])
def delete_container(ct_id):
    '''
    '''
    try:
        container = ContainerDTO({'id': ct_id})
        if container.is_valid():
            return success_response(container_backend.delete_container(container))
        else:
            return error_response(503, "Invalid date received")
    except:
        return error_response(503, "Something went wrong")


@blueprint.route('', methods=['POST'])
def create_container():
    '''
    '''
    try:
        json = request.get_json()
        json['image'] = ContainerImageDTO(json.get('image'))
        container = CreatableContainerDTO(json)
        if container.is_valid():
            created = container_backend.create_container(container)
            # TODO: return created container
            return success_response()
        else:
            return error_response(503, "Invalid input data")
    except:
        return error_response(503, "Something went wrong")


@blueprint.route('', methods=['GET'])
def get_containers():
    '''
    Returns an array of all containers the backend knows.
    '''
    try:
        containers = container_backend.get_containers()
        return success_response(containers)
    except:
        return error_response(503, "Something failed")
