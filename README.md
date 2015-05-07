# ipynbsrv-hostapi

> Package containing the executable & library for the host API component.

## Synopsis

```bash
usage: ipynbsrv_hostapi [-h] [-d, --debug] [-l, --listen ADDRESS] [-p, --port PORT]

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           Run in debug mode.
  -l, --listen ADDRESS  The address to listne on.
  -p, --port PORT       The port to bind to.
```

## HTTP REST API Overview

| HTTP Method | Slug | Description |
|-------------|------|-------------|
| GET         | /containers | Returns a list of all containers the backend knows. |
| POST        | /containers | Creates a container as per the specification included in the POST body. |
| DELETE      | /containers/`<CT>` | Deletes the references container from the backend. |
| GET         | /containers/`<CT>` | Returns information about the requested container. |
| POST        | /containers/`<CT>`/clone | Creates a clone of an already existing container as per the specification from the request body. |
| POST        | /containers/`<CT>`/exec | Executes the command from the request body inside the container and returns its output. |
| GET         | /containers/`<CT>`/logs | Returns a list of log messages the container has produced. |
| GET         | /containers/`<CT>`/public_key | Returns the public RSA key of the container. |
| POST        | /containers/`<CT>`/restart | Restarts the container. |
| POST        | /containers/`<CT>`/resume | Resumes a suspended container. |
| POST        | /containers/`<CT>`/start | Starts the container. |
| POST        | /containers/`<CT>`/stop | Stops the running container. |
| POST        | /containers/`<CT>`/suspend | Suspends the container. |
| GET         | /containers/`<CT>`/snapshots | Returns a list of all snapshots for the given container. |
| POST        | /containers/`<CT>`/snapshots | Creates a new container snapshot for the container as per the specification in the request body. |
| DELETE      | /containers/`<CT>`/snapshots/`<SH>` | Deletes the referenced container snapshot from the container backend. |
| GET         | /containers/`<CT>`/snapshots/`<SH>` | Returns information about a single snapshot of the given container. |
| POST        | /containers/`<CT>`/snapshots/`<SH>`/restore | Restores the referenced container snapshot. |
| GET         | /containers/images | Returns a list of images the container backend can bootstrap containers from. |
| POST        | /containers/images | Creates a container image as per the specification included in the POST body. |
| DELETE      | /containers/images/`<IMG>` | Returns information about a single image. |
| GET         | /containers/images/`<IMG>` | Deletes the referenced image from the backend. |