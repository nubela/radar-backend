"""
data mocking/population tool
"""
from db import Category, db, Location, Ad
from util.geo import GPSPosition
from util.util import random_string 
from random import randint

def populate_categories():
    """
    populates table with categories.
    """
    #check if categories are already populated
    all_cat = Category.query.all()
    if len(all_cat) > 0:
        return
    
    categories = (
                  #personals
                  "Strictly Platonic",
                  "Woman seeking Woman",
                  "Woman seeking Men",
                  "Man seeking Woman",
                  "Man seeking Man",
                  "Man seeking Man",
                  #for sale
                  "Free",
                  "Bikes",
                  "Books",
                  "Business",
                  "Computer",
                  "General",
                  "Household",
                  "Jewelry",
                  "Tickets",
                  "Tools",
                  "Wanted",
                  "Jewelry",
                  "Appliances",
                  "Arts and Crafts",
                  "Auto parts",
                  "Vehicles",
                  "Phones",
                  "Jewelry",
                  "Clothes",
                  "Electronics",
                  "Music",
                  "Video",
                  "Games",
                  #services
                  "Beauty Services",
                  "Computer Services",
                  "Creative Services",
                  "Labour Services",
                  "Writing Services",
                  "Legal Services",
                  #housing
                  "Rent",
                  "Apartments",
                  "Sell",
                  "Rooms/Shared",
                  )
    for c in categories:
        category = Category(name=c)
        db.session.add(category)
    db.session.commit()

def mock_ads():
    all_cat = Category.query.all() 
    for i in range(100):
        posn = GPSPosition(randint(-360000000,360000000), randint(-360000000,360000000))
        rand_cat = all_cat[randint(0, len(all_cat)-1)]
        location = Location(
                            longitude=posn.longitude,
                            latitude=posn.latitude
                            )
        Ad.create(location, "mock@mock.com", "Random Mock App" + random_string(), str(randint(0,1000)), "sample_upload_pic.jpg", rand_cat," ".join([random_string() for i in range(10)]))
    db.session.commit()
    
if __name__ == '__main__':
    populate_categories()
    mock_ads()