"""
test suite for radar backend
"""
import unittest
from radar import app, init_db
import tempfile
from data import populate_categories, mock_ads
import os
from util.util import random_string
from util.fileupload import open_file
from random import randint
from db import Location
import json

class RadarTests(unittest.TestCase):
    
    def setUp(self):
        #declare testing state
        app.config["TESTING"] = True
        #spawn test client
        self.app = app.test_client()
        #temp db
        self.db, app.config["DATABASE"] = tempfile.mkstemp()
        init_db()
        populate_categories()
        mock_ads()
    
    def tearDown(self):
        os.close(self.db)
        os.unlink(app.config["DATABASE"])
        
    def test_ad_creation(self):
        """
        Tests the API to create ads.
        """
        data = {
                "long": randint(-360000000,360000000),
                "lat": randint(-360000000,360000000),
                "category": 5,
                "email": "test@test.com",
                "title": "Test Item " + random_string(),
                "price": str(randint(0,1000)),
                "image": open_file("sample_upload_pic.jpg"),
                "description": " ".join([random_string() for i in range(10)]),
                }
        
        #create it
        create_response  = self.app.post("/ad/create", data=data)
        response_dict = json.loads(create_response.data)
        ad_id = response_dict["res"]
        
        #retrieve it
        res = self.app.post("/ad/get", data={"id": ad_id})
        assert "res" in res.data
    
    def test_first_ad_list(self):
        """
        """
        pass
    
    def test_categorized_ad_list(self):
        """
        """
        pass
    
    def test_my_ads_list(self):
        """
        """
        pass
    
    def test_delete_ad(self):
        """
        """
        pass 
    
if __name__ == '__main__':
    unittest.main()