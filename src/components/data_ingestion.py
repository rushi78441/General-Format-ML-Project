## Modular way of data ingestion in a machine learning project
# # This module is responsible for ingesting data from various sources, such as CSV files, databases, or APIs.

import os 
import sys 
from src.exception import CustomException
from src.logger import logging 
import pandas as pd
from sklearn.model_selection import train_test_split 
from dataclasses import dataclass
from src.components.data_transformation import DataTransformation 

## We make our class DataIngestionConfig to define the configuration for our data ingestion. 

@dataclass    ## helpful for use class Variables
class DataIngestionConfig:
    ## inputs for the data ingestion comonent
    train_data_path: str = os.path.join('artifacts', 'train.csv')   ## variable to store the path of the train data as type str , in artifacts folder and file name train.csv
    test_data_path:str = os.path.join('artifacts', 'test.csv')     ## variable to store the path of the test data as type str , in artifacts folder and file name test.csv
    raw_data_path:str = os.path.join('artifacts', 'data.csv')      ## variable to store the path of the raw data as type str , in artifacts folder and file name data.csv

## our DataIngestion class will handle the data ingestion process.
class DataIngestion:
    def __init__(self):
        ## Initialize the DataIngestion class with the configuration for data ingestion. 
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")
        try:
            ## we read from mongodb and apis too ,we do further
            df=pd.read_csv(os.path.join('notebook','data','stud.csv'))  ## read the data from the CSV file located in the notebook/data folder
            logging.info('Read the dataset as dataframe')

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)  ## create the directory if it does not exist
            df.to_csv(self.ingestion_config.raw_data_path, index=False,header=True)  ## save the raw data to the specified path without the index

            ## split the data into training and testing sets
            logging.info('Train test split initiated')
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)  ## split the data into training and testing sets with a 80-20 split

            ## saving the train and test sets to the specified paths
            logging.info('Train test split completed')
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)  ## save the training set to the specified path without the index
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)  ## save the testing set to the specified path without the index
            logging.info('Ingestion of the data is completed')

            ## return the paths of the train, test, and raw data, as these are require for data_transformation and model training
            logging.info("Data ingestion is completed successfully")
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,
                self.ingestion_config.raw_data_path 
            )
        ## handle any exceptions that occur during the data ingestion process
        except Exception as e:
            raise CustomException(e,sys)
        
if __name__ == "__main__":
    obj = DataIngestion()
    obj.initiate_data_ingestion()  ## call the initiate_data_ingestion method to start the data ingestion process

    data_transformation = DataTransformation()
    data_transformation.initiate_data_transformation(train_path=obj.ingestion_config.train_data_path , test_path=obj.ingestion_config.test_data_path)  ## call the initiate_data_transformation