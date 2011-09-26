#===============================================================================
# FIle upload library - Handles AJAX (POST) files that are non-multipart.
# 
# In this module, we will abstract some patterns that has to do with saving files.
# /steven 8th sep 2011. 
#===============================================================================

import os
import base64
from util import random_string
from util import wsgi_print

def save_file(post_file, extension=None, subdir=None, dir_to_save=None):
    """
    Saves a file to a directory.
    * file must be base64 encoded stream.
    
    - Ensures no file clashes.
    - Returns the filename.
    """
    
    wsgi_print("nube2")
    
    if extension == None:
        extension = ".jpg"
    if dir_to_save == None:
        from radar import app
        dir_to_save = app.config["upload_dir"]
    if subdir == None: 
        subdir = ""
        
    working_dir = os.path.join(dir_to_save, subdir)
    
    file_data = base64.b64decode(post_file)
    
    wsgi_print("nube3")
    
    file_name = random_string() + extension
    absolute_write_path = os.path.join(working_dir, file_name) 
    while os.path.exists(absolute_write_path):
        file_name = random_string() + extension 
        absolute_write_path = os.path.join(working_dir, file_name)
    
    file = open(absolute_write_path,'wb+')
    file.write(file_data)
    file.close()
    
    wsgi_print("nube")
    
    return file_name

def open_file(file_name):
    """
    opens file in samples, and return base64 encoded streams.
    """
    from radar import app
    sample_dir = app.config["samples_dir"]
    file = open(os.path.join(sample_dir, file_name), 'r')
    stream = file.read()
    encoded_stream = base64.b64encode(stream)
    return encoded_stream
    