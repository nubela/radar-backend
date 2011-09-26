#===============================================================================
# db schema/mapping for radar app
#===============================================================================
from radar import app
from flaskext.sqlalchemy import SQLAlchemy
import datetime
import math
from local_config import SQL_URI
from util.util import wsgi_print

app.config['SQLALCHEMY_DATABASE_URI'] = SQL_URI

db = SQLAlchemy(app)

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    ad  = db.relationship('Ad', backref='ad',
                             lazy='dynamic')
    
    def __init__(self, **kwargs):
        for k,v in kwargs.iteritems():
            setattr(self, k, v)
            
    def delete(self):
        db.session.delete(self)
        db.session.commit()
            
    @property
    def serialize(self):
        """
        Return this object data into an easily serializable form (For JSON)
        """
        return {
                "id": self.id,
                "longitude": self.longitude,
                "latitude": self.latitude,
                }

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    
    def __init__(self, **kwargs):
        for k,v in kwargs.iteritems():
            setattr(self, k, v)
            
    @property
    def serialize(self):
        """
        Return this object data into an easily serializable form (For JSON)
        """
        return {
                "id": self.id,
                "name": self.name,
                }
    
    @staticmethod
    def get(id):
        return Category.query.get(id)
    
    @staticmethod
    def match(name):
        return Category.query.filter(Category.name == name).all()[0]
    
    @staticmethod
    def gen_options():
        categories = Category.query.all()
        opt_str = ""
        for cat in categories:
            opt_str += "option value='"+str(cat.id)+"' | " + cat.name + "\n"
        return opt_str 

class Ad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    location = db.relationship("Location")
    created_timestamp = db.Column(db.DateTime)
    contact_email = db.Column(db.String(255))
    
    #meta below
    description = db.Column(db.String(255))
    title = db.Column(db.String(255))
    price = db.Column(db.Float(asdecimal=True))
    image = db.Column(db.String(255))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category =  db.relationship("Category")
    
    def __init__(self, **kwargs):
        for k,v in kwargs.iteritems():
            setattr(self, k, v)
            
    def delete(self):
        db.session.delete(self)
        db.session.commit()
            
    @property
    def serialize(self):
        return {
                "id": self.id,
                "location": self.location.serialize,
                "created_timestamp": self.created_timestamp.isoformat() ,
                "contact_email": self.contact_email,
                "description": self.description,
                "title": self.title,
                "price": str(int(self.price)),
                "image": self.image,
                "category": self.category.serialize ,
                }
    
    @staticmethod
    def get(id):
        return Ad.query.get(id)
    
    @staticmethod
    def create(location, email, title, price, image, category, desc=None,):
        
        db.session.add(location)
        db.session.flush()
        
        ad = Ad(location_id=location.id, 
                contact_email=email, 
                title=title,
                price=price,
                image=image,
                description=desc,
                category_id = category.id,
                created_timestamp = datetime.datetime.now(),
                )
        
        db.session.add(ad)
        db.session.commit()
        return ad.id