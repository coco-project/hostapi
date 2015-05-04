from flask import Flask
from ipynbsrv.hostapi.routes.containers import blueprint as containers
import sys

'''
'''
def main():
    args = sys.argv
    if len(args) >= 2 and args[1] == '--help':
        sys.stderr.write("Usage: %s\n" % args[0])
        return 1

    app = Flask(__name__)
    app.secret_key = "uk1`\x15%\xdcl;\x8b\xa1\x9aK\x85\xa9\xd3@Fs\xdcQku\xf4"

    app.register_blueprint(containers)

    app.run(host='0.0.0.0')


if __name__ == "__main__":
    sys.exit(main())
