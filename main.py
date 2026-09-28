from connection.mt5_connection import init_mt5, deinit_mt5


def main():
    if not init_mt5():
        return

    try:
        # Your main logic here
        pass

    finally:
        deinit_mt5()


if __name__ == "__main__":
    main()
