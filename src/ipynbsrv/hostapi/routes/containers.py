from flask import Blueprint, request
from ipynbsrv.hostapi.backends import DockerContainerBackend
from ipynbsrv.hostapi.routes.common import error_response, success_response

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
        return success_response(container_backend.exec_in_container(
            {'id': ct_id},
            request.form.get('cmd')
        ))
    except:
        return error_response(503, "Something went wrong")


@blueprint.route('/<ct_id>/logs', methods=['GET'])
def get_container_logs(ct_id):
    '''
    '''
    try:
        return success_response(container_backend.get_container_logs({
            'id': ct_id
        }))
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
        return success_response(container_backend.restart_container({
            'id': ct_id
        }))
    except:
        return error_response(503, "Something went wrong")


@blueprint.route('/<ct_id>/snapshot', methods=['POST'])
def snapshot_container(ct_id):
    '''
    '''
    try:
        return success_response(container_backend.snapshot_container(
            {'id': ct_id},
            request.form.get('name')
        ))
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
        return success_response(container_backend.stop_container({
            'id': ct_id
        }))
    except:
        return error_response(503, "Something went wrong")


@blueprint.route('/<ct_id>', methods=['GET'])
def get_container(ct_id):
    '''
    '''
    try:
        return success_response(container_backend.get_container({
            'id': ct_id
        }))
    except:
        return error_response(503, "Something went wrong")


@blueprint.route('/<ct_id>', methods=['DELETE'])
def delete_container(ct_id):
    '''
    '''
    try:
        return success_response(container_backend.delete_container({
            'id': ct_id
        }))
    except:
        return error_response(503, "Something went wrong")


@blueprint.route('', methods=['POST'])
def create_container():
    '''
    '''
    return "CREATE CONTAINER"


@blueprint.route('', methods=['GET'])
def get_containers():
    '''
    '''
    try:
        return success_response(container_backend.get_containers())
    except:
        return error_response(503, "Something failed")
