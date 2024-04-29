import os 
import sys
from dataclasses import dataclass

from sklearn.ensemble import AdaBoostRegressor, GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import r2_score

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object,evaluate_models


@dataclass
class ModelTrainerConfig:
    trained_model_file_paht = os.path.join("artifacts", "model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self,train_array,test_array):
        """ This function is used to find the best accurate model by hyperparameter tuning and save the best model and the return best model r2 error"""
        try:
            logging.info("Split training and test input data")
            X_train, Y_train, X_test, Y_test  = (
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )

            models = {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression":LinearRegression(),
                "AdaBoost Regressor":AdaBoostRegressor()
            }

            params = {
                "Decision Tree":{
                    'criterion':['squared_error', 'absolute_error', 'poisson', 'friedman_mse']
                },
                 "Random Forest":{
                     'n_estimators':[8,16,32,64,128,256]
                 },
                 "Gradient Boosting": {
                     'learning_rate':[0.1,0.01,0.5,0.001],
                     'n_estimators':[8,16,32,64,128,256],
                     'subsample':[0.6,0.7,0.75,0.8,0.85,0.9]

                 },
                 "Linear Regression":{},
                 "AdaBoost Regressor":{
                     'learning_rate':[0.1,0.01,0.5,0.001],
                     'n_estimators':[8,16,32,64,128,256]
                 }
            }

            model_report = evaluate_models(X_train=X_train, Y_train=Y_train, X_test=X_test, Y_test=Y_test, models=models, param=params)

            # find best model using model report (ex: {model 1 name:0.71, model 2 name: 0.88,........}) and then save the best model.
            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_model_name]

            if best_model_score <0.6:
                raise CustomException("No best model found")
            logging.info("Best model found on both training and testing dataset")

            save_object(
                file_path=self.model_trainer_config.trained_model_file_paht,
                obj = best_model
            )

            # find the best models r2 error and return it.
            predicted = best_model.predict(X_test)
            r2_square = r2_score(Y_test,predicted)

            return r2_square


        except Exception as e:
            raise CustomException(e,sys)