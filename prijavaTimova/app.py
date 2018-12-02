from flask import Flask, send_from_directory, make_response
from flask_cors import CORS

from app.view import main_view
import sys


def create_app(debug=False):
    app = Flask(__name__, static_folder='public')
    CORS(app)
    app.register_blueprint(main_view.members)
    app.register_blueprint(main_view.teams)
    app.debug = debug

    @app.route('/<path:path>')
    def serve_static(path):
        resp = make_response(send_from_directory(app.static_folder, path))
        resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        resp.headers["Pragma"] = "no-cache"
        resp.headers["Expires"] = "0"
        return resp

    @app.route('/api/secret/')
    def secret_route():
        return send_from_directory('view', 'secret.html')

    @app.route('/')
    def index_page():
        return send_from_directory(app.static_folder, 'listaTimova.html')

    return app


if __name__ == "__main__":
    debug = len(sys.argv) > 1 and sys.argv[1] == 'debug'
    app = create_app(debug=debug)
    app.run(host='0.0.0.0')
