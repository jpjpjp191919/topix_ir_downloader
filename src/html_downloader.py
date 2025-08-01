import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# --- Settings ---
CSV_PATH = 'data/topix_companies.csv'
SAVE_DIR = 'saved_html'
LOG_DIR = 'logs'
FAILED_URLS_LOG = os.path.join(LOG_DIR, 'failed_html_urls.csv')

def setup_driver():
    """Set up the Chrome WebDriver."""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    return driver

def download_html(driver, url, save_path):
    """Download and save the HTML of a given URL."""
    try:
        driver.get(url)
        # Wait for the page to be fully loaded
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )
        time.sleep(5)  # Additional wait for dynamic content
        html_content = driver.page_source
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        return True
    except Exception as e:
        print(f'Error downloading {url}: {e}')
        return False

def main():
    """Main function to download HTML from a list of URLs."""
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    try:
        companies = pd.read_csv(CSV_PATH)
    except FileNotFoundError:
        print(f'Error: {CSV_PATH} not found. Please create it.')
        return

    driver = setup_driver()
    failed_urls = []

    for _, row in companies.iterrows():
        ticker = row['Ticker']
        name = row['Name']
        url = row['URL']
        save_path = os.path.join(SAVE_DIR, f'{ticker}_{name}.html')

        print(f'Downloading HTML for {name} ({ticker}) from {url}...')
        if not download_html(driver, url, save_path):
            failed_urls.append({'Ticker': ticker, 'Name': name, 'URL': url})

    if failed_urls:
        failed_df = pd.DataFrame(failed_urls)
        failed_df.to_csv(FAILED_URLS_LOG, index=False)
        print(f'\nSaved {len(failed_urls)} failed URLs to {FAILED_URLS_LOG}')

    driver.quit()
    print('\nHTML download process finished.')

if __name__ == '__main__':
    main()
