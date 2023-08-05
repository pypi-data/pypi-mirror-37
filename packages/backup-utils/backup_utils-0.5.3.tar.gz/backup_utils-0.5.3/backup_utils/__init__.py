import argparse
from .Backup import Backup

__all__ = [Backup.__class__.__name__, "main"]
__VERSION__ = "0.5.3"
__AUTHOR__ = "Oprax <oprax@me.com>"


def main():
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument(
        "-v", "--version", action="version", version="%(prog)s " + __VERSION__
    )
    parser.add_argument("-r", "--run", action="store_true", help="Create a new backup")
    parser.add_argument(
        "--test-notifier",
        action="store_true",
        help="Send a notification to test notifier settings",
    )
    parser.add_argument(
        "-d",
        "--dir",
        required=False,
        action="append",
        help="Add a new directory to the backup list, so next run it will be backup",
    )
    args = parser.parse_args()
    bak = Backup()
    if args.dir:
        bak.add_dir(args.dir)
    elif args.test_notifier:
        bak.notify(
            "Hi, your notifier settings is working !",
            attachments={"test.log": b"this is a test"},
        )
    else:
        bak.run()
