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
app.config['samples_dir'] = os.path.join(os.getcwd(), "static/uploads")

def init_app():
    """
    Initializes the app for first run.
    """
    upload_dir = app.config["upload_dir"]
    if not os.path.exists(upload_dir):
        os.mkdir(upload_dir)

@app.route('/ad/get', methods=['POST'])
def get_ad():
    """
    Retrieves all the information about an ad.
    """
    from db import Ad
    ad = Ad.query.get(request.form.get("id"))
    if ad:
        return jsonify({"res": ad.serialize })
    else: 
        return jsonify({"res": False })
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
    
    Requires the following param:
        * long, lat
        * category, email, title, price, image, category, description
    """
    from db import Location, Category, Ad
    location = Location(
                        longitude = request.form.get("long"),
                        latitude  = request.form.get("lat"),
                        )
    category = Category(
                        name = request.form.get("category")
                        )
    id = Ad.create(location, 
                      request.form.get("email"),
                      request.form.get("title"), 
                      request.form.get("price"), 
                      save_file(request.form.get("image")), 
                      category,
                      request.form.get("description",""))
    return jsonify({"res":id})

@app.route('/ad/delete', methods=['POST'])
def delete():
    from db import Ad
    """
    Deletes an ad
    """
    ad = Ad.get(request.form.get("id"))
    ad.location.delete()
    ad.delete()
    return jsonify({"res": True })

if __name__ == '__main__':
    init_app()
    app.debug = True
    app.run(host='0.0.0.0')