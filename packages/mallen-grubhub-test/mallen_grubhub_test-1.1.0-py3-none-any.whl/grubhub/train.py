"""
This script will train a region based model
"""
import argparse
from grubhub import utils as _utils
import logging
import sys
import click

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# TODO handle deprication warning.
# there is an issue with numpy and pandas updates discussed here
# https://stackoverflow.com/questions/51986414/deprecationwarning-numpy-core-umath-tests
# workaround is hacky


@click.command()
@click.option("--region_id", default=1, help="Region for model training")
@click.option("--model_id", default=None, help="Trained model ID")
def main(region_id: int, model_id:str):
    """
    Perform feature engineering and model training and saving
    :param region_id:
    :return:
    """

    # load training data
    logging.info('GETTING TRAINING DATA...')
    training_data = _utils.load_google_doc(_utils.DOC_ID,
                                           _utils.DRIVE_URL,
                                           parse_dates=[_utils.DATE_COL_NAME]
                                           )
    # perform feature engineering
    logging.info('BUILDING FEATURES...')
    feature_data = _utils.build_region_features(training_data, region_id)
    # build model
    logging.info('TRAINING MODEL...')
    model = _utils.train_model(feature_data)
    # CV performance
    logging.info('CHECKING MODEL PERFORMANCE...')
    score = _utils.model_validation(model, feature_data)
    logging.info(f"MODEL PERFORMANCE RMSE: {score}")
    # save model
    if not model_id:
        _utils.save_model(model)
    else:
        _utils.save_model(model, model_id=model_id)


if __name__ == '__main__':
    main()