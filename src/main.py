import os
import argparse
from calsyncs.caldav import CalDav
from datetime import datetime, timedelta

from scrapers.darkside_api import DarkSideAPIScraper


def parse_gym_arguments():
    parser = argparse.ArgumentParser(description="Gym Arguments")
    parser.add_argument("--start_date", default=datetime.now(), help="Start date")
    parser.add_argument(
        "--end_date", default=datetime.now() + timedelta(days=120), help="End date"
    )

    parser.add_argument("--gym-url", required=True, help="Gym base URL")
    parser.add_argument(
        "--slow", default=True, action="store_true", help="Sleep between requests"
    )

    parser.add_argument(
        "--gym-user", default=os.environ.get("GYM_USER"), help="User name"
    )
    parser.add_argument(
        "--gym-password", default=os.environ.get("GYM_PASSWORD"), help="Password"
    )

    parser.add_argument("--caldav-url", required=True, help="CalDAV URL")
    parser.add_argument("--calendar", default="Gym", help="Calendar name")
    parser.add_argument(
        "--caldav-user", default=os.environ.get("CALDAV_USER"), help="User name"
    )
    parser.add_argument(
        "--caldav-password", default=os.environ.get("CALDAV_PASSWORD"), help="Password"
    )
    return parser.parse_args()


def main():
    parser = argparse.ArgumentParser(description="Command-line Argument Parser")
    subparsers = parser.add_subparsers(title="groups", dest="group_name")
    gym_parser = subparsers.add_parser("gym", help="Gym group arguments")
    args = parse_gym_arguments()

    api = DarkSideAPIScraper(args.gym_url, args.gym_user, args.gym_password)
    cal = CalDav(
        args.caldav_url,
        args.caldav_user,
        args.caldav_password,
        args.calendar,
        args.start_date,
        args.end_date,
    )

    with api.login() as session:
        cal.sync(session.get_trainings())


if __name__ == "__main__":
    main()
