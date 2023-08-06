"""This module contains application entrypoints for using the library from the command line.
"""
import colorama
import configargparse
import os
from colorama import Fore, Style
from redditsweeper.__version__ import __version__ as version
from redditsweeper.sweeper import Sweeper
from redditsweeper.exceptions import SweeperError


def check_subreddits(subreddits):
    # configargparse returns [""] for a value of [], so go ahead and convert it into an empty list
    if subreddits == [""] or subreddits is None:
        return []
    for sub in subreddits:
        if not sub.startswith("r/"):
            raise SweeperError("Subreddit entry \"{}\" must be of format r/subredditname".format(sub))
    return subreddits


def main():
    colorama.init()

    parser = configargparse.ArgumentParser(description="Cleans up old reddit comments periodically.",
                                           default_config_files=["redditsweeper.cfg"],
                                           auto_env_var_prefix="redditsweeper_")
    parser.add("-c", "--config", is_config_file=True, help="Config path if not redditsweeper.cfg")
    parser.add("-d", "--dry", help="Dry run (don't delete messages)", action="store_true")
    parser.add("-e", "--exclude", nargs="*", help="Subreddits to exclude from deletion.")
    parser.add("-i", "--include", nargs="*", help="Subreddits to include for deletion. Leave blank to include all.")
    parser.add("-k", "--keep", help="Keep comments than the given number (in days)", type=int)
    parser.add("-m", "--mfa", help="MFA token, if MFA is enabled")
    parser.add("-s", "--savefile", help="If set, writes deleted items to a JSON file")
    parser.add("-t", "--types", help="Item type to delete (comment, submission, both)", default="both")
    parser.add("-u", "--user", help="User in praw.ini if not default", default="default")
    args = parser.parse_args()

    try:
        inclusions = check_subreddits(args.include or [])
    except SweeperError as err:
        print("{}Error:{} {}".format(Fore.RED, Style.RESET_ALL, err))
        return
    
    try:
        exclusions = check_subreddits(args.exclude or [])
    except SweeperError as err:
        print("{}Error:{} {}".format(Fore.RED, Style.RESET_ALL, err))
        return

    print(Style.BRIGHT + "Starting redditsweeper v{}".format(version) + Style.RESET_ALL)
    print("{}Dry run:{} {}".format(Style.BRIGHT, Style.RESET_ALL, "yes" if args.dry else "no"))
    print("{}Including:{} {}".format(Style.BRIGHT, Style.RESET_ALL, "all" if not inclusions else ", ".join(inclusions)))
    print("{}Excluding:{} {}".format(Style.BRIGHT, Style.RESET_ALL, ", ".join(exclusions) if exclusions else "none"))
    print("{}Item types:{} {}".format(Style.BRIGHT, Style.RESET_ALL,
                                      "comments and submissions" if args.types == "both" else args.types))
    if args.savefile:
        print("{}Saving to:{} {}".format(Style.BRIGHT, Style.RESET_ALL, args.savefile))
        # Since updates to the savefile need to start from scratch, check for its existence and delete if needed
        if os.path.isfile(args.savefile):
            os.unlink(args.savefile)
    print("")
    sweeper = Sweeper(args.types, inclusions, exclusions, args.dry, keep=args.keep, user=args.user,
                      mfa=args.mfa, save=args.savefile)
    sweeper.run()


if __name__ == "__main__":
    main()
