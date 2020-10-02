import os
import json
from flask import Flask, request

import myslackbot

# read configuration file
with open('config.json', 'r') as f:
    data = f.read()
config = json.loads(data)

token  = config.get('BOT_TOKEN')            # Bot User OAuth Access Token
secret = config.get('SIGNING_SECRET')       # Signing Secret


app = Flask(__name__)

my_slackbot = myslackbot.MySlackBot(token, secret)

@app.route('/event_api', methods=['POST'])
def do_post_req():

    # Get content-type header option from request.
    try:
        content_type = request.headers['Content-type']
    except KeyError as e:
        print(e)
        return 'Invalid request'

    if content_type == 'application/json':

        body = request.get_data(as_text=True)
        body_json = request.get_json(silent=True)

        # for Slack URL verification.
        try:
            if body_json['type'] == 'url_verification':
                return body_json['challenge'], 200
        except KeyError as e:
            print(e)
            return 'Invalid request'


        # Get headers from request.
        try:
            x_slack_signature = request.headers['X-Slack-Signature']
            x_slack_request_ts = request.headers['X-Slack-Request-Timestamp']
        except KeyError as e:
            print(e)
            return 'Invalid request'

        # Verify request by Signing Secret and X-Slack-Signature.
        try:
            my_slackbot.verify_auth(body, x_slack_signature, x_slack_request_ts)
        except ValueError as e:
            print(e)
            return 'Authorization failed.', 200

        # Get slack event from request.
        try:
            channel_id = body_json['event']['channel']
            event_text = body_json['event']['text']
            team_id    = body_json['team_id']
            user_id    = body_json['event']['user']
        except KeyError as e:
            print(e)
            return 'Invalid request'

        # omit bot id from event text.
        user_text = event_text[14:].lstrip()

        my_slackbot.send_simplemsg(channel_id, user_text)


    return 'OK', 200



if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))

