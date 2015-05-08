import argparse
from flask import Flask
from ipynbsrv.common.utils import ClassLoader
from ipynbsrv.hostapi import config
from ipynbsrv.hostapi.http.routes.containers import blueprint
import sys


def main():
    '''
    ipynbsrv host API command-line interface entry point.
    '''
    # define available arguments
    parser = argparse.ArgumentParser(description="ipynbsrv host API CLI tool")
    parser.add_argument('--container-backend', help='absolute name of the container backend module to load',
                        action='store', type=str, default="ipynbsrv.backends.container_backends.Docker", dest='container_backend')
    parser.add_argument('--container-backend-args', help='arguments to pass to the container backend upon initialization',
                        action='store', type=str, default="version='1.18'", dest='container_backend_args')
    parser.add_argument('-d, --debug', help='run in debug mode',
                        action='store_true', default=False, dest='debug')
    parser.add_argument('-l, --listen', help='the address to listen on',
                        action='store', type=str, default='0.0.0.0', dest='address')
    parser.add_argument('-p, --port', help='the port to bind to',
                        action='store', type=int, default=8080, dest='port')
    args = parser.parse_args()

    # set the container backend
    module, klass = ClassLoader.split(args.container_backend)
    backend = ClassLoader(module=module, klass=klass, args=args.container_backend_args)
    # TODO: line below doesn't work. Docker Client throws 404 error on operations
    # config.container_backend = backend

    # bootstrap the application and add our routes
    app = Flask(__name__)
    app.register_blueprint(blueprint)

    # run the application / HTTP REST API
    app.run(debug=args.debug, host=args.address, port=args.port)


if __name__ == "__main__":
    sys.exit(main())
