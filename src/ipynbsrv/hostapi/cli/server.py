import argparse
from flask import Flask
from ipynbsrv.common.utils import ClassLoader
from ipynbsrv.hostapi import config
from ipynbsrv.hostapi.http.routes.containers import blueprint as containers_blueprint
from ipynbsrv.hostapi.http.routes.core import blueprint as core_blueprint
import sys


def main():
    """
    ipynbsrv host API command-line interface entry point.
    """
    # define available arguments
    parser = argparse.ArgumentParser(description='ipynbsrv host API CLI tool')
    parser.add_argument('-d', '--debug', help='run in debug mode',
                        action='store_true', default=False, dest='debug')
    parser.add_argument('-l', '--listen', help='the address to listen on (default: 0.0.0.0)',
                        action='store', type=str, default='0.0.0.0', dest='address')
    parser.add_argument('-p', '--port', help='the port to bind to (default: 8080)',
                        action='store', type=int, default=8080, dest='port')
    parser.add_argument('--container-backend', help='absolute name of the container backend class to load (default: ipynbsrv.backends.container_backends.Docker)',
                        action='store', type=str, default='ipynbsrv.backends.container_backends.Docker', dest='container_backend')
    parser.add_argument('--container-backend-args', help='arguments to pass to the container backend upon initialization (default: { "version": "auto" })',
                        action='store', type=str, default='{ "version": "auto" }', dest='container_backend_args')
    args = parser.parse_args()

    # set configuration values
    config.debug = args.debug

    try:
        module, klass = ClassLoader.split(args.container_backend)
        backend = ClassLoader(module=module, klass=klass, args=args.container_backend_args)
        config.container_backend = backend.get_instance()
    except Exception as ex:
        if config.debug:
            raise ex
        else:
            print """Initializing the container backend failed.
Turn on debug mode (-d. --debug) to get more information about the error."""
            sys.exit(1)

    # bootstrap the application and add our routes
    app = Flask(__name__)
    app.register_blueprint(containers_blueprint)
    app.register_blueprint(core_blueprint)

    # run the application / HTTP REST API
    app.run(debug=config.debug, host=args.address, port=args.port)


if __name__ == "__main__":
    sys.exit(main())
