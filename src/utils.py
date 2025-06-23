import os 
import sys 
import numpy as np 
import pandas as pd 
from src.exception import CustomException 
from src.logger import logging
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
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
    

def evaluate_models(X_train, y_train, X_test, y_test, models):
    """
    Evaluate multiple regression models and return their performance metrics.
    
    Parameters:
    - X_train: Training feature set.
    - y_train: Training target variable.
    - X_test: Testing feature set.
    - y_test: Testing target variable.
    - models (dict): Dictionary of model names and their instances.
    
    Returns:
    - dict: A dictionary containing model names and their respective performance metrics.
    """
    report = {}

    for i in range(len(list(models))):
        try:
            model = list(models.values())[i]
            model.fit(X_train, y_train)

            ## Prediction
            y_train_pred = model.predict(X_test)
            y_test_pred = model.predict(X_test)

            ## Evaluation
            test_model_r2_score = r2_score(y_test, y_test_pred)

            report[list(models.keys())[i]] = test_model_r2_score
            logging.info(f"Model: {list(models.keys())[i]}, R2 Score: {test_model_r2_score}")

        except Exception as e:
            logging.error(f"Error evaluating {model}: {e}")
    
    return report

def load_object(file_path):
    """
    Load an object from a file using pickle.
    
    Parameters:
    - file_path (str): The path from which the object will be loaded.
    
    Returns:
    - The loaded object.
    
    Raises:
    - CustomException: If there is an error during loading the object.
    """
    try:
        with open(file_path, 'rb') as fileobj:
            return dill.load(fileobj)
        
        logging.info(f"Object loaded successfully from {file_path}")
            
    except Exception as e:
        raise CustomException(f"Error loading object: {e}") from e