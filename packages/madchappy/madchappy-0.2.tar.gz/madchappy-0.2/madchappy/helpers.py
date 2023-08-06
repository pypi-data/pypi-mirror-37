import requests


class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args:  # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False


def test():
    print("This is the helper module.")


def post_to_slack(thecase,
                  message="",
                  user_to_mention="",
                  slack_channel="",
                  slack_bot_name="",
                  slack_incoming_webhook=""
                  ):

    for case in switch(thecase):
        if case('generic'):
            text = "{} ({})" \
                .format(message, user_to_mention)
            break

    payload = {
        "username": slack_bot_name,
        "text": text,
        "channel": slack_channel
    }

    requests.post(slack_incoming_webhook, json=payload)


def log_message(*message):
    print(message)
