import os
import sys
import json
from slackclient import SlackClient

sys.path.append(os.path.join(os.environ["GGPATH"], "GGProject"))
from GreeterGuru import settings

slack_token = settings.SLACK_TOKEN
slack_channel = settings.SLACK_CHANNEL
slack_client = SlackClient(slack_token)
leave_channel = slack_client.api_call("channels.archive", json = {'channel': slack_channel, 'token':slack_token})
