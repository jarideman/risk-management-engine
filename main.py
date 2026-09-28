from connection.mt5_connection import init_mt5, deinit_mt5
from pipeline.pipeline import run_pipeline


def main():
    if not init_mt5():
        return

    try:
        run_pipeline()

    finally:
        deinit_mt5()


if __name__ == "__main__":
    main()
