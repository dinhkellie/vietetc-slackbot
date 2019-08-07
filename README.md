# Vietcetera Analytics Bot

## Usage:


@stats-bot help 

@stats-bot count (metric) from (starttime) to (endtime)

<!-- @stats-bot goal (number) (metric) by (dimension) -->

leaving out the start and end time will default to the past 14 days
@stats-bot count avgTimeOnPage 
    returns the number of 

Examples:
@stats-bot count newUsers from 14daysago to today
@stats-bot count pageviews from 100daysago to today

@stats-bot views /en/yellow-fever-in-modern-day-vietnam-when-asia-is-like-disneyland/ from 3daysago to today


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







if (starttime) and (endtime) are left out, the default range will be past 7 days
