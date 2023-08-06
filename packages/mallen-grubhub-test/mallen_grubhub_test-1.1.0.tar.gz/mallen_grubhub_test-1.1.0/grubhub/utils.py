'''
This files is a utilities file to hold constants as well as helper functions
that might be used across multiple scripts
'''

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.externals import joblib
from typing import List
import numpy as np
import os
from datetime import datetime
import logging


# CONSTANTS
## data
DOC_ID = '1vKJ0GIKw18td9iHpKPa5N14fFsrBaYJY'
DRIVE_URL = 'https://drive.google.com/uc?id={doc_id}&export=dowload'
# feature names
DATE_COL_NAME = 'date'
MONTH_COL_NAME = 'month'
DOW_COL_NAME = 'weekday'
TIME_COL_NAME = 'time'
EVENT_COL_NAME = 'event'
REGION_ID_COL_NAME = 'region_id'
## model params
PREDICTORS = [DOW_COL_NAME,
              MONTH_COL_NAME,
              EVENT_COL_NAME,
              TIME_COL_NAME
              ]
LABELS = 'order_count'
N_TREES = 50
MIN_LEAF_SAMPLES = 1
MODEL_SAVE_LOC = 'models'
MODEL_SAVE_NAME = 'region_id_model-{model_id}.pkl'


# HELPER FUNCTIONS
def load_google_doc(doc_id: str = DOC_ID,
                    doc_url: str = DRIVE_URL,
                    **kwargs) -> pd.DataFrame:
    """
    This function will load a google drive document into a pandas dataframe
    :param doc_id: [str] ID of the google drive document
    :param doc_url: [str] google drive url
    :return: pandas dataframe of data from google drive doc
    """
    doc = doc_url.format(doc_id=doc_id)
    return pd.read_csv(doc, **kwargs)


def add_weekday_feature(df: pd.DataFrame,
                        weekday_name: str = DOW_COL_NAME,
                        date_col: str = DATE_COL_NAME) -> pd.DataFrame:
    """
    This function adds a weekday column to a dataframe if a 'date'
    column exits
    :param df: [DataFrame] dataframe with date information
    :param weekday_name: [str] name of the weekday column
    :param date_col: [str] name of the date column
    :return: [dataframe] data with new weekday column
    """
    if date_col not in df.columns:
        raise KeyError(f'No column named {date_col}')
    return df[date_col].dt.weekday


def add_month_feature(df: pd.DataFrame,
                        month_name: str = MONTH_COL_NAME,
                        date_col: str = DATE_COL_NAME) -> pd.DataFrame:
    """
    This function adds a month column to a dataframe if a 'date'
    column exits
    :param df: [DataFrame] dataframe with date information
    :param weekday_name: [str] name of the month column
    :param date_col: [str] name of the date column
    :return: [dataframe] data with new month column
    """
    if date_col not in df.columns:
        raise KeyError(f'No column named {date_col}')
    return df[date_col].dt.month


def add_time_feature(df: pd.DataFrame,
                     date_col: str = DATE_COL_NAME) -> pd.DataFrame:
    """
    This function adds the time feature to the data
    :param df: [DataFrame] data with date information
    :param date_col: [str] name of the date column
    :return:
    """
    sorted_df = df.sort_values(by=date_col)
    sorted_df.loc[:, TIME_COL_NAME] = range(0, sorted_df.shape[0])
    return sorted_df


def build_region_features(df: pd.DataFrame,
                          region_id: int) -> pd.DataFrame:
    """
    Construct the feature set for the model
    :param df: [Dataframe] raw input data
    :param region_id: [int] region ID for which to build features
    :return:
    """
    feature_df = df[df[REGION_ID_COL_NAME]==region_id].copy()
    feature_df.loc[:, DOW_COL_NAME] = add_weekday_feature(feature_df)
    feature_df.loc[:, MONTH_COL_NAME] = add_month_feature(feature_df)
    feature_df = add_time_feature(feature_df)
    return feature_df


def train_model(feature_df: pd.DataFrame,
                features: List = PREDICTORS,
                labels: str = LABELS) -> RandomForestRegressor:
    """
    Build a RandomForestRegressor from training data
    :param feature_df: [DataFrame] feature data to train on
    :param features: [list] features to use for training
    :param labels: [str] column name of the labels
    :return:
    """
    # TODO model hyperparams could be abstracted
    clf = RandomForestRegressor(N_TREES,
                                min_samples_leaf=MIN_LEAF_SAMPLES)
    clf.fit(feature_df[features], feature_df[labels])
    return clf


def model_validation(model,
                     feature_df: pd.DataFrame,
                     features: List = PREDICTORS,
                     labels: str = LABELS) -> float:
    feature_df.loc[:, 'predicted'] = model.predict(feature_df[features])
    feature_df.loc[:, 'residual'] = feature_df[labels] - feature_df['predicted']
    rmse = np.round(np.sqrt(feature_df['residual'].pow(2).mean()),
                    decimals=4)
    return rmse

def save_model(model,
               model_loc: str = MODEL_SAVE_LOC,
               model_name: str = MODEL_SAVE_NAME,
               model_id: str = datetime.now().strftime("%Y%m%d-%X")):
    """
    Save a sklearn model to disk
    :param model: sklearn classifier
    :param model_loc: [str] model directory
    :param model_name: [str] model name
    :param model_id: [str] model id to append to the name
    :return:
    """
    filename = model_name.format(model_id=model_id)
    if not os.path.isdir(model_loc):
        os.makedirs(model_loc)
    save_path = os.path.join(model_loc, filename)
    joblib.dump(model, save_path)
    logging.info(f'SAVING MODEL: {save_path}')


