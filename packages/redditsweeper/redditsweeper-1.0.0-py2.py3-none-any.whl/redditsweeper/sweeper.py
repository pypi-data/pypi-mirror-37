import json
import os
import praw
import time
from colorama import Fore, Style
from datetime import datetime
from praw.config import Config
from praw.models import Comment, Submission
from prawcore.exceptions import ResponseException, OAuthException
from redditsweeper.__version__ import __version__ as version
from redditsweeper.exceptions import SweeperError
# Python 2 doesn't have JSONDecodeError in its json package
try:
    from json import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError


class Sweeper(object):
    """This class contains state information about the reddit connection and configuration options and offers methods
    to perform deletion operations.
    """
    def __init__(self, types, include, exclude, dry, user="default", keep=None, mfa=None, save=None):
        self._include = {s.lower() for s in include}
        self._exclude = {s.lower() for s in exclude}

        self._user = user
        self._dry = dry
        self._keep_after = time.time() - keep * 86400 if keep else None
        self._types = types
        self._mfa = mfa
        self._save = save

    def _connect(self):
        """Isolates the connection process, along with the user agent construction, which is prescribed strongly by
        reddit's developer guidelines.
        Connecting to an MFA-enabled account without supplying a token will return the same error as using wrong
        credentials. However, the password (which must be combined with the token) is loaded during the same process
        as the connection itself. So, if a token is given, use the Config class to peek at what the password would be,
        but stick the MFA token to the end and then pass it explicitly to the Reddit class constructor.
        """
        user_agent = "python:redditsweeper:v{}".format(version)
        try:
            if self._mfa:
                config = Config(self._user)
                password = "{}:{}".format(config.password, self._mfa)
                self._reddit = praw.Reddit(self._user, check_for_updates=False, user_agent=user_agent,
                                           password=password)
            else:
                self._reddit = praw.Reddit(self._user, check_for_updates=False, user_agent=user_agent)
        except ResponseException:
            raise SweeperError("Application ID or secret not recognized")
        except OAuthException:
            raise SweeperError("Login failed")
        self._user = self._reddit.user.me()
        print(Style.BRIGHT + "Connected as {}\n".format(self._reddit.config.username) + Style.RESET_ALL)

    def _save_item(self, item):
        if not self._save:
            return
        save = {"comments": [], "submissions": []}
        if os.path.isfile(self._save):
            try:
                with open(self._save) as fh:
                    save = json.load(fh)
            except JSONDecodeError:
                # This happens if the file is blank, for example.
                pass
        if isinstance(item, Comment):
            save["comments"].append({"permalink": item.permalink,
                                     "upvotes": item.ups,
                                     "body": item.body,
                                     "created_utc": item.created_utc})
        elif isinstance(item, Submission):
            save["submissions"].append({"permalink": item.permalink,
                                        "upvotes": item.ups,
                                        "title": item.title,
                                        "selftext": item.selftext,
                                        "created_utc": item.created_utc})
        with open(self._save, "w") as fh:
            json.dump(save, fh, sort_keys=True, indent=4)

    def _handle_item(self, item):
        if self._keep_after and item.created_utc >= self._keep_after:
            print(Style.DIM + Fore.GREEN + "\t\tSkipping due to too new" + Style.RESET_ALL)
            return
        sub = item.subreddit.display_name_prefixed.lower()

        if sub in self._exclude:
            print(Style.DIM + Fore.GREEN + "\t\tSkipping due to excluded subreddit" + Style.RESET_ALL)
            return

        if not self._include or sub in self._include:
            print(Style.BRIGHT + Fore.RED + "\t\tDeleted!" + Style.RESET_ALL)
            if not self._dry:
                item.delete()
            self._save_item(item)
        else:
            print(Style.DIM + Fore.GREEN + "\t\tSkipping due to subreddit not included" + Style.RESET_ALL)

    def _each_item(self):
        if self._types == "comments" or self._types == "both":
            print("Iterating over comments")
            for comment in self._user.comments.new(limit=1000):
                humantime = datetime.fromtimestamp(comment.created_utc).strftime("%Y-%m-%d %H:%M")
                summary = comment if len(comment.body) <= 50 else comment.body[:50].replace("\n", "") + "..."
                print("\t{}Comment{} {}:\n\t\tTime: {}\n\t\tSummary: {}".format(Style.BRIGHT, Style.RESET_ALL, comment,
                                                                                humantime, summary))
                yield comment
        if self._types == "submissions" or self._types == "both":
            print("Iterating over submissions")
            for submission in self._user.submissions.new(limit=1000):
                humantime = datetime.fromtimestamp(submission.created_utc).strftime("%Y-%m-%d %H:%M")
                print("\t{}Submission{} {}:\n\t\tTime: {}\n\t\tSummary: {}".format(Style.BRIGHT, Style.RESET_ALL,
                                                                                   submission, humantime,
                                                                                   submission.title))
                yield submission

    def run(self):
        try:
            self._connect()
            for item in self._each_item():
                self._handle_item(item)
        except KeyboardInterrupt:
            print("Stopping due to user interrupt...")
