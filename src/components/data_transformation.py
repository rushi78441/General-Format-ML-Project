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
import src.utils as utils


## Data Transformation Configuration (in this we wants inputs rquired for data transformation)
@dataclass
class DataTransformationConfig: 
    preprocessor_obj_file_path: str = os.path.join('artifacts', 'preprocessor.pkl')

## Data Transformation Class
class DataTransformation: 
    def __init__(self): 
        self.data_transformation_config = DataTransformationConfig()

    ## Function to get the preprocessor object
    def get_data_transformer_object(self):
        """ 
        This function creates a preprocessor object that will handle both numerical and categorical features.
        It uses pipelines.
        """
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
                    ('imputer', SimpleImputer(strategy='median')),    
                    ('scaler', StandardScaler())
                ]
            ) 
    
            ## Categorical Pipeline - this pipeline will handle categorical features
            categorical_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='most_frequent')),
                    ('one_hot_encoder', OneHotEncoder(handle_unknown='ignore')),
                    ('scaler', StandardScaler())  
                ]
            )

            logging.info('numerical and categorical feature scaling and encoding completed')

            ## Preprocessor - this will combine both numerical and categorical pipelines
            ## ColumnTransformer is used to apply different transformations pipeline to different columns
            preprocessor = ColumnTransformer( 
                transformers=[
                    ('numerical', numerical_pipeline, numerical_features),
                    ('categorical', categorical_pipeline, categorical_features)
                ]
            )

            logging.info('preprocessor object created')
            return preprocessor
        
        except Exception as e:
            raise CustomException(e, sys) 
        

    ## Function to fit and transform the data
    def initiate_data_transformation(self, train_path, test_path):
        """
        This function reads the train and test data, applies the preprocessor to both,
        and saves the preprocessor object to a file.
        """
        try: 
            trained_data = pd.read_csv(train_path)
            test_data = pd.read_csv(test_path)
            logging.info('Train and test data read successfully')

            logging.info('Obtaining preprocessor object')
            preprocessor_obj = self.get_data_transformer_object()

            ## Splitting features and target variable
            target_column_name = 'math_score'
            input_features_train_df = trained_data.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = trained_data[target_column_name]
            input_features_test_df = test_data.drop(columns=[target_column_name], axis=1) 
            target_feature_test_df = test_data[target_column_name] 

            logging.info('Applying preprocessor object on training and testing dataframes')
            ## Fitting the preprocessor on training data and transforming both train and test data
            input_features_train_df = preprocessor_obj.fit_transform(input_features_train_df)
            input_features_test_df = preprocessor_obj.transform(input_features_test_df)
            
            logging.info('Preprocessing completed')

            ## Saving the preprocessor object to a file
            train_arr = np.c_[
                input_features_train_df, 
                np.array(target_feature_train_df)
            ]

            test_arr = np.c_[
                input_features_test_df, 
                np.array(target_feature_test_df)
            ]

            logging.info('Saving preprocessor object to file')

            ## Saving the preprocessor object to a file
            utils.save_object( 
                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprocessor_obj
            )

            ## returning the preprocessor object and the transformed arrays
            return (
                train_arr, 
                test_arr, 
                self.data_transformation_config.preprocessor_obj_file_path   ## preprocessor.pkl
            )
        except Exception as e:
            raise CustomException(e, sys)