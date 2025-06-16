import os
import time
from urllib.parse import urljoin
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Load variables from env ---
load_dotenv(override=True)
LOGIN_URL      = os.getenv("LOGIN_URL")
START_URL      = os.getenv("START_URL")
USERNAME       = os.getenv("USERNAME")
PASSWORD       = os.getenv("PASSWORD")
OUTPUT_FILE    = os.getenv("OUTPUT_FILE", "site_texts.txt")
ALLOWED_PREFIX = os.getenv("ALLOWED_PREFIX")
USER_FIELD     = os.getenv("USER_FIELD")
PASSWORD_FIELD = os.getenv("PASSWORD_FIELD")
LOGIN_BUTTON   = os.getenv("LOGIN_BUTTON")

# --- Set up Chrome with Selenium ---
options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

# --- Perform login ---
driver.get(LOGIN_URL)
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, USER_FIELD)))

# Fill in email and password field using JS events
driver.execute_script(f"""
    let f = document.getElementById('{USER_FIELD}');
    f.focus(); f.value = arguments[0];
    f.dispatchEvent(new Event('input', {{ bubbles: true }}));
    f.dispatchEvent(new Event('change', {{ bubbles: true }}));
""", USERNAME)
driver.execute_script(f"""
    let f = document.getElementById('{PASSWORD_FIELD}');
    f.focus(); f.value = arguments[0];
    f.dispatchEvent(new Event('input', {{ bubbles: true }}));
    f.dispatchEvent(new Event('change', {{ bubbles: true }}));
""", PASSWORD)

# Click the login button
login_btn = driver.find_element(By.CSS_SELECTOR, LOGIN_BUTTON)
driver.execute_script("arguments[0].click();", login_btn)
time.sleep(4)

# --- Track visited URLs to prevent loops ---
visited = set()

# --- Extract visible text and page title from HTML ---
def extract_text_with_title(html):
    soup = BeautifulSoup(html, "html.parser")

    # Get page title
    title = soup.title.string.strip() if soup.title and soup.title.string else "Untitled"
    title = title[:100].replace("\n", " ").strip()

    # Remove unwanted elements
    for tag in soup(["script", "style", "nav", "footer", "header", "noscript"]):
        tag.decompose()

    # Get visible text only
    text = soup.get_text(separator="\n", strip=True)
    return title, text

# --- Recursive crawler function with error handling ----
def crawl_with_selenium(url, output_handle):
    if url in visited or not url.startswith(ALLOWED_PREFIX):
        return
    visited.add(url)

    try:
        driver.get(url)
        time.sleep(2)
        html = driver.page_source
        title, text = extract_text_with_title(html)

        # Write page title and text to file
        output_handle.write("\n" + "="*30 + "\n")
        output_handle.write(title + "\n")
        output_handle.write("="*30 + "\n\n")
        output_handle.write(text + "\n\n")

        # Find and follow internal links
        soup = BeautifulSoup(html, "html.parser")
        for a in soup.find_all("a", href=True):
            next_url = urljoin(url, a["href"])
            if next_url.startswith(ALLOWED_PREFIX):
                crawl_with_selenium(next_url, output_handle)

    except Exception as e:
        print(f"Error while processing {url}: {e}")

# --- Start crawling process ---
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    crawl_with_selenium(START_URL, f)

print(f"\nCrawling complete. Content saved in: {OUTPUT_FILE}")
