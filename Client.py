import os
import Actionner

from slackclient import SlackClient

# import the actionner you will use for the client
from Actionner import PacktPubActionner
# from Actionner import TestActionner


ENV_TOKEN = "SCRAPPER_SLACK_TOKEN"


class Client:
    def __init__(self):
        self.sc = SlackClient(os.environ.get(ENV_TOKEN))

    def default_method(self, action: str, relevant_method: list) -> None:
        err_msg = "There is no action '" + action + "' available for this module. Please, select one among: "
        first_line = True
        for method in relevant_method:
            if not first_line:
                err_msg = " "*len(err_msg)
            else:
                first_line = False
            print(err_msg + method)


    # define your packtpub actionner. This is the default template
    def packtpub(self, action: str) -> None:
        actionner = PacktPubActionner.PacktPubActionner()
        func = getattr(actionner, action, None)
        if func is not None:
            result = func()
            _status = result["status"]
            if _status == "success":
                self.sc.api_call("chat.postMessage", channel="#scrapper-success", text=result["content"], as_user=True)
            elif _status == "fail":
                self.sc.api_call("chat.postMessage", channel="#scrapper-failure", text=result["reason"], as_user=True)
        else:
            self.default_method(action, actionner.get_relevant_methods())


    @staticmethod
    def list_actionner() -> list:
        return [module for module in dir(Actionner) if 'Actionner' in module and module != 'Actionner']
