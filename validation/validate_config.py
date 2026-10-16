import logging
import config
from validation.validate_number import validate_number


logger = logging.getLogger(__name__)


def validate_config():
    valid_config = True

    positive_values = [
        'slippage',
        'risk_percentage',
        'sl_risk_percentage',
        'free_margin_threshold'
        'margin_exposure_threshold'
        'max_positions'
    ]

    negative_values = [
        'max_daily_loss',
        'max_daily_pnl',
    ]

    non_empty_values = [
        'exposure_groups',
        'max_group_exposure',
        'max_symbol_exposure',
    ]

    for positive_value in positive_values:
        config_value = config[positive_value]

        if not validate_number(config_value):
            logger.warning("Value: %s is not a valid number", positive_value)
            valid_config = False

            pass

        if config_value <= 0:
            logger.warning("Value: %s is not a positive number", positive_value)
            valid_config = False


    for negative_value in negative_values:
        config_value = config[negative_value]

        if not validate_number(config_value):
            logger.warning("Value: %s is not a valid number", negative_value)
            valid_config = False

            pass

        if config_value >= 0:
            logger.warning("Value: %s is not a negative number", negative_value)
            valid_config = False

    # TODO validate not emty

    return valid_config