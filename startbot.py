# -*- coding: utf-8 -*-
# Followed tutorials https://www.twilio.com/blog/2018/03/google-analytics-slack-bot-python.html
# and https://www.fullstackpython.com/blog/build-first-slack-bot-python.html

import os
import time
import re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pylab as pl
import matplotlib.lines as ln
import matplotlib.pyplot as plt
import logging
import datetime
import difflib
from slackclient import SlackClient
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.errors import HttpError
from calendar import monthrange

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

class Startbot:

    def __init__(self):
        self.slack_token = os.environ['SLACK_BOT_TOKEN']
        self.slack_client = SlackClient(self.slack_token)
        self.view_id = os.environ['VIEW_ID']

        self.SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
        self.KEY_FILE_LOCATION = 'google-credentials.json'
        self.VIEW_ID = self.view_id


        logging.getLogger('googleapicliet.discovery_cache').setLevel(logging.ERROR)

        # instantiate Slack client
        # slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
        # starterbot's user ID in Slack: value is assigned after the bot starts up
        self.starterbot_id = None

    def parse_bot_commands(self, slack_events):
        """
            Parses a list of events coming from the Slack RTM API to find bot commands.
            If a bot command is found, this function returns a tuple of command and channel.
            If its not found, then this function returns None, None.
        """
        for event in slack_events:
            if event["type"] == "message" and not "subtype" in event:
                user_id, message = self.parse_direct_mention(event["text"])
                if user_id == self.starterbot_id:
                    return message, event["channel"]
        return None, None

    def parse_direct_mention(self, message_text):
        """
            Finds a direct mention (a mention that is at the beginning) in message text
            and returns the user ID which was mentioned. If there is no direct mention, returns None
        """
        matches = re.search(MENTION_REGEX, message_text)
        # the first group contains the username, the second group contains the remaining message
        return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

    def handle_command(self, command, channel):
        return self.execute_command(command, channel)

    def execute_command(self, command, channel):
        """
            Executes bot command if the command is known
        """
        # Default response is help text for the user
        default_response = "Not sure what you mean. For help type: '@stats-bot help'"

        # Finds and executes the given command, filling in response
        response = None
        
        if command.startswith("count"): 
            metric = command.split()[1]
            response = '`{} {}`'.format(self.count(metric), metric)
        elif command.startswith("views"):
            url = command.split()[1]
            response = '`{} {}`'.format(self.views(command, url), "views")
        elif command.startswith("help"):
            response = "Usage: @stats-bot `count` (metric) `from` (starttime) `to` (endtime) \n Examples: \n @stats-bot `count` newUsers `from` 14daysago `to` today \n @stats-bot `count` pageviews `from` 100daysago `to` today \n @stats-bot `count` users \n \n @stats-bot `graph` (metric) by `dimension` `from` (starttime) `to` (endtime) \n @stats-bot `graph` users `by` day `from` 14daysago `to` today \n \n @stats-bot views (url slug - everything after vietcetera.com) [optional] from (starttime) to (enddtime) \n @stats-bot views /en/yellow-fever-in-modern-day-vietnam-when-asia-is-like-disneyland/ from 3daysago to today \n \n if (starttime) and (endtime) are left out, the default range will be past 7 days"
        elif command.startswith("graph"):
            self.graph_metric(command, channel)
        elif command.startswith("top"):
            response = self.top(command)
        elif command.startswith("goal"):
            goal_number = command.split()[1]
            metric = command.split()[2]
            number, percentage = self.set_goal_metric(goal_number, command) 
            number = str(number)
            percentage = str(percentage * 100)
            response = 'Currently at '+ number + " " + metric + " which is " + percentage + "% of goal."
        else:
            response = default_response
            # Sends the response back to the channel
        self.slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=response
        )

    def graph_metric(self, command, channel):
        response = ''
        if len(command.split())>1:
            metric = command.split()[1]
            words = command.split(' ')
            if 'by' in command and len(command.split())>3:
                pos = words.index('by')
                dimension = command.split()[pos+1]
                x, y = self.count_xy(metric, dimension, command)
                if not x[0].isdigit():
                    xtick_names = [x[0], x[1], x[2], x[3], x[4],  x[5],  x[6]]
                    my_xticks = [textwrap.fill(text,15) for text in xtick_names]
                    x = np.array([0, 1, 2, 3, 4, 5, 6])
                    plt.xticks(x, my_xticks, rotation=45)
                    y = np.array([y[0], y[1], y[2], y[3], y[4], y[5], y[6]])
                    # Stylize graph
                pl.plot(x, y, "r-") # plots the graph with red lines
                plt.ylim(ymin=0) #Sets the minimum y value to 0
                pl.grid(True, linestyle='-.') #Makes a dashed grid in the background
                plt.xlabel(dimension.capitalize()) #Capitalizes the first letter of the x-axis label
                plt.ylabel(metric.capitalize()) #Capitalizes the first letter of the y-axis label
                plt.title(metric.capitalize()+' by '+dimension.capitalize()) #Sets the title as [Metric] by [Dimension]
                plt.tight_layout() #adjusts spacing between subplots
                pl.savefig("graph.png") #saves the graph as a png file
                self.slack_client.api_call('files.upload', channels=channel, filename='graph.png', file=open('graph.png', 'rb')) #uploads the png file to slack
                pl.close()
            else: #run if the command doesn’t contain more than four words
                response='`What should {} be graphed by?`'.format(metric)
        else: #run if the command doesn’t contain more than two words
            response='`Graph what?`'

        # Sends the response back to the channel
        self.slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=response
        )


    # initialize an analytics object
    def initialize_analyticsreporting(self):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            self.KEY_FILE_LOCATION, self.SCOPES)
        analytics = build('analyticsreporting', 'v4', credentials=credentials, cache_discovery=False)
        return analytics

    # parses input and extracts and returns start and end date
    # default if none is given is one week
    def get_start_end_date(self, command):
        start_date = ''
        end_date = ''
        
        words = command.split(' ')
        
        if ' from ' in command or ' to ' in command:
            if ' from ' in command:
                pos = words.index('from')
                start_date = command.split()[pos+1]
            if ' to ' in command:
                pos = words.index('to')
                end_date = command.split()[pos+1]
        elif ' MTD ' in command or ' mtd ' in command: 
            # calculate how many days since beginning of month
            time = datetime.date.today()
            days_in_month = monthrange(time.year, time.month)[1]
            start_date = str(monthrange(time.year, time.month)[1]) + 'daysAgo'
        else:
            # default range is one week
            start_date = '7daysago'
            end_date = 'today'
            
        return start_date, end_date

    # def top(self, command):
    #     start_date, end_date = self.get_start_end_date(command)
    #     analytics = self.initialize_analyticsreporting()
    #     # try: 
    #     response = analytics.reports().batchGet(
    #         body={
    #             'reportRequests': [
    #             {
    #                 'viewId': self.view_id,
    #                 'dateRanges': [{'startDate': start_date, 'endDate': end_date}],
    #                 'metrics': [{'expression': 'ga:uniquePageviews'},
    #                             {'expression': 'ga:pageviews'}],
    #                 'dimensions': [{'name': "ga:country"}],
    #                 "dimensionFilterClauses": [{
    #                     'filters': [{"dimensionName": "ga:pagePath", 'expressions': ['ga:pagePath'] }]
    #                 }]
    #             }]
    #         }
    #     ).execute()
            
    #     # except HttpError:
    #     #     return "Unable to get top pages"

    #     """
    #     Parse the data to something readable and return it.
    #     :return: dictionary with data
    #     """
    #     report = response['reports']
    #     metricHeaderEntries = report[0]['columnHeader']['metricHeader']['metricHeaderEntries']
    #     totals = report[0]['data']['totals']
    #     unique = totals[0]['values'][0]
    #     pageviews = totals[0]['values'][1]

    #     data = {}
    #     data[metricHeaderEntries[0]['name']] = unique
    #     data[metricHeaderEntries[1]['name']] = pageviews
        
    #     return data
        


    # return number of pageviews/sessions with option for date range
    def count(self, command):
        start_date, end_date = self.get_start_end_date(command)
        
        analytics = self.initialize_analyticsreporting()
        try: 
            response = analytics.reports().batchGet(
                body={
                    'reportRequests': [
                    {
                        'viewId': self.VIEW_ID,
                        'dateRanges': [{'startDate': start_date, 'endDate': end_date}],
                        'metrics': [{'expression': 'ga:{}'.format(command)}]
                    }]
                }
            ).execute()
        except HttpError:
            return "Unknown metric:"

        answer = response['reports'][0]['data']['totals'][0]['values'][0]
        # print (answer)
        return answer

    def set_goal_metric(self, number, command):
        # first get the current amount using the count function
        metric = command.split()[2]
        current_number = self.count(metric)
        # print (current_number)
        goal_percentage = (int(current_number)/int(number))
        return current_number, goal_percentage
        # return 0

    def views(self, command, url):
        start_date, end_date = self.get_start_end_date(command)
        analytics = self.initialize_analyticsreporting()
        try: 
            response = analytics.reports().batchGet(
                body={
                    'reportRequests': [
                    {
                        'viewId': self.VIEW_ID,
                        'dimensions': [
                            {
                            "name": "ga:pagePath"
                            }
                        ],
                        'dateRanges': [{'startDate': start_date, 'endDate': end_date}],
                        'metrics': [ { "expression": "ga:pageviews" } ],
                        "dimensionFilterClauses": [ { "filters": [ { "operator": "EXACT", "dimensionName": "ga:pagePath", "expressions": url } ] } ]
                    }]
                }
            ).execute()
        except HttpError:
            return "Unknown metric:"

        answer = response['reports'][0]['data']['totals'][0]['values'][0]
        # print(response)
        return answer

    # configure count function to plot x y coordinates with matplotlib
    def count_xy(self, metric, dimension, command):
        start_date, end_date = self.get_start_end_date(command)
        analytics = self.initialize_analyticsreporting()
        response = analytics.reports().batchGet(
            body={
                'reportRequests': [
                {
                    'viewId': self.VIEW_ID,
                    'dateRanges': [{'startDate': start_date, 'endDate': end_date}],
                    'metrics': [{'expression': 'ga:{}'.format(metric)}],
                    'dimensions': [{'name':'ga:{}'.format(dimension)}]

                }]
            }
        ).execute()
        answer = response['reports'][0]['data']['rows']
        if not answer[0]['dimensions'][0].isdigit():
            answer = sorted(answer, key=lambda x: float(x['metrics'][0]['values'][0]), reverse=True)
        yArray=[]
        for step in range(0, len(answer)):
            yArray.append(float(answer[step]['metrics'][0]['values'][0]))
        xArray=[]
        for step in range(0, len(answer)):
            xArray.append(answer[step]['dimensions'][0])
        return xArray, yArray
    

    def run(self):
        
        if self.slack_client.rtm_connect(with_team_state=False):
            print("Starter Bot connected and running!")
            # Read bot's user ID by calling Web API method `auth.test`
            self.starterbot_id = self.slack_client.api_call("auth.test")["user_id"]
            while True:
                command, channel = self.parse_bot_commands(self.slack_client.rtm_read())
                if command:
                    self.handle_command(command, channel)
                time.sleep(RTM_READ_DELAY)
        else:
            print("Connection failed. Exception traceback printed above.")
