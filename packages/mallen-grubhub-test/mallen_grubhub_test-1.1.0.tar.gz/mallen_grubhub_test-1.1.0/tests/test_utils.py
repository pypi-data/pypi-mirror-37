import pandas as pd
from grubhub import utils
from datetime import datetime
import random
import tempfile
from sklearn.externals import joblib
import os


def build_df():
    """
    Build a test dataframe
    :return:
    """
    dates = [datetime.strftime(datetime(year=2018,
                                        month=11,
                                        day=d),
                               "%Y-%m-%d")
             for d in range(1, 30)]
    data = [{'event': 0,
             'order_count': random.randint(0,25),
             'region_id': random.choice([1,2,3]),
             'date': t} for t in dates
            ]

    test_df = pd.DataFrame(data=data,
                           index=range(len(data))
                           )
    test_df['date'] = pd.to_datetime(test_df['date'])
    return test_df


def test_add_weekday_feature():
    """
    Test that a weekday column is added to a dataframe
    :return:
    """
    test_df = build_df()
    test_df.loc[:, 'weekday'] = utils.add_weekday_feature(test_df)
    assert 'weekday' in test_df.columns
    assert not test_df['weekday'].isna().all()


def test_add_month_feature():
    """
    Test that a weekday column is added to a dataframe
    :return:
    """
    test_df = build_df()
    test_df.loc[:, 'month'] = utils.add_month_feature(test_df)
    assert 'month' in test_df.columns
    assert not test_df['month'].isna().all()


def test_add_time_feature():
    """
    test that a time feature is added to a dataframe
    :return:
    """
    test_df = build_df()
    test_df = utils.add_time_feature(test_df)
    assert 'time' in test_df.columns
    assert not test_df['time'].isna().all()


def test_build_region_features():
    """
    test that region classifier features are produced
    :return:
    """
    test_df = build_df()
    feature_df = utils.build_region_features(test_df, 1)
    assert 1 == feature_df['region_id'].unique()[0]
    assert 'weekday' in feature_df.columns
    assert not feature_df['weekday'].isna().all()
    assert 'month' in feature_df.columns
    assert not feature_df['month'].isna().all()
    assert 'time' in feature_df.columns
    assert not feature_df['time'].isna().all()


def test_train_model():
    """
    Test that a model is trained
    :return:
    """
    test_df = build_df()
    feature_df = utils.build_region_features(test_df, 1)
    model = utils.train_model(feature_df)
    assert hasattr(model, 'predict')
    assert len(utils.PREDICTORS) == model.n_features_


def test_save_model():
    """
    test saving a classifier to disk
    :return:
    """
    test_df = build_df()
    feature_df = utils.build_region_features(test_df, 1)
    model = utils.train_model(feature_df)
    with tempfile.TemporaryDirectory() as d:
        utils.save_model(model,
                         model_loc=d,
                         model_id='test')
        # test loading model to ensure it saved

        clf = joblib.load(os.path.join(d,
                                       utils.MODEL_SAVE_NAME.format(
                                           model_id='test')
                                       )
                          )
        assert hasattr(clf, 'predict')
        assert len(utils.PREDICTORS) == clf.n_features_


