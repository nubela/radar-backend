#===============================================================================
# backend for radar app
#===============================================================================
from flask.app import Flask
import os

app = Flask(__name__)

def init_db():
    from db import db
    db.create_all()

#dir config
app.config['upload_dir'] = os.path.join(os.getcwd(), "static/uploads")

def init_app():
    """
    Initializes the app for first run.
    """
    upload_dir = app.config["upload_dir"]
    if not os.path.exists(upload_dir):
        os.mkdir(upload_dir)

@app.route('/')
def hw():
    return "helloworld"

if __name__ == '__main__':
    init_app()
    app.debug = True
    app.run(host='0.0.0.0')