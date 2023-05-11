# news_search_texm
script for search news texm_by

import subprocess
import asyncio
from telegram import Bot
import json
from difflib import SequenceMatcher
import time
from random import randrange

# ////////////////////////////////////////////////////////////
# Define the file path
script_path_1 = "./news_search_1.py"
script_path_2 = "./news_search_2.py"
# script_path_n... = "./news_search_n... .py"

# Run the script
subprocess.call(["python", script_path_1])
subprocess.call(["python", script_path_2])

# ////////////////////////////////////////////////////////////
# Read data from result1.json and result2.json
with open('result1.json', 'r', encoding="utf-8") as file1, \
        open('result2.json', 'r', encoding="utf-8") as file2:

    data1 = json.load(file1)
    data2 = json.load(file2)
# Combine the data and filter out duplicate or similar articles
combined_data = data1 + data2

result_all = []
for article in combined_data:
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

# ////////////////////////////////////////////////////////////////////
# Read links from articles_url_list_1.txt
with open('articles_url_list_1.txt', 'r', encoding="utf-8") as file1:
    links1 = file1.readlines()
# Read links from articles_url_list_2.txt
with open('articles_url_list_2.txt', 'r', encoding="utf-8") as file2:
    links2 = file2.readlines()
# Combine the links
all_links = links1 + links2
# Write the combined links to articles_url_list_all.txt
with open('articles_url_list_all.txt', 'w', encoding="utf-8") as outfile:
    outfile.writelines(all_links)
# ////////////////////////////////////////////////////////////////////

async def publish_articles():
    # Read data from result_all.json
    with open('result_all.json', 'r', encoding="utf-8") as file:
        data = json.load(file)

    # Initialize your Telegram bot
    bot_token = '6230573565:AAGro7qOktJvU_4hzvIFazZkT9UUDug1r8g'
    bot = Bot(token=bot_token)

    # Define your Telegram channel ID
    channel_id = '@texm_by'  # Replace with your channel ID

    # Load the previously published articles
    try:
        with open('published_articles.json', 'r', encoding="utf-8") as file:
            published_articles = json.load(file)
    except FileNotFoundError:
        published_articles = []

    # Publish articles to your Telegram channel
    new_articles = []
    delay_seconds = 500  # Customize the delay duration in seconds
    for article in data:
        article_title = article['article_title']
        article_img = article['article_img']
        article_text = article['article_text']

        # Check if the article has been previously published
        article_already_published = any(
            pub_article['article_title'] == article_title for pub_article in published_articles
        )

        if not article_already_published:
            # Generate the hyperlink for the article title
            article_title_link = f'<a href="{article_img}">{article_title}</a>'

            # Format the message text with the title and text
            message_text = f"{article_title_link}\n\n{article_text}"

            # Publish the message to your channel
            await bot.send_message(chat_id=channel_id, text=message_text, parse_mode='HTML')

            # Add the article to the published articles list
            new_articles.append(article)
            time.sleep(randrange(500, 600))

    # Update the published articles record
    published_articles.extend(new_articles)
    with open('published_articles.json', 'w', encoding="utf-8") as file:
        json.dump(published_articles, file)

# Run the publish_articles coroutine
asyncio.run(publish_articles())
# ////////////////////////////////////////////////////////////////

