# ipynbsrv-hostapi

> Package containing the executable & library for the host API component (a `ipynbsrv.backends.container_backends.HttpRemote` endpoint).

## Synopsis

```bash
usage: ipynbsrv_hostapi [-h] [-d]
                        [-l ADDRESS] [-p PORT]
                        [--container-backend CONTAINER_BACKEND]
                        [--container-backend-args CONTAINER_BACKEND_ARGS]

ipynbsrv host API CLI tool

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           run in debug mode

  -l ADDRESS, --listen ADDRESS
                        the address to listen on (default: 0.0.0.0)
  -p PORT, --port PORT  the port to bind to (default: 8080)

  --container-backend CONTAINER_BACKEND
                        absolute name of the container backend class to load
                        (default: ipynbsrv.backends.container_backends.Docker)
  --container-backend-args CONTAINER_BACKEND_ARGS
                        arguments to pass to the container backend upon
                        initialization (default: { "version": "auto" })
```