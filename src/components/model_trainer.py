import os,sys
import numpy as np
import pandas as pd
from dataclasses import dataclass
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor,AdaBoostRegressor
from sklearn.linear_model import LinearRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor  
from xgboost import XGBRegressor
from src.exception import CustomException
from src.logger import logging
import src.utils as utils
from sklearn.metrics import r2_score

@dataclass
class ModelTrainerConfig:
    model_trainer_file_path: str = os.path.join('artifacts', 'model.pkl')


## Model Trainer Class
class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    ## initialize the model_trainer
    def initialize_model_trainer(self,train_data, test_data,preprocessor_obj):
        """
        This function initializes the model trainer with various regression models.
        """
        try:
            logging.info('Spliting train and test input data')

            X_train,y_train,X_test,y_test = (
                train_data[:,:-1],
                train_data[:,-1],
                test_data[:,:-1],
                test_data[:,-1]
            )

            models = {
                'RandomForestRegressor': RandomForestRegressor(),
                'GradientBoostingRegressor': GradientBoostingRegressor(),
                'AdaBoostRegressor': AdaBoostRegressor(),
                'LinearRegression': LinearRegression(),
                'GaussianNB': GaussianNB(),
                'SVR': SVR(),
                'DecisionTreeRegressor': DecisionTreeRegressor(),
                'XGBRegressor': XGBRegressor()
            }

            ## Evaluate the models
            logging.info('Evaluating models')
            models_report : dict = utils.evaluate_models(X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test, models=models)
        
            ## to get best model score from the report
            best_model_score = max(sorted(models_report.values()))

            ## to get best model name from the report
            best_model_name = list(models_report.keys())[
                list(models_report.values()).index(best_model_score)
            ]

            ## to get best model
            best_model = models[best_model_name]

            if best_model_score < 0.6:
                raise CustomException('Not got best model')
            logging.info(f'Best model found: {best_model_name} with score: {best_model_score}')

            ## Save the best model
            logging.info('Saving the best model')
            utils.save_object(
                file_path=self.model_trainer_config.model_trainer_file_path,
                obj=best_model
            )

            predicted = best_model.predict(X_test)
            logging.info(f'Predictions: {predicted}')

            r2 = r2_score(y_test, predicted)
            logging.info(f'R2 Score of the best model: {r2_score}')

        except Exception as e:
            raise CustomException(e, sys)    