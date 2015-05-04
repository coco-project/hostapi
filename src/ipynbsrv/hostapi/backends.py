from ipynbsrv.contract.backends import CloneableContainerBackend, CommitableContainerBackend
from docker import Client

'''
'''
class DockerContainerBackend(CloneableContainerBackend, CommitableContainerBackend):
    '''
    Initialites a new Docker container backend.

    :param base_url: The URL or unix path to the Docker API endpoint.
    :param version: The Docker API version number.
    '''
    def __init__(self, version, base_url='unix://var/run/docker.sock'):
        self.client = Client(base_url=base_url, version=version)

    def clone_container(self, container):
        raise NotImplementedError

    def commit_container(self, container):
        raise NotImplementedError

    def container_status(self, container):
        raise NotImplementedError

    def container_is_running(self, container):
        raise NotImplementedError

    def create_container(self, container):
        raise NotImplementedError

    def delete_container(self, container, force=False):
        raise NotImplementedError

    def restart_container(self, container):
        self.stop(force=force)
        self.start()

    def start_container(self, container):
        raise NotImplementedError

    def stop_container(self, container, force=False):
        raise NotImplementedError
