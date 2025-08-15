import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    debug = os.environ.get('FLASK_DEBUG', False)
    app.run(host='localhost', port=5001, debug=debug)
