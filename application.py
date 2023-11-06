#!/usr/bin/python3
import os

from app import create_app

if __name__ == '__main__':  # pragma: no cover - initialization only
    app = create_app()
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = bool(os.getenv('FLASK_DEBUG', False))
    app.run(port=port, debug=debug)
