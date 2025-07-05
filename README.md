# Xbox Friends Scraper

This Python script uses Selenium to scrape the friends list off of any Xbox user's profile page. (Assuming it is public of course)

---

## Features/Utilization

- Manually login to your Xbox/Microsoft account through an automated Chrome browser.
- Navigate to a target Xbox gamertag's profile.
- Click the "Friends" tab and scrape all friend gamertags.
- Designed to be extended to scrape multiple profiles and build friend clusters.

---

## Prerequisites

- Python 3+
- Google Chrome browser (I used on **version 137.0.7151.120**)
- ChromeDriver corresponding to your Chrome version (placed in the `chromedriver-win64/` folder)
- any kind of Xbox account to use to log-in to the Xbox network

---

## Setup

1. Clone or download this repository.

2. Install Python dependencies (preferably in a virtual environment):

   ```bash
   pip install selenium
