import os
import requests
import pandas as pd
from playwright.sync_api import sync_playwright
import time
import re
import base64

# Prompt for URL and keyword
url = input("Enter Required URL Man....!! : ")
keyword = input("Enter the keyword: ")
base_url = 'https://www.anibis.ch/'

# Create main directory based on the keyword
main_directory = os.path.join('output', keyword)
os.makedirs(main_directory, exist_ok=True)

# Create directories for each price range
price_range = ['1-50', '50-100', '100-200', '200+']

# for price_range in price_ranges:
    # os.makedirs(os.path.join(main_directory, f'Items {price_range}'), exist_ok=True)
os.makedirs(os.path.join(main_directory, f'Items'), exist_ok=True)

def fetch_page_urls(page, url):
    try:
        page.goto(url, wait_until="load", timeout=60000)
        time.sleep(5)  # Wait for page to load

        # Extract URLs from the current page
        href_elements = page.query_selector_all('a.mui-style-blugjv')
        hrefs = [element.get_attribute('href') for element in href_elements]
        full_urls = [base_url + href for href in hrefs if href and href.startswith('/')]

        return full_urls
    except Exception as e:
        print(f"Error fetching page URLs: {e}")
        return []

def process_url(page, url1):
    try:
        page.goto(url1, wait_until="load", timeout=60000)
        time.sleep(2)  # Wait for page to load

        # Extract the title
        title_element = page.query_selector('h1.MuiTypography-root.MuiTypography-h5.mui-style-12qxwu3')
        title = title_element.inner_text().strip() if title_element else "Title not found"

        # Extract the price
        price_element = page.query_selector('h2.MuiTypography-root.MuiTypography-h5.mui-style-1inwisb')
        price_text = price_element.inner_text().strip().replace('.', '') if price_element else "Price not found"
        price = re.sub(r'[^\d]', '', price_text)
        price = int(price) if price else 0

        # Extract the description
        description_element = page.query_selector('div.MuiBox-root.mui-style-1m1gi3l > div.MuiBox-root.mui-style-znb5ut > span.MuiTypography-root.MuiTypography-body1.ecqlgla1.mui-style-1wn7xgy')
        description = description_element.inner_html().replace('<br>', '\n').strip() if description_element else "Description not found"

        # Clean the description
        description = re.sub(r'<[^>]+>', '', description).strip()

        # Print the extracted information
        print(f"Title: {title}")
        print(f"Price: {price}")
        print(f"Description: {description}")

        # Determine price range folder
        if price >=0:
            price_folder = 'Items'
        # elif price <= 100:
        #     price_folder = 'Price Range 50-100'
        # elif price <= 200:
        #     price_folder = 'Price Range 100-200'
        # else:
        #     price_folder = 'Price Range 200+'

        # Create a folder for the title within the appropriate price range folder
        # title_folder = os.path.join(main_directory, price_folder, title.replace('/', '_').replace('\\', '_'))
        cleaned_title = title.replace('/', '_').replace('\\', '_')

        # Modify the folder creation to include price before the title
        title_folder = os.path.join(main_directory, price_folder, f"{price} euro {cleaned_title}")

        os.makedirs(title_folder, exist_ok=True)

        # Save the information to a text file
        details_file = os.path.join(title_folder, 'details.txt')
        with open(details_file, 'w') as file:
            file.write(f"Title: {title}\n")
            file.write(f"Price: {price}\n")
            file.write(f"Description: {description}\n")

        # Create an images directory inside the title folder
        images_folder = os.path.join(title_folder, 'images')
        os.makedirs(images_folder, exist_ok=True)

        # Find and download all images
        images = page.query_selector_all("div.mui-style-15p2jc1.e1pjrd9l0 img")
        if images:
            for idx, img_tag in enumerate(images):
                img_url = img_tag.get_attribute('src')
                if img_url:
                    download_image(img_url, images_folder, idx)
        else:
            img_element = page.query_selector('img.mui-style-191q1qc')
            if img_element:
                img_url = img_element.get_attribute('src')
                if img_url:
                    download_image(img_url, images_folder, 0)
            else:
                print("Image element not found")

    except Exception as e:
        print(f"Error processing URL {url1}: {e}")

def decode_data_url(data_url):
    """Decode a data URL to raw binary data."""
    try:
        match = re.match(r'data:image/.+;base64,(.*)', data_url)
        if match:
            base64_data = match.group(1)
            return base64.b64decode(base64_data)
    except Exception as e:
        print(f"Error decoding data URL: {e}")
    return None

def download_image(img_url, folder, idx):
    """Download an image from a URL or decode if it's a data URL."""
    try:
        if img_url.startswith('data:'):
            # Handle data URL
            img_data = decode_data_url(img_url)
            if img_data:
                img_filename = os.path.join(folder, f'image_{idx+1}.jpg')
                with open(img_filename, 'wb') as img_file:
                    img_file.write(img_data)
                print(f"Downloaded {img_filename}")
        else:
            # Handle regular URL
            img_data = requests.get(img_url).content
            img_filename = os.path.join(folder, f'image_{idx+1}.jpg')
            with open(img_filename, 'wb') as img_file:
                img_file.write(img_data)
            print(f"Downloaded {img_filename}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {img_url}: {e}")

def fetch_data():
    start_time = time.time()  # Start timing
    page_number = 1
    all_urls = []

    with sync_playwright() as p:
        user_data_path = '/Users/{username}/documents/firefox/AK/Default2'  # Update this path as needed
        context = p.firefox.launch_persistent_context(user_data_path, headless=False)
        page = context.new_page()

        while True:
            # Construct URL with updated page number
            page_url = re.sub(r'page=\d+', f'page={page_number}', url)
            print(f'Fetching data from: {page_url}')
            page_urls = fetch_page_urls(page, page_url)
            
            if not page_urls:
                print("No more URLs found. Ending pagination.")
                break
            
            all_urls.extend(page_urls)
            page_number += 1

        # Save all URLs to CSV
        df = pd.DataFrame(all_urls, columns=['URL'])
        df.to_csv(os.path.join(main_directory, 'urls.csv'), index=False)
        print("Saved URLs to urls.csv")

        # Process each URL sequentially
        for url1 in all_urls:
            process_url(page, url1)

        page.close()
        context.close()
        end_time = time.time()  # End timing
        elapsed_time_seconds = end_time - start_time
        elapsed_time_minutes = elapsed_time_seconds / 60
        print(f"Total time taken: {elapsed_time_minutes:.2f} minutes")

fetch_data()
