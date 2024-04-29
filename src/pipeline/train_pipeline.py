import sys
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.components.data_ingestion import DataIngestion
from src.exception import CustomException


if __name__ == "__main__":
    try:
        obj = DataIngestion()
        # read the data and then do the train test split
        train_data_path, test_data_path = obj.initiate_data_ingestion()

        # do the data transformation (preprocessing)
        data_trainsformation = DataTransformation()
        train_arr, test_arr,_= data_trainsformation.initiate_data_transformation(train_data_path,test_data_path)

        # find the best model and train the best model and then save it
        modelTrainer = ModelTrainer()
        print(modelTrainer.initiate_model_trainer(train_arr,test_arr))

    except Exception as e:
        raise CustomException(e, sys)
