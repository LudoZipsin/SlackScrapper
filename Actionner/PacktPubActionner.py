import os

from robobrowser import RoboBrowser
from bs4 import BeautifulSoup
import requests
import sys

from .Actionner import Actionner


ENV_LOGIN = "PACKTPUB_LOGIN"
ENV_PASS = "PACKTPUB_PASS"

URL_DOMAIN = "https://www.packtpub.com"
CUSTOM_USER_AGENT = "Mozilla/5.0"


class PacktPubActionner(Actionner):
    def __init__(self):
        Actionner.__init__(self)
        self.login = os.environ.get(ENV_LOGIN)
        self.password = os.environ.get(ENV_PASS)

    def fetch_free_learning(self) -> dict:
        url_free_learning = "/packt/offers/free-learning"
        pattern_free_ebook = "/freelearning-claim/"
        form_id = "packt-user-login-form"

        browser = RoboBrowser(user_agent=CUSTOM_USER_AGENT, parser="lxml")
        browser.open(URL_DOMAIN + url_free_learning)

        login_form = browser.get_form(id=form_id)
        login_form["email"].value = self.login
        login_form["password"].value = self.password

        browser.submit_form(login_form)

        response = requests.get(URL_DOMAIN + url_free_learning, headers={'User-Agent': CUSTOM_USER_AGENT})
        soup = BeautifulSoup(response.text, "html.parser")
        url_link = None
        for link in soup.find_all('a'):
            if pattern_free_ebook in str(link.get('href')):
                url_link = link.get('href')
                browser.open(URL_DOMAIN + url_link)
                return {"status": "success", "content": "One ebook as been downloaded."}
        if url_link is None:
            return {"status": "fail", "reason": "Unable to get the free ebook url."}



    # def tester(self) -> None:
    #     print("tester")