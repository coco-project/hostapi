from ipynbsrv.contract.backends import (CloneableContainerBackend,
    ContainerBackendError, SnapshotableContainerBackend)
from docker import Client


class DockerContainerBackend(SnapshotableContainerBackend):
    '''
    '''

    '''
    String to identify either a container is running or stopped.
    '''
    RUNNING_IDENTIFIER = 'Up'

    '''
    Initializes a new Docker container backend.

    :param version: The Docker API version number.
    :param base_url: The URL or unix path to the Docker API endpoint.
    '''
    def __init__(self, version, base_url='unix://var/run/docker.sock'):
        self.client = Client(base_url=base_url, version=version)

    def container_exists(self, container):
        containers = self.get_containers(only_running=False)
        for returned in containers:
            if container.id == returned['Id']:
                return True
        return False

    def container_is_running(self, container):
        if not self.container_exists(container):
            raise ValueError("Container does not exist")

        container = self.get_container(container)
        return container['Status'].startswith(DockerContainerBackend.RUNNING_IDENTIFIER)

    def container_snapshot_exists(self, container, name):
        raise NotImplemented

    def create_container(self, container):
        # TODO: check if such a container already exists
        return self.client.create_container(
            name=container.name,
            image=container.image.get_full_identifier(),
            command=container.command,
            ports=container.ports,
            volumes=container.volumes,
            environment=container.env,
            detach=True
        )

    def create_container_snapshot(self, container, name):
        if not self.container_exists(container):
            raise ValueError("Container does not exist")
        if not name or not isinstance(name, str):
            raise ValueError("No snapshot name defined or not a str")
        # TODO: check if snapshot with that name and tag already exists
        parts = name.split(':')
        if len(parts) != 2:
            raise ValueError("Illegal name. Must be in the form repository:tag")

        repository = parts[0]
        tag = parts[1]
        try:
            return self.client.commit(
                container=container.id,
                repository=repository,
                tag=tag
            )
        except Exception as ex:
            raise ContainerBackendError(ex)

    def delete_container(self, container, force=False):
        if not self.container_exists(container):
            raise ValueError("Container does not exist")
        if self.container_is_running(container) and not force:
            raise ValueError("Container running but delete not forced")

        try:
            return self.client.remove_container(container=container.id, force=force)
        except Exception as ex:
            raise ContainerBackendError(ex)

    def delete_container_snapshot(self, container, snapshot):
        if self.container_snapshot_exists(container, snapshot):
            raise ValueError("Container snapshot does not exist")
        raise NotImplemented

    def exec_in_container(self, container, cmd):
        if not self.container_exists(container):
            raise ValueError("Container does not exist")
        if not self.container_is_running(container):
            raise ValueError("Container not running")

        try:
            exec_id = self.client.exec_create(container=container.id, cmd=cmd)
            return self.client.exec_start(exec_id=exec_id, stream=False)
        except Exception as ex:
            raise ContainerBackendError(ex)

    def get_container(self, container):
        if not self.container_exists(container):
            raise ValueError("Container does not exist")

        containers = self.get_containers(only_running=False)
        for returned in containers:
            if container.id == returned['Id']:
                return returned

    def get_container_logs(self, container):
        if not self.container_exists(container):
            raise ValueError("Container does not exist")

        try:
            logs = self.client.logs(container=container.id, stream=False, timestamps=True)
            return filter(lambda x: len(x) > 0,  logs.split('\n'))
        except Exception as ex:
            raise ContainerBackendError(ex)

    def get_containers(self, only_running=False):
        try:
            return self.client.containers(all=not only_running)
        except Exception as ex:
            raise ContainerBackendError(ex)

    def restart_container(self, container, force=False):
        if not self.container_exists(container):
            raise ValueError("Container does not exist")

        try:
            if force:
                return self.client.restart(container=container.id, timeout=0)
            else:
                return self.client.restart(container=container.id)
        except Exception as ex:
            raise ContainerBackendError(ex)

    def restore_container_snapshot(self, container, snapshot):
        raise NotImplementedError

    def start_container(self, container):
        pass

    def stop_container(self, container, force=False):
        if not self.container_exists(container):
            raise ValueError("Container does not exist")
        if not self.container_is_running(container):
            raise ValueError("Container not running")

        try:
            if force:
                return self.client.stop(container=container.id, timeout=0)
            else:
                return self.client.stop(container=container.id)
        except Exception as ex:
            raise ContainerBackendError(ex)
