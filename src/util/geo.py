from kdtree import KDTree
from sqlalchemy.sql.expression import and_
from util import fib

class GPSPosition:
    """
    Represents a GPS coordinate
    """
    
    def __init__(self, longtitude, latitude):
        self.longitude = int(longtitude)
        self.latitude = int(latitude)

def get_ads(longitude, latitude, total):
    """
    talks to the db, returns a list of _total_ ads that are near, sorted by proximity. 
    """
    from db import Location
    
    locations = []
    fib_gen = fib()
    fib_no = fib_gen.next()
    
    while len(locations) < total:
        location_conditions = and_(
                                   Location.latitude <= latitude + fib_no,
                                   Location.latitude >= latitude - fib_no,
                                   Location.longitude <= longitude + fib_no,
                                   Location.longitude >= longitude - fib_no,
                                   )
        locations = Location.query.filter(location_conditions).all()
        fib_no = fib_gen.next()
        
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