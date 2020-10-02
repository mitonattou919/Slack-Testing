import os
import json
from fastapi import FastAPI, Request

import myslackbot

# read configuration file
with open('config.json', 'r') as f:
    data = f.read()
config = json.loads(data)

token  = config.get('BOT_TOKEN')            # Bot User OAuth Access Token
secret = config.get('SIGNING_SECRET')       # Signing Secret


app = FastAPI()

my_slackbot = myslackbot.MySlackBot(token, secret)

@app.post('/event_api')
async def do_post_req(request: Request):

    # Get content-type header option from request.
    try:
        content_type = request.headers['Content-type']
    except KeyError as e:
        print(e)
        return 'Invalid request'

    if content_type == 'application/json':

        body_byte = await request.body()
        body = body_byte.decode()
        body_json = await request.json()

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



@app.get('/health_check')
async def do_get():
    return {'message': 'Hello World!'}


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))

