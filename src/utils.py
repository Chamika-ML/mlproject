import os
import pickle
import sys
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score
from src.exception import CustomException



def save_object(file_path,obj):
    """ This function is used to create folder and pickle file inside that"""
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj,file_obj)
    
    except Exception as e:
        raise CustomException(e,sys)
    

def evaluate_models(X_train, Y_train, X_test, Y_test, models, param):
    """ This function is used to find best prameters for each machine learning moldel and calsulate r2 scors for best models and then return dict like
        {model 1 name:0.71, model 2 name: 0.88,........}"""
    try:
        report = {}

        for i in range(len(list(models))):
            # select model and its parameters
            model = list(models.values())[i]
            para = param[list(models.keys())[i]]

            gs = GridSearchCV(model,para,cv=3)
            gs.fit(X_train,Y_train)

            # select best paramters which are found in gridserchcv and train the model
            model.set_params(**gs.best_params_)
            model.fit(X_train,Y_train)

            # calculate r2 score an update the result dictionary
            y_test_pred = model.predict(X_test)
            test_model_score = r2_score(Y_test,y_test_pred)

            report[list(models.keys())[i]] = test_model_score
        
        return report

    except Exception as e:
        raise CustomException(e,sys)
    

def load_object(file_path):
    """ This function is used to load and return pickle file"""
    try:
        with open(file_path, 'rb') as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        raise CustomException(e,sys)