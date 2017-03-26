import os

from robobrowser import RoboBrowser

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
        url_book_list = "/account/my-ebooks"
        url_free_learning = "/packt/offers/free-learning"
        pattern_free_ebook = "/freelearning-claim/"
        form_id = "packt-user-login-form"

        browser = RoboBrowser(user_agent=CUSTOM_USER_AGENT, parser="lxml")
        browser.open(URL_DOMAIN + url_free_learning)

        login_form = browser.get_form(id=form_id)
        login_form["email"].value = self.login
        login_form["password"].value = self.password

        browser.submit_form(login_form)

        url_link = None
        opener = browser.find(class_="twelve-days-claim")
        if opener is not None:
            url_link = opener.attrs["href"]

        if url_link is None:
            return {"status": "fail", "reason": "Unable to get the free ebook url."}

        browser.open(URL_DOMAIN + url_book_list)
        last_ebook_title = browser.find(class_="product-line").attrs["title"]

        browser.open(URL_DOMAIN + url_free_learning)
        dotd_title = browser.find(class_="dotd-title").h2.text.strip()

        browser.open(URL_DOMAIN + url_link)
        new_ebook_title = browser.find(class_="product-line").attrs["title"]
        message = "The ebook '" + new_ebook_title + "' has been donwloaded."
        if last_ebook_title == new_ebook_title:
            message = "You already had this ebook: " + dotd_title + "."
        return {"status": "success", "content": message}



    # def tester(self) -> None:
    #     print("tester")
