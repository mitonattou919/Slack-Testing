#         1         2         3         4         5         6         7
#1234567890123456789012345678901234567890123456789012345678901234567890123456789

# coding: utf-8

import hashlib
import hmac
import requests
import json
import time


# [START MySlackBot]
#
# General purpose class for Slack Bot.
#
# Supported with 
#   Event-API: app_mention
#   Web-API: chat.postMessage
#
# Attributes:
#   token:  Bot User OAuth Access Token defined in slack app.
#   secret: Singning Secret defined in slack app Basic Information.
#
#         1         2         3         4         5         6         7
#1234567890123456789012345678901234567890123456789012345678901234567890123456789
class MySlackBot:

    # Slack Web-API URL.
    url_chat_post_message   = 'https://slack.com/api/chat.postMessage'
    url_chat_post_ephemeral = 'https://slack.com/api/chat.postEphemeral'
    url_chat_delete         = 'https://slack.com/api/chat.delete'


    # [ START init]
    #
    def __init__(self, token, secret):
        self.token  = token
        self.secret = secret

    # [ END init]


    # [ START verify_auth]
    # Verify request from slack by recomendation method.
    #
    # Args:
    #   body: Request body sent from slack event-api as text.
    #   signature: Request header X-Slack-Signature value
    #   timestamp: Request header X-Slack-Request-Timestamp
    # Returns:
    #   none
    # Raises:
    #   ValueError: if validation failed.
    #
    def verify_auth(self, body, signature, timestamp):

        # for debug - recording start time.
        start_time = time.time()

        # format various information with Slack specified format.
        message = f'v0:{timestamp}:{body}' 

        try:
            hash_val = hmac.new(self.secret.encode('utf-8'),
                       message.encode('utf-8'), hashlib.sha256).hexdigest()
        except e:
            print(e)

        # comparing X-Slack-Signature vs. calcurated message.
        if signature != f'v0={hash_val}':
            raise ValueError('Invalid Signature')

        # for debug - logging elapsed time.
        elapsed_time = time.time() - start_time
        print ("slack.verify_auth elapsed:{0}".format(elapsed_time) + "[sec]")

        return 'OK'

    # [ END verify_auth]


    # [ START send_simpemsg]
    # Send simple message to slack by Web-API(chat.postMessage).
    #
    # Args:
    #   channel: Destination channel-identifier from request
    #   reply_text: message text you wanna send to slack.
    # Returns:
    #   none
    # Raises:
    #   none
    #
    def send_simplemsg(self, channel, reply_text):

        # for debug - recording start time.
        start_time = time.time()

        # setting up request header.
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Authorization': 'Bearer ' + self.token
        }

        # setting up request body.
        data = {
            'channel': channel,
            'text': reply_text
        }

        # send request to Slack Web-API.
        try:
            r = requests.post(
                self.url_chat_post_message, 
                data=json.dumps(data), 
                headers=headers
            )
            print(r.text)
        
        except ConnectionError as e:
            print(e)

        except HTTPError as e:
            print(e)

        except Timeout as e:
            print(e)

        # for debug - logging elapsed time.
        elapsed_time = time.time() - start_time
        print ("slack.send_msg elapsed:{0}".format(elapsed_time) + "[sec]")

    # [ END send_simpemsg]

#         1         2         3         4         5         6         7
#1234567890123456789012345678901234567890123456789012345678901234567890123456789

