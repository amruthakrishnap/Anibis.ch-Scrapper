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
   ```bash

2. **Install dependencies::**
   
   ```bash
   pip install -r requirements.txt
   ```bash
   
3. **Install Playwright browsers::**

   ```bash
   playwright install
   ```bash


  ## Usage

1. **Edit the script:**

   Update the `user_data_path` variable in the script to point to your Firefox profile. Modify the path according to your operating system.

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
    ```bash
