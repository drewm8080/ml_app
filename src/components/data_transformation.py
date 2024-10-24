import sys
from dataclasses import dataclass

import numpy as np 
import pandas as pd 
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline 
from sklearn.preprocessing import OneHotEncoder,StandardScaler
import os

from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifact','proprocessor.pkl')

class DataTransformation:
    '''
    This function is for data transformation
    
    '''

    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        try:
            numerical_columns = ['writing_score','reading_score']
            categorical_colums = [
                'gender',
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course"
            ]

            num_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='median')),
                    ('scaler', StandardScaler())
                ]
            )
            cat_pipeline = Pipeline(

                steps= [
                    ('imputer', SimpleImputer(strategy='most_frequent')),
                    ('one_hot_encoder',OneHotEncoder()),
                    ('scaler',StandardScaler())
                ]
            )

            preprocessor = ColumnTransformer(
                [
                    ('num_pipeline',num_pipeline,numerical_columns)
                    ('cat_pipeline',cat_pipeline,categorical_colums)
                ]
            )

            return preprocessor
        except Exception as e:
            print(e)

    def initiate_data_transformation(self,train_path,test_path):

        try:
            train_df = pd.read_csv(train_path)
            test_df =pd.read_csv(test_path)

            print('train and test data done')
            preprocessing_obj = get_data_transformer_object()
            target_column = 'math_score'
            numerical_columns = ['writing_score','reading_score']

            input_feature_train_df = train_df.drop(columns = target_column,axis=1)
            target_feature_train_df = train_df[target_column]
            
            
            input_feature_test_df = test_df.drop(columns = target_column,axis=1)
            target_feature_test_df = test_df[target_column]

            print('applying preprocesisng on training and testing')

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)
            train_arr = np.c_[input_feature_train_arr,np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr,np.array(target_feature_test_df)]

            print('saving preprocessed objects')

            save_object(
                file_path = self.data_transformation_config.preprocessor_obj_file_path
                obj = preprocessing_obj
            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )



        except Exception as e:
            print(e)


            
