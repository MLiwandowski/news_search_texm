import json
from difflib import SequenceMatcher
from typing import List
from bs4 import BeautifulSoup
import requests
import schedule
import time

# Define your keywords
KEYWORDS = ["keyword1", "keyword2", "keyword3"]

# Define your headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
}

def get_data_ixbt(file_path: str, keywords: List[str]) -> None:
    # Your code for collecting and processing data from iXBT
    
def get_data_gagadget(file_path: str, keywords: List[str]) -> None:
    # Your code for collecting and processing data from Gagadget

def collect_and_process_data():
    # Call the functions to collect and process the data
    get_data_ixbt('articles_url_list_1.txt', KEYWORDS)
    get_data_gagadget('articles_url_list_2.txt', KEYWORDS)

    # Combine and filter the data
    with open('result1.json', 'r', encoding="utf-8") as file1, \
            open('result2.json', 'r', encoding="utf-8") as file2:
        data1 = json.load(file1)
        data2 = json.load(file2)
    combined_data = data1 + data2

    result_all = []
    for article in combined_data:
        # Check for duplicates or similar articles
        duplicate = False
        for existing_article in result_all:
            similarity = SequenceMatcher(None, article['article_text'], existing_article['article_text']).ratio()
            if similarity > 0.7:
                duplicate = True
                break
        if not duplicate:
            result_all.append(article)

    # Write the combined data to result_all.json
    with open('result_all.json', 'w', encoding="utf-8") as outfile:
        json.dump(result_all, outfile, indent=4, ensure_ascii=False)

def publish_news():
    # Code to publish news every 5-6 minutes
    # Adjust this code to publish the news in your desired way
    pass

# Schedule the data collection and processing every hour
schedule.every().hour.do(collect_and_process_data)

# Schedule the news publication every 5-6 minutes
schedule.every(5).to(6).minutes.do(publish_news)

# Run the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)
