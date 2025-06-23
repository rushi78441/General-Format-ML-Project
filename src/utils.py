import os 
import sys 
import numpy as np 
import pandas as pd 
from src.exception import CustomException 
from src.logger import logging
import dill

def save_object(file_path, obj):
    """
    Save an object to a file using pickle.
    
    Parameters:
    - file_path (str): The path where the object will be saved.
    - obj: The object to be saved.
    
    Raises:
    - CustomException: If there is an error during saving the object.
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)  # Ensure the directory exists

        with open(file_path, 'wb') as fileobj:
            dill.dump(obj, fileobj)
        
        logging.info(f"Object saved successfully at {file_path}")
        
    except Exception as e:
        raise CustomException(f"Error saving object: {e}") from e