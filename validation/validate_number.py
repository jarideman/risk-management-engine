import logging
import math


logger = logging.getLogger(__name__)


def validate_number(num):
    if num is None:
        logger.warning("Invalid number: value is None")

        return False

    if isinstance(num, bool) or not isinstance(num, (int, float)):
        logger.warning(
            "Invalid number: expected int or float, got %s (%r)",
            type(num).__name__,
            num,
        )

        return False

    if not math.isfinite(num):
        logger.warning("Invalid number: value is not finite (%r)", num)

        return False

    return True
