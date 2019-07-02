# Followed tutorials https://www.twilio.com/blog/2018/03/google-analytics-slack-bot-python.html
# and https://www.fullstackpython.com/blog/build-first-slack-bot-python.html

import os
import time
import re
from slackclient import SlackClient
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.errors import HttpError

slack_token = os.environ['SLACK_BOT_TOKEN']
slack_client = SlackClient(slack_token)
view_id = os.environ['VIEW_ID']

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'slackbot-vietetc-0657ea58d876.json'
VIEW_ID = view_id

# instantiate Slack client
# slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    # Default response is help text for the user
    default_response = "Not sure what you mean."

    # Finds and executes the given command, filling in response
    response = None
    # This is where you start to implement more commands!
    if command.startswith("count"): 
        metric = command.split()[1]
        response = '`{} {}!`'.format(count(metric), metric)
    
    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )

# initialize an analytics object
def initialize_analyticsreporting():
  credentials = ServiceAccountCredentials.from_json_keyfile_name(
      KEY_FILE_LOCATION, SCOPES)
  analytics = build('analytics', 'v4', credentials=credentials, cache_discovery=False)
  return analytics

# return number of pageviews/sessions with option for date range
def count(metric):
    analytics = initialize_analyticsreporting()
    response = analytics.reports().batchGet(
        body={
            'reportRequests': [
            {
                'viewId': VIEW_ID,
                'dateRanges': [{'startDate': "7daysAgo", 'endDate': "today"}],
                'metrics': [{'expression': 'ga:{}'.format(metric)}]
            }]
        }
    ).execute()
    answer = response['reports'][0]['data']['totals'][0]['values'][0]
    print(response)
    return answer

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")
