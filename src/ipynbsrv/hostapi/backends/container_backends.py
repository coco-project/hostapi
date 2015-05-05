from ipynbsrv.contract.backends import (CloneableContainerBackend, ContainerBackendError,
                                        SnapshotableContainerBackend)
from docker import Client


class Docker(CloneableContainerBackend, SnapshotableContainerBackend):
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

    '''
    :inherit
    '''
    def clone_container(self, container, clone, **kwargs):
        pass

    '''
    :inherit
    '''
    def container_exists(self, container, **kwargs):
        containers = self.get_containers(only_running=False)
        return next((ct for ct in containers if ct['Id'] == container.get('identifier')), False)

    '''
    :inherit
    '''
    def container_is_running(self, container, **kwargs):
        if not self.container_exists(container):
            raise ContainerNotFoundError

        container = self.get_container(container)
        return container['Status'].startswith(Docker.RUNNING_IDENTIFIER)

    '''
    :inherit
    '''
    def container_snapshot_exists(self, container, name, **kwargs):
        raise NotImplemented

    '''
    :inherit
    '''
    def create_container(self, container, **kwargs):
        try:
            return self.client.create_container(
                name=container.get('name'),
                image=container.get('image'),
                command=container.get('command'),
                ports=container.get('ports'),
                volumes=container.get('volumes'),
                environment=container.get('env'),
                # TODO: other optional params
                detach=True
            )
        except Exception as ex:
            raise ContainerBackendError(ex)

    '''
    :inherit

    :param name: The snapshots name in required 'repository:tag' format.
    '''
    def create_container_snapshot(self, container, name, **kwargs):
        if not self.container_exists(container):
            raise ContainerNotFoundError
        if self.container_snapshot_exists(container, name):
            raise Exception("A snapshot with that name already exists for the given container")

        parts = name.split(':')
        if len(parts) != 2:
            raise ValueError("Illegal name. Must be in the form repository:tag")
        repository = parts[0]
        tag = parts[1]
        try:
            return self.client.commit(
                container=container.get('identifier'),
                repository=repository,
                tag=tag
            )
        except Exception as ex:
            raise ContainerBackendError(ex)

    '''
    :inherit

    :param force: If true, the container doesn't need to be stopped.
    '''
    def delete_container(self, container, **kwargs):
        if not self.container_exists(container):
            raise ContainerNotFoundError
        force = kwargs.get('force')
        if force is not True and self.container_is_running(container):
            raise IllegalContainerStateError

        try:
            return self.client.remove_container(container=container.get('identifier'), force=(force is True))
        except Exception as ex:
            raise ContainerBackendError(ex)

    '''
    :inherit
    '''
    def delete_container_snapshot(self, container, snapshot, **kwargs):
        if not self.container_exists(container):
            raise ContainerNotFoundError
        if self.container_snapshot_exists(container, snapshot):
            raise Exception("Container snapshot does not exist")
        raise NotImplemented

    '''
    :inherit
    '''
    def exec_in_container(self, container, cmd, **kwargs):
        if not self.container_exists(container):
            raise ContainerNotFoundError
        if not self.container_is_running(container):
            raise IllegalContainerStateError

        try:
            exec_id = self.client.exec_create(container=container.get('identifier'), cmd=cmd)
            return self.client.exec_start(exec_id=exec_id, stream=False)
        except Exception as ex:
            raise ContainerBackendError(ex)

    '''
    :inherit
    '''
    def get_container(self, container):
        if not self.container_exists(container):
            raise ContainerNotFoundError
        containers = self.get_containers(only_running=False)
        return next((ct for ct in containers if ct['Id'] == container.get('identifier')), None)

    '''
    :inherit

    :param timestamps: If true, the log messages timestamps are included.
    '''
    def get_container_logs(self, container, **kwargs):
        if not self.container_exists(container):
            raise ContainerNotFoundError

        timestamps = kwargs.get('timestamps')
        try:
            logs = self.client.logs(
                container=container.get('identifier'),
                stream=False,
                timestamps=(timestamps is True)
            )
            return filter(lambda x: len(x) > 0,  logs.split('\n'))
        except Exception as ex:
            raise ContainerBackendError(ex)

    '''
    :inherit
    '''
    def get_containers(self, only_running=False, **kwargs):
        try:
            return self.client.containers(all=(not only_running))
        except Exception as ex:
            raise ContainerBackendError(ex)

    '''
    :inherit
    '''
    def get_required_creation_fields(self):
        return [
            ('name', basestring),
            ('image', basestring),
            ('command', basestring)
        ]

    '''
    :inherit

    :param force: If true, kill the container if it doesn't want to stop.
    '''
    def restart_container(self, container, **kwargs):
        if not self.container_exists(container):
            raise ContainerNotFoundError

        force = kwargs.get('force')
        try:
            if force:
                return self.client.restart(container=container.get('identifier'), timeout=0)
            else:
                return self.client.restart(container=container.get('identifier'))
        except Exception as ex:
            raise ContainerBackendError(ex)

    '''
    :inherit
    '''
    def restore_container_snapshot(self, container, snapshot, **kwargs):
        raise NotImplementedError

    '''
    :inherit
    '''
    def start_container(self, container, **kwargs):
        pass

    '''
    :inherit

    :param force: If true, kill the container if it doesn't want to stop.
    '''
    def stop_container(self, container, **kwargs):
        if not self.container_exists(container):
            raise ContainerNotFoundError
        if not self.container_is_running(container):
            raise IllegalContainerStateError

        force = kwargs.get('force')
        try:
            if force:
                return self.client.stop(container=container.get('identifier'), timeout=0)
            else:
                return self.client.stop(container=container.get('identifier'))
        except Exception as ex:
            raise ContainerBackendError(ex)


class ContainerNotFoundError(ContainerBackendError):
    '''
    Error meant to be raised when an operation can not be performed
    because the container on which the method should act does not exist.
    '''

    def __init__(self, message=''):
        super(ContainerNotFoundError, self).__init__(message)


class IllegalContainerStateError(ContainerBackendError):
    '''
    Error meant to be raised when an operation can not be performed
    because the container on which the method should act is in an
    illegal state (e.g. exec method and the container is stopped).
    '''

    def __init__(self, message=''):
        super(IllegalContainerStateError, self).__init__(message)
