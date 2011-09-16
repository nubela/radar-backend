#===============================================================================
# db schema/mapping for radar app
#===============================================================================
import radar
from flaskext.sqlalchemy import SQLAlchemy

radar.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/radar'
db = SQLAlchemy(radar)

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    longitude = db.Column(db.Integer)
    latitude = db.Column(db.Integer)
    pointy = db.relationship('Ad', backref='ad',
                             lazy='dynamic')
    
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
            
    @property
    def serialize(self):
        return {
                "id": self.id,
                "location": self.location.serialize,
                "created_timestamp": self.created_timestamp,
                "contact_email": self.contact_email,
                "description": self.description,
                "title": self.title,
                "price": self.price,
                "image": self.image,
                "category": self.category.serialize,
                }
    
    @staticmethod
    def create(location, email, title, price, image, category, desc=None,):
        
        db.session.add(location)
        db.session.flush()
        
        db.session.add(category)
        db.session.flush()
        
        ad = Ad(location_id=location.id, 
                contact_email=email, 
                title=title,
                price=price,
                image=image,
                description=desc,
                category_id = category.id,
                )
        
        db.session.add(ad)
        db.commit()