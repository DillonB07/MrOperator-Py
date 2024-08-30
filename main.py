from dotenv import load_dotenv
from slack_bolt import App

import json
import os

from config import LOG_CHANNEL

load_dotenv()

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
)

def get_thread(user_id: str, dm_ts: str='', channel_ts: str=''):
    # check if it exists in the db, if not, set it
    with open("data.json", "r") as f:
        data = json.load(f)

    if data.get(user_id) is None:
        data[user_id] = {}

    for thread in data[user_id]:
            if thread["dm_ts"] == dm_ts or thread["channel_ts"] == channel_ts:
                if dm_ts != '':
                    ...
                return thread

    # if we got here, it doesn't exist
    if dm:
        data[user_id].append({"dm_ts": thread_ts, "channel_ts": None})
        return None
    else:
        # We do not want to start threads in the channel

@app.event("app_home_opened")
def handle_app_home_opened(body):
    print("hi homies")

@app.event("message")
def handle_messages(body):
    user_id = body["event"]["user"]
    ts = body["event"]["ts"]
    if body["event"]["channel_type"] == "im":
        print('Message received in DM')
        thread = get_thread(user_id, ts, True)
        if not thread:
            # There is not a channel thread associated with this message and it needs creating
            root_msg = app.client.chat_postMessage(
                channel=LOG_CHANNEL,
                text=f"New ticket created by <@{user_id}>",
            )
            thread = get_thread(user_id, ts, True)

    elif body["event"]["channel_type"] == "channel":
        print('Message received in channel')
        thread = get_thread(user_id, ts, False)
        if not thread:
            # There will not be a ticket associated with this message
            return
    else:
        # Not sure what happened here - probably will never get triggered but let's catch it anyway
        print(f'Message received in unknown channel type - {body["event"]["channel_type"]}')
        return

if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
