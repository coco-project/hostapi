from flask import Blueprint

'''
'''
blueprint = Blueprint('name', __name__, url_prefix='/containers')


'''
'''
@blueprint.route('/<int:ct_id>/exec', methods=['POST'])
def exec_in_container(ct_id):
    return "EXEC CONTAINER"

'''
'''
@blueprint.route('/<int:ct_id>/clone', methods=['POST'])
def clone_container(ct_id):
    return "CLONE CONTAINER"

'''
'''
@blueprint.route('/<int:ct_id>/commit', methods=['POST'])
def commit_container(ct_id):
    return "COMMIT CONTAINER"

'''
'''
@blueprint.route('/<int:ct_id>/logs', methods=['GET'])
def get_container_logs(ct_id):
    return "GET CONTAINER LOGS"

'''
'''
@blueprint.route('/<int:ct_id>/public_key', methods=['GET'])
def get_public_key(ct_id):
    return "PUBLIC KEY CONTAINER"

'''
'''
@blueprint.route('/<int:ct_id>/restart', methods=['GET'])
def restart_container(ct_id):
    return "STOP CONTAINER"

'''
'''
@blueprint.route('/<int:ct_id>/start', methods=['GET'])
def start_container(ct_id):
    return "START CONTAINER"

'''
'''
@blueprint.route('/<int:ct_id>/stop', methods=['GET'])
def stop_container(ct_id):
    return "STOP CONTAINER"

'''
'''
@blueprint.route('/<int:ct_id>', methods=['GET'])
def get_container(ct_id):
    return "GET CONTAINER"

'''
'''
@blueprint.route('/<int:ct_id>', methods=['DELETE'])
def delete_container(ct_id):
    return "DELETE CONTAINER"

'''
'''
@blueprint.route('', methods=['POST'])
def create_container():
    return "CREATE CONTAINER"

'''
'''
@blueprint.route('', methods=['GET'])
def get_containers():
    return "GET CONTAINERS"
