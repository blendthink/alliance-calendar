import argparse


def receive_argument_month() -> int:
    parser = argparse.ArgumentParser('This program registers holidays for the specified month in google calendar')
    parser.add_argument('--month', required=True, type=int, help='The month you want to register a holiday')
    args = parser.parse_args()
    return args.month
