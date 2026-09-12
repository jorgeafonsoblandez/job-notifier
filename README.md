💼 Trade Me Job Aggregator

A lightweight Python script that searches Trade Me for
new job listings and sends a daily digest directly to your Telegram.
Perfect for staying ahead of the competition
without manually scrolling!

Features:
- Checks for specific IT and Temporary/Casual keywords.
- Filters IT jobs for Auckland or Remote work.
- Remembers previously seen jobs so you only get fresh alerts.
- Runs completely free using GitHub Actions, once a day.

How to Use:
1. Fork this repository.
2. Get your Trade Me API credentials (OAuth 1.0a) and a Telegram Bot Token/Chat ID.
3. Add these as GitHub Repository Secrets.
4. Edit config.py to match your desired job titles.
5. Enable GitHub Actions to run the daily schedule.

Notes:
- The schedule runs once a day rather than more frequently: new listings
  don't appear fast enough to justify checking more often, it keeps API
  usage low, and GitHub doesn't reliably honor high-frequency (e.g. hourly
  or more often) cron schedules anyway — runs can be delayed or skipped
  under load, which is much less noticeable at a daily cadence.
- Until the Trade Me production app is approved, TRADEME_API_BASE should
  point at the sandbox (https://api.tmsandbox.co.nz/v1), which only
  returns fixed test data — real listings require the production API base
  and production OAuth credentials.
