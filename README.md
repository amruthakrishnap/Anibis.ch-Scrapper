# Anibis Web Scraper

This Python project is a web scraper designed to extract product information from Anibis. It collects product details such as title, price, and description, along with images, and organizes the data into folders based on price ranges.

## Features

- Scrapes product details (title, price, description) and images from Anibis.
- Organizes data into folders based on price ranges.
- Uses Playwright for browser automation.

## Prerequisites

- Python 3.x
- Playwright
- Requests
- Pandas
- BeautifulSoup (optional, if switching to BeautifulSoup)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/anibis-web-scraper.git
   cd anibis-web-scraper


2. **Install dependencies::**
   
   ```bash
   pip install -r requirements.txt
   
3. **Install Playwright browsers::**

   ```bash
   playwright install

  ## Usage

1. **Edit the script:**

   Update the `user_data_path` variable in the script to point to your Firefox profile. Modify the path according to your operating system. For One time you need to run Headful mode to save cookies and bypass        captcha.Then for Next Runs you can do it with headless mode. Simply Change Headless=True in the code.

   - **MacOS:**
     ```python
     user_data_path = '/Users/{username}/documents/firefox/AK/Default2'
     ```

   - **Windows:**
     ```python
     user_data_path = 'C:/Users/{username}/AppData/Roaming/Mozilla/Firefox/Profiles/your-profile'
     ```

   - **Linux:**
     ```python
     user_data_path = '/home/{username}/.mozilla/firefox/your-profile'
     ```

2. **Run the script:**

   Execute the script using Python:

   ```bash
   python scraper.py
    ```

   ## Code Overview

This Python script is designed to scrape data from a specified URL using Playwright, which allows for automated interaction with web pages. The script performs the following tasks:

1. **Fetch Page URLs:** 
   It extracts URLs from the paginated listings on the specified webpage.

2. **Process Each URL:** 
   For each URL, it extracts the title, price, and description of the product and saves this information along with images into organized folders.

3. **Save Data:** 
   Data is categorized into folders based on the product's price range:
   - "Price Range 1-50"
   - "Price Range 50-100"
   - "Price Range 100-200"
   - "Price Range >=200"

   Each product's details are saved in a text file, and images are stored in an images directory within the product's folder.

4. **Setup and Execution:** 
   The script prompts the user for a URL and handles data extraction accordingly. It also handles downloading of images, whether they are standard URLs or base64 data URLs.

## Output Structure

After running the script, the output is organized as follows:

```plaintext
<Keyword>/
├── Price Range 1-50/
│   ├── ProductTitle1/
│   │   ├── details.txt
│   │   └── images/
│   └── ProductTitle2/
│       ├── details.txt
│       └── images/
├── Price Range 50-100/
│   ├── ProductTitle3/
│   │   ├── details.txt
│   │   └── images/
│   └── ProductTitle4/
│       ├── details.txt
│       └── images/
├── Price Range 100-200/
│   ├── ProductTitle5/
│   │   ├── details.txt
│   │   └── images/
│   └── ProductTitle6/
│       ├── details.txt
│       └── images/
└── Price Range >=200/
    ├── ProductTitle7/
    │   ├── details.txt
    │   └── images/
    └── ProductTitle8/
        ├── details.txt
        └── images/

