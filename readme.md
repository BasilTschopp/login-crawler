## Web Crawler with Login

This Python script uses Selenium and BeautifulSoup to log into a website, crawl internal pages, and save visible text content.
During the crawling process, each visited page is displayed in a browser window for easier debugging and observation.

## Run
python crawler.py

## Requirements
pip install selenium beautifulsoup4 python-dotenv

## Parameters
LOGIN_URL: URL of the login page. The crawler logs in here first.  
START_URL: Entry point for crawling after login.  
ALLOWED_PREFIX: Restricts crawling to URLs that start with this prefix.  

## env File
LOGIN_URL = 'https://.../login'   
START_URL = 'https://.../area/start'  
USERNAME  =  
PASSWORD  =  
OUTPUT_FILE    = 'filename.txt'  
ALLOWED_PREFIX = 'https://.../area'  
USER_FIELD     = username_field_id  
PASSWORD_FIELD = password_field_id  
LOGIN_BUTTON   = login_button_id  
