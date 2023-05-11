import json
import asyncio
from telegram import Bot

# Load data from JSON file
with open('result2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Initialize Telegram bot with API token
bot = Bot('6230573565:AAGro7qOktJvU_4hzvIFazZkT9UUDug1r8g')

# Keep track of the last sent article
last_sent = ''


async def main():
    global last_sent  # use global variable
    # Loop through each article in data
    for article in data:
        # Check if the article has a different title and URL from the last sent article
        if article['article_title'] != last_sent and article['original_url'] != last_sent:
            # Create the HTML message with a link to the title and the image
            title_link = f"<a href='{article['original_url']}'>{article['article_title']}</a>"
            message = f"{title_link}\n\n{article['article_text']}"

            # Send message to Telegram channel
            await bot.send_message(chat_id='@texm_by', text=message, parse_mode='HTML', disable_web_page_preview=False)
            print('Sent message:', message)

            # Update last sent article
            last_sent = article['article_title']
            await asyncio.sleep(20)  # Wait 20 seconds before sending the next message


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
