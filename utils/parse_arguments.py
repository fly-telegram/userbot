# Fly-telegram UserBot
# this code is licensed by cc-by-nc (https://creativecommons.org/share-your-work/cclicenses)

import argparse


def parse() -> dict:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--session-string",
        dest="session_string",
        action="store",
        type=str,
        help="Allows you to start a userbot via session string.",
        required=False,
    )
    parser.add_argument(
        "--no-logo",
        action="store_true",
        help="Disables the logo in the console.",
    )

    args = parser.parse_args()
    return args
