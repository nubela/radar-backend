from kdtree import KDTree
from sqlalchemy.sql.expression import and_

class GPSPosition:
    """
    Represents a GPS coordinate
    """
    
    def __init__(self, longtitude, latitude):
        self.longitude = int(longtitude)
        self.latitude = int(latitude)

def get_ads_email_filtered(email, longitude, latitude, total):
    from db import Ad
    ads = Ad.query.filter(Ad.contact_email == email).all()
    locations = []
    for ad in ads:
        locations += [ad.location]
    
    return location_sort((longitude, latitude), locations, total)

def get_ads_cat_filtered(cat_id, longitude, latitude, total):
    from db import Ad
    ads = Ad.query.filter(Ad.category_id == cat_id).all()
    locations = []
    for ad in ads:
        locations += [ad.location]
    return location_sort((longitude, latitude), locations, total)

def get_ads(longitude, latitude, total):
    """
    talks to the db, returns a list of _total_ ads that are near, sorted by proximity. 
    """
    from db import Location, Ad
    from util import exp
    
    locations = []
    exp_gen = exp()
    exp_no = exp_gen.next()
    
    while len(locations) < int(total):
        
        #location filtered query
        location_conditions = and_(
                                   Location.latitude <= latitude + exp_no,
                                   Location.latitude >= latitude - exp_no,
                                   Location.longitude <= longitude + exp_no,
                                   Location.longitude >= longitude - exp_no,
                                   )
        locations  = Location.query.filter(location_conditions).all()
            
    return location_sort((longitude, latitude), locations, total)

def location_sort(point, locations, total):
    """
    Given a point, and a list of Location objects, returns a list of Location, capped with a length of _total_, sorted by proximity.
    """
    sorted_locations = []
    location_map = {}
    location_data = []
    for l in locations:
        k = (l.longitude, l.latitude)
        if not location_map.has_key(k):
            location_data += [k] 
            location_map[k] = [l]
        else: location_map[k] += [l]
    
    location_data_sorted = proximity_filter(point, location_data, total)
    
    for k in location_data_sorted:
        while len(location_map[k]) > 0:
            sorted_locations += [location_map[k][0]]
            del location_map[k][0]
    
    return sorted_locations

def proximity_filter(point, data, total):
    """
    given a point, and a data set of points, we return a list of points, capped with a length of _total_, sorted in proximity.
    """
    tree = KDTree.construct_from_data(data)
    return tree.query(query_point=point, t=total)