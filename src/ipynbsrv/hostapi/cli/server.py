import argparse
from flask import Flask
from ipynbsrv.hostapi.http.routes.containers import blueprint as containers
import sys


def main():
    '''
    ipynbsrv host API command-line interface entry point.
    '''
    parser = argparse.ArgumentParser(description="ipynbsrv host API CLI tool")
    parser.add_argument('-d, --debug', help='run in debug mode',
                        action='store_true', default=False, dest='debug')
    parser.add_argument('-l, --listen', help='the address to listne on',
                        action='store', type=str, default='0.0.0.0', dest='address')
    parser.add_argument('-p, --port', help='the port to bind to',
                        action='store', type=int, default=8080, dest='port')
    args = parser.parse_args()

    app = Flask(__name__)
    app.register_blueprint(containers)
    app.run(debug=args.debug, host=args.address, port=args.port)


if __name__ == "__main__":
    sys.exit(main())
