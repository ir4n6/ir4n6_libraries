# The most basic of scripts to push messsages into Slack via a channel webhook
# In order to use this, you'll need to create an App in Slack, activate Incoming Webhooks
#  for the app and Add New Webhook to Workspace
#  The resulting Webhook URL needs to passed in with the function call
#  This program can also call the webhook url from a config file

import requests

def call_slack(message, webhook_url, handle_error=0):
    headers = {'Content-Type': 'application/json'}
    r = requests.post(webhook_url, json=message, headers=headers)
    if handle_error:
        if not r.status_code == 200:
            return 1, "Error sending message to Webhook URL: {}".format(webhool_url)
        else:
            return 0, None

if __name__ == '__main__':
    import configparser
    config = configparser.ConfigParser()
    config.read("config/configSettings.txt")
    slack_webhook = config.get("Slack", "webhook_url")

    message = {'text': 'Test from ir4n6_slack_webhook.py'}
    call_slack(message, slack_webhook)
