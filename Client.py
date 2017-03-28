import os

from slackclient import SlackClient


ENV_TOKEN = "SCRAPPER_SLACK_TOKEN"
MAIN_ERROR_CHANNEL = "#integration-error"
MAIN_CONTACT = "Admin"


class Client:
    def __init__(self):
        self.sc = SlackClient(os.environ.get(ENV_TOKEN))

    def channel_writer(self, module: str = None, action: str = None, channel: str = None, message: str = None) -> None:
        if channel is None or message is None or action is None or module is None:
            self.sc.api_call("chat.postMessage", channel=MAIN_ERROR_CHANNEL, text="Hey {contact} An error occurs with "
                                                                                  "action '{action}' from module "
                                                                                  "'{module}'.".format(
                contact=MAIN_CONTACT, action=action, module=module))
            if message is not None:
                self.sc.api_call("chat.postMessage", channel=MAIN_ERROR_CHANNEL, text=message)
        else:
            self.sc.api_call("chat.postMessage", channel=channel, text=message)
