#===============================================================================
# backend for radar app
#===============================================================================
from flask import Flask, request
import os
from util.fileupload import save_file
from flask.helpers import jsonify
from util.geo import get_ads, GPSPosition, get_ads_cat_filtered,\
    get_ads_email_filtered
from sqlalchemy.sql.expression import and_

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
    
    Type: Normal / First List (not stated)
    - Requires the following param:
        * long, lat
        * total
        
    Type: Categorized (categorized)
        (Additional param)
        * category_id
    
    Type: My Ads (my_ad)
        (Additional param)
        * email
    """
    from db import Location, Ad
    
    req_type = request.form.get("type",None)
    location = GPSPosition(request.form.get("long"), request.form.get("lat"))
    total = int(request.form.get("total"))
    ads = None
    
    if req_type == "my_ad":
        email  = request.form.get("email")
        ads = get_ads_email_filtered(email, location.longitude, location.latitude, total)
    elif req_type == "categorized":
        #get category
        ads = get_ads_cat_filtered(int(request.form.get("category_id")), location.longitude, location.latitude, total)
    else:
        ads = get_ads(location.longitude, location.latitude, total)
    
    ads = [x.ad.all()[0] for x in ads]
    if len(ads) > 0:
        print jsonify({
                        "ads":[i.serialize for i in ads],
                        "res": True
                        }).data
        return jsonify({
                        "ads":[i.serialize for i in ads],
                        "res": True
                        })
    else:
        print jsonify({"res": False}).data
        return jsonify({"res": False})

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
    category = Category.get(request.form.get("category"))
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