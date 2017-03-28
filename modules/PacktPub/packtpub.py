from yapsy.IPlugin import IPlugin
from robobrowser import RoboBrowser

import inspect
import utils
import Client
import os

MODULE_NAME = "PacktPub"


ENV_LOGIN = "PACKTPUB_LOGIN"
ENV_PASS = "PACKTPUB_PASS"

BASE_URL = "https://www.packtpub.com"
CUSTOM_USER_AGENT = "Mozilla/5.0"

SPECIFIC_ERROR_CHANNEL = "#scrapper-failure"
SUCCESS_CHANNEL = "#scrapper-success"


class PacktPubPlugin(IPlugin):

    @staticmethod
    def _initialize() -> dict:
        return {"client": Client.Client(),
                "login" : os.environ.get(ENV_LOGIN),
                "password" : os.environ.get(ENV_PASS)
        }

    def actions(self):
        print(str(utils.remove_action_to_ignore(inspect.getmembers(self,  predicate=inspect.ismethod))))
        return utils.remove_action_to_ignore(inspect.getmembers(self,  predicate=inspect.ismethod))

    def fetch_free_learning(self):
        _action_name = "fetch_free_learning"
        _max_try = 1

        _url_book_list = "/account/my-ebooks"
        _url_free_learning = "/packt/offers/free-learning"
        _form_id = "packt-user-login-form"

        # this is to prevent a little bug from packtpub that force the user to click two times on the claim e-book link
        _nbr_try = 0

        _init = self._initialize()

        # START LOGIN PROCEDURE
        browser = RoboBrowser(user_agent=CUSTOM_USER_AGENT, parser="lxml")
        browser.open(BASE_URL + _url_free_learning)

        login_form = browser.get_form(id=_form_id)
        login_form["email"].value = _init["login"]
        login_form["password"].value = _init["password"]

        browser.submit_form(login_form)
        # END LOGIN PROCEDURE. We now have credential access

        browser.open(BASE_URL + _url_book_list)
        _last_ebook = browser.find(class_="product-line").attrs["title"]
        if _last_ebook is None:
            _init["client"].channel_writer(module=MODULE_NAME, action=_action_name,
                                           message="It looks like you were unable to login.")
            utils.error(msg="Oups, an error occurs...")

        browser.open(BASE_URL + _url_free_learning)
        _url_link = browser.find(class_="twelve-days-claim")
        if _url_link is not None:
            _url_link = _url_link.attrs["href"]
        else:
            _init["client"].channel_writer(module=MODULE_NAME, action=_action_name, channel=SPECIFIC_ERROR_CHANNEL,
                                           message="Unable to get the link to claim free download.")

        _dotd_title = browser.find(class_="dotd-title").h2.text.strip()

        browser.open(BASE_URL + _url_link)
        _new_ebook = browser.find(class_="product-line").attrs["title"]
        while _new_ebook is None and _nbr_try < _max_try:
            _url_link = browser.find(class_="twelve-days-claim")
            if _url_link is not None:
                _url_link = _url_link.attrs["href"]
            else:
                _init["client"].channel_writer(module=MODULE_NAME, action=_action_name, channel=SPECIFIC_ERROR_CHANNEL,
                                               message="Unable to get the link to claim free download.")
            browser.open(BASE_URL + _url_link)
            _new_ebook = browser.find(class_="product-line").attrs["title"]

        if _new_ebook is None:
            _init["client"].channel_writer(module=MODULE_NAME, action=_action_name, channel=SPECIFIC_ERROR_CHANNEL,
                                           message="Unable to download the title.")
        else:
            if _new_ebook != _last_ebook:
                _init["client"].channel_writer(module=MODULE_NAME, action=_action_name, channel=SUCCESS_CHANNEL,
                                               message="The book '{ebook}' has been downloaded :)"
                                               .format(ebook=_new_ebook))
            else:
                _init["client"].channel_writer(module=MODULE_NAME, action=_action_name, channel=SUCCESS_CHANNEL,
                                               message="You already had the book '{ebook}'".format(ebook=_dotd_title))
        print("Success!")
