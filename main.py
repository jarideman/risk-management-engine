from connection import init_mt5, deinit_mt5
from pipeline.pipeline import run_pipeline
import logging


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    logger = logging.getLogger(__name__)

    if not init_mt5():
        logger.critical("MT5 initiation failed.")

        return

    try:
        run_pipeline()

    finally:
        deinit_mt5()


if __name__ == "__main__":
    main()
