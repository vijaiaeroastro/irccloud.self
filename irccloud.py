# A Simple script to keep an irc cloud client always alive 
__author__ = "S Vijaikumar"
__email__  = "vijai@vijaikumar.in"
__copyright__ = "Copyright (C) 2021 S Vijai Kumar & EliteOfGods"
__license__ = "UNLICENSE"
__version__ = "1.0"

import requests
import sys
import traceback
import logging
from os import environ
import json
import random

class irccloud:
    """
    This is a very simple class that takes an user's irc user name
    and password as input and keeps the connection alive to emulate
    the hearbeat produced due to real browser activity.
    """
    AuthenticationToken = ""
    SessionId = ""
    KeepAliveToken = ""

    def __init__(self, email, password, debug_mode=False):
        self.email = email
        self.password = password
        self.debugging = debug_mode
        logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO)
        self.log = logging.getLogger(__name__)

    def get_authentication_token(self):
        url = "https://www.irccloud.com/chat/auth-formtoken"
        r = requests.post(url)
        response = r.json()
        if self.debugging:
            print(response)
        if response["success"]:
            self.log.info("Successfully obtained authentication token.")
            irccloud.AuthenticationToken = response["token"]
        else:
            self.log.error("Failed to obtain an authentication token.")
            irccloud.AuthenticationToken = "AUTH_FAILURE"

    def get_session_id(self):
        self.get_authentication_token()
        if irccloud.AuthenticationToken == "AUTH_FAILURE":
            return irccloud.AuthenticationToken
        else:
            login_url = "https://www.irccloud.com/chat/login"
            headers = {
                "content-type": "application/x-www-form-urlencoded",
                "x-auth-formtoken":irccloud.AuthenticationToken
            }
            login_data = {
                "email" : self.email,
                "password" : self.password,
                "token" : irccloud.AuthenticationToken
            }
            r = requests.post(login_url, data = login_data, headers = headers)
            response = r.json()
            if self.debugging:
                print(response)
            if response["success"]:
                self.log.info("Successfully obtained a session id.")
                irccloud.SessionId = response["session"]
            else:
                self.log.critical("Failed to obtain a session id.")
                irccloud.SessionId = "SESSION_FAILURE"

    def keep_alive(self):
        ua_file = open("user_agents.json", "r+")
        user_agents = json.load(ua_file)
        ua_file.close()

        stream_url = "https://www.irccloud.com/chat/stream"
        headers = {"Connection" : "keep-alive",
                   "Accept-Encoding" : "gzip,deflate,sdch",
                   "User-Agent" : random.choice(user_agents),
                   "Cookie": "session={0}".format(irccloud.SessionId),
                   "Host":"www.irccloud.com"
        }
        r = requests.post(stream_url, headers = headers)
        if self.debugging:
            print(r.json())
        if r.status_code == 200:
            irccloud.KeepAliveToken = "KA_ALIVE"
        else:
            irccloud.KeepAliveToken = "KA_DEAD"

    def runner(self):
        self.get_session_id()
        self.log.debug("   IRC Cloud Keep alive Func   ")
        if irccloud.SessionId == "SESSION_FAILURE":
            self.log.critical("Couldn't get a session initialized. Quitting... :(")
            sys.exit(0)
        else:
            self.keep_alive()
            if irccloud.KeepAliveToken == "KA_ALIVE":
                self.log.info("IRC Cloud Session is Kept alive.")
            else:
                self.log.error("IRC Cloud Session could not be Kept alive.")


if __name__ == "__main__":
    try:
        email = environ.get("IRCCLOUD_USERNAME")
        password = environ.get("IRCCLOUD_PASSWORD")
        debug_mode = False
        irc = irccloud(email, password, debug_mode)
        irc.runner()
    except KeyboardInterrupt:
        self.log.debug("Shutdown requested. Exiting script. Thank you :)")
        sys.exit(0)
    except Exception:
        traceback.print_exc(file=sys.stdout)
        sys.exit(0)
