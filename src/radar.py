#===============================================================================
# backend for radar app
#===============================================================================
from flask import Flask, request
import os
from util.fileupload import save_file
from flask.helpers import jsonify
from util.geo import get_ads, GPSPosition

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

@app.route('/ad/list', methods=['POST'])
def list():
    """
    Lists ads
    """
    location = GPSPosition(request.form.get("long"), request.form.get("lat"))
    total = request.form.get("total")
    ads = get_ads(location.longitude, location.latitude, total)
    
    ads = [x.add.all()[0] for x in ads]
    return jsonify(ads=[i.serialize for i in ads])

@app.route('/ad/create', methods=['POST'])
def create():
    """
    Creates an ad
    """
    from db import Location, Category, Ad
    location = Location(
                        longitude = request.form.get("long"),
                        latitude  = request.form.get("lat"),
                        )
    category = Category(
                        name = request.form.get("category")
                        )
    Ad.create(location, 
              request.form.get("email"),
              request.form.get("title"), 
              request.form.get("price"), 
              save_file(request.form.get("image")), 
              request.form.get("category"),
              request.form.get("lat",""))
    return jsonify({"res":True})

@app.route('/ad/delete', methods=['POST'])
def delete():
    from db import Ad
    """
    Deletes an ad
    """
    ad = Ad.get(request.form.get("id"))
    ad.location.delete()
    ad.delete()

if __name__ == '__main__':
    init_app()
    app.debug = True
    app.run(host='0.0.0.0')