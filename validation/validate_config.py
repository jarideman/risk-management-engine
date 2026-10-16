import logging
import config
from validation.validate_number import validate_number


logger = logging.getLogger(__name__)


def validate_config():
    valid_config = True

    positive_values = [
        'SLIPPAGE',
        'RISK_PERCENTAGE',
        'SL_RISK_PERCENTAGE',
        'FREE_MARGIN_THRESHOLD',
        'MAX_POSITIONS',
        'MARGIN_EXPOSURE_THRESHOLD',
    ]

    negative_values = [
        'MAX_DAILY_LOSS',
        'MAX_DAILY_PNL',
    ]

    non_empty_values = [
        'EXPOSURE_GROUPS',
        'MAX_GROUP_EXPOSURE',
        'MAX_SYMBOL_EXPOSURE',
    ]

    for positive_value in positive_values:
        config_value = getattr(config, positive_value, None)

        if not config_value:
            logger.warning(
                "Config value %s is empty",
                positive_value,
            )
            valid_config = False

            continue


        if not validate_number(config_value):
            logger.warning("Value: %s is not a valid number", positive_value)
            valid_config = False

            continue


        if config_value <= 0:
            logger.warning("Value: %s is not a positive number", positive_value)
            valid_config = False


    for negative_value in negative_values:
        config_value = getattr(config, negative_value, None)

        if not config_value:
            logger.warning(
                "Config value %s is empty",
                negative_value,
            )
            valid_config = False

            continue


        if not validate_number(config_value):
            logger.warning("Value: %s is not a valid number", negative_value)
            valid_config = False

            continue


        if config_value >= 0:
            logger.warning("Value: %s is not a negative number", negative_value)
            valid_config = False


    for non_empty_value in non_empty_values:
        config_value = getattr(config, non_empty_value, None)

        if not config_value:
            logger.warning(
                "Config value %s is empty",
                non_empty_value,
            )
            valid_config = False

            continue

    return valid_config
