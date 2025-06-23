import sys 
import os 
from dataclasses import dataclass 
import numpy as np 
import pandas as pd 
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from src.exception import CustomException
from src.logger import logging
import pickle

## Data Transformation Configuration (in this we wants inputs rquired for data transformation)
@dataclass
class DataTransformationConfig: 
    preprocessor_obj_file_path: str = os.path.join('artifacts', 'preprocessor.pkl')

## Data Transformation Class
class DataTransformation: 
    def __init__(self): 
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        try:
            numerical_features = ['writing_score', 'reading_score']
            categorical_features = [
                'gender',
                'race_ethnicity',
                'parental_level_of_education',
                'lunch',
                'test_preparation_course'
            ]

            ## Numerical Pipeline - this pipeline will handle numerical features
            numerical_pipeline = Pipeline( 
                steps=[
                    ('imputer', SimpleImputer(strategy='mean')),    
                    ('scaler', StandardScaler())
                ]
            ) 
        except Exception as e:
            pass