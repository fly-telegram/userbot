# Fly-telegram UserBot
# this code is licensed by cc-by-nc (https://creativecommons.org/share-your-work/cclicenses)

import argparse


def parse() -> argparse.Namespace:
    """
    Parses command-line arguments using argparse.

    Returns:
        argparse.Namespace: A namespace containing the parsed arguments.

    The function defines two command-line arguments:

    * `--session-string`: Allows starting a userbot via a session string.
    * `--no-logo`: Disables the logo in the console.
    """
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

    parser.add_argument(
        "--test",
        action="store_true",
        help="In telegram test server",
    )
    
    return parser.parse_args()
