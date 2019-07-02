# Vietcetera Analytics Bot

## Usage:
@stats-bot help

@stats-bot count (metric) from (starttime) to (endtime)

Examples:
@stats-bot count newUsers from 14daysago to today
@stats-bot count pageviews from 100daysago to today

Available metrics:
* pageviews - total number of views across all pages (vietcetera.com and all its articles)
* users - total number of users (unique IDs/computers) across all pages
  * newUsers - number of first-time users across all pages
* sessions - total number of open sessions (full time span a user spends on vietcetera, from single article to multi-article browsing)
  * percentNewUsers  - (newUsers / sessions)
* bounces - number of visits that ended in only one pageview


if (starttime) and (endtime) are left out, the default range will be past 7 days
