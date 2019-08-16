# Vietcetera Analytics Bot

A bot integration for Vietcetera's Slack that pulls real-time data from Google Analytics Core Reporting API. 

## Usage:

@stats-bot help 

### Get various data points
_Format_ @stats-bot count (metric) [optional] from (starttime) to (endtime)

<!-- @stats-bot goal (number) (metric) by (dimension) -->

Examples:
@stats-bot count newUsers from 14daysago to today
@stats-bot count pageviews from 100daysago to today
@stats-bot count users

### Get number of views on a specific article by time period
_Format_ @stats-bot views (url slug - everything after vietcetera.com) [optional] from (starttime) to (enddtime)

@stats-bot views /en/yellow-fever-in-modern-day-vietnam-when-asia-is-like-disneyland/ from 3daysago to today

if (starttime) and (endtime) are left out, the default range will be past 7 days

### Graph data points
_Format_ @stats-bot graph (metric) [optional] from (starttime) to (enddtime)

@stats-bot graph users by day from 14daysago to today

### See progress on goals
If you have a goal number in mind, say 1 million page views by the end of the month, there is a command to easily help you find out how close we are to that goal number.

@stats-bot goal 1000000 pageviews from 30daysago to today
@stats-bot goal 1000000 pageviews mtd 

> Currently at 163688 pageviews which is 16.3688% of goal.

The output will be of the format:
Currently at X (metric) which is Y % of goal. 

#### Important:
* Numbers must be without commas or periods i.e. 100,000 or 100.000 will not work.

## Available metrics:

### User
* _users_ - Total number of users (unique IDs/computers) who have initiated at least one session during the date range across all pages 
* _newUsers_ - Number of first-time users across all pages
* _percentNewUsers_  - (newUsers / sessions)
* _1dayUsers_
* _7dayUsers_
* _28dayUsers_
* _30dayUsers_

### Sessions
* _sessions_ - Total number of Sessions within the date range. A session is the period time a user is actively engaged with your website, app, etc. 
* _sessionsPerUser_
* _bounces_ - Number of visits that ended in only one pageview
* _bounceRate_ - bounces / sessions
* _sessionDuration_ 
* _avgSessionDuration_ - The average length of a Session. 

### Traffic
* _organicSearches_

### Goal Conversions
* _goal1Starts_
* _goalStartsAll_
* _goal1Completions_
* _goalCompletionsAll_
* _goal1Value_
* _goalValueAll_
* _goalValuePerSession_
* _goal1ConversionRate_
* _goalConversionRateAll_
* _goal1Abandons_
* _goalAbandonsAll_
* _goal1AbandonsRate_
* _goalAbandonRateAll_

### Page Tracking
* _entrances_
* _entranceRate_
* _pageViews_
* _pageViewsPerSession_ - Pages/Session (Average Page Depth) is the average number of pages viewed during a session. Repeated views of a single page are counted.
* _avgTimeOnPage_
* _exits_
* _exitRate_

### Site Speed
* _pageLoadTime_
* _avgPageLoadTime_
* _pageDownloadTime_
* _serverConnectionTime_

### App Tracking
* _screenViews_
* _screenViewsPerSession_
* _timeOnScreen_
* _avgScreenviewDuration_

There are more metrics that you can use to get data - the full list is at: https://ga-dev-tools.appspot.com/query-explorer/ and https://developers.google.com/analytics/devguides/reporting/core/dimsmets
