import subprocess
import asyncio
from telegram import Bot
import json
from difflib import SequenceMatcher
import time
from random import randrange

# ////////////////////////////////////////////////////////////
# Define the file path
# script_path_1 = "./news_search_1.py"
# script_path_2 = "./news_search_2.py"
# script_path_n... = "./news_search_n... .py"

# Run the script
subprocess.call(["python", script_path_1])
subprocess.call(["python", script_path_2])

# ////////////////////////////////////////////////////////////

words = ["Apple", "Blackview", "Google", "Iphone", "LG", "Lynk & Co", "Motorola", "Nintendo Switch", "Pixel", 'Realme', "Sharp","Tecno","Xiaomi", "Samsung", "Nokia", "Tesla ", "PlayStation", "смартфон"]
keywords = words

#////////////////////////////////////////////////////////////

url_ixbt = "https://www.ixbt.com/news/?show=tape"

def get_articles_urls(url):
    s = requests.Session()
    response = s.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    articles_urls = soup.find_all("h2", class_="no-margin")
    articles_urls_list = []
    for au in articles_urls:
        art_url = "https://www.ixbt.com/" + au.find("a")["href"]
        articles_urls_list.append(art_url)
    time.sleep(randrange(2, 5))
    with open("articles_url_list_1.txt", "w", encoding="utf-8") as file:
        for url in articles_urls_list:
            file.write(f"{url}\n")
    return "Работа по сбору ссылок выполнена"


def get_data(file_path, keywords):
    with open(file_path) as file:
        url_list = [line.strip() for line in file.readlines()]

    urls_count = len(url_list)
    s = requests.Session()
    result_data = []

    for idx, url in enumerate(url_list[1:25]):
        response = s.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")

        articles = soup.find_all("div", class_="b-article__header")
        article_title = articles[0].find("h1").text.strip()
        article_img = f"https://www.ixbt.com{soup.find('figure', class_='image-caption').find('img').get('src')}"

        article_text = []
        for p in soup.find_all("p"):
            article_text.append(p.text.strip().replace('\n', ''))
        article_text = '\n'.join(article_text)
        article_text = article_text[:article_text.rfind(' 2023 в ')]

        # Check if article contains any of the keywords
        if any(keyword.lower() in article_text.lower() for keyword in keywords):
            article_text = article_text.split('\n')
            # Remove everything after the publication date
            publication_date_index = next((i for i, s in enumerate(article_text) if 'Дата публикации' in s), None)
            if publication_date_index is not None:
                article_text = '\n'.join(article_text[:publication_date_index])
            else:
                article_text = '\n'.join(article_text)

            print(f"{article_title}\n{article_text}\n {article_img}\n{'#' * 10}")
            result_data.append(
                {
                    "original_url": url,
                    "article_title": article_title,
                    "article_img": article_img,
                    "article_text": article_text,
                }
            )
        else:
            print(f"Слова не найдены в статье {article_title}")
        print(f"Обработал {idx + 1}/{urls_count}")

    with open("result1.json", "w", encoding="utf-8") as file:
        json.dump(result_data, file, indent=4, ensure_ascii=False)

def main():
    get_articles_urls(url=url_ixbt)
    get_data("articles_url_list_1.txt", keywords)

if __name__ == "__main__":
    main()
# ///////////////////////////////////////////////////////////
WORDS = ["Apple", "Blackview", "Google", "Iphone", "LG", "Lynk & Co", "Motorola", "Nintendo Switch", "Pixel", 'Realme', "Sharp","Tecno","Xiaomi", "Samsung", "Nokia", "Tesla ", "PlayStation", "смартфон"]
KEYWORDS = [word.lower() for word in WORDS]

URL_IXBT = "https://gagadget.com/news/"

def get_articles_urls(url: str) -> str:
    with requests.Session() as s:
        response = s.get(url=url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")
    articles_urls = soup.find_all("span", class_="cell-title")

    articles_urls_list = []
    for au in articles_urls:
        art_url = "https://gagadget.com/" + au.find("a")["href"]
        articles_urls_list.append(art_url)
    time.sleep(randrange(2, 5))
    with open("articles_url_list_2.txt", "w", encoding="utf-8") as file:
        for url in articles_urls_list:
            file.write(f"{url}\n")
    return "Работа по сбору ссылок выполнена"


def get_data(file_path: str, keywords: List[str]) -> None:
    with open(file_path) as file:
        url_list = [line.strip() for line in file.readlines()]

    urls_count = len(url_list)
    s = requests.Session()
    result_data = []

    for idx, url in enumerate(url_list[1:25]):
        response = s.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")

        articles = soup.find_all("div", class_="l-inner")
        if articles:
            article_title = articles[0].find("h1").text.strip()
            article_img = f"https://gagadget.com{soup.find('div', class_='l-container').find('img').get('src')}"

            article_text = []
            for p in soup.find_all("p"):
                article_text.append(p.text.strip().replace('\n', ''))
            article_text = '\n'.join(article_text)
            article_text = article_text[:article_text.rfind('Источник: ')]

            # print(f"{article_title}\n{article_text}\n {article_img}\n{'#' * 10}")

            # Check if article contains any of the keywords
            if any(keyword.lower() in article_text.lower() for keyword in keywords):
                article_text = article_text.split('\n')
                # Remove everything after the publication date
                publication_date_index = next((i for i, s in enumerate(article_text) if 'Дата публикации' in s), None)
                if publication_date_index is not None:
                    article_text = '\n'.join(article_text[:publication_date_index])
                else:
                    article_text = '\n'.join(article_text)

                print(f"{article_title}\n{article_text}\n {article_img}\n{'#' * 10}")
                result_data.append(
                    {
                        "original_url": url,
                        "article_title": article_title,
                        "article_img": article_img,
                        "article_text": article_text,
                    }
                )
            else:
                print(f"Слова не найдены в статье {article_title}")
        else:
            print(f"Статья не найдена для URL: {url}")

        print(f"Обработано {idx + 1}/{urls_count}")

    with open("result2.json", "w", encoding="utf-8") as file:
        json.dump(result_data, file, indent=4, ensure_ascii=False)


def main():
    get_articles_urls(url=URL_IXBT)
    get_data("articles_url_list_2.txt", KEYWORDS)


if __name__ == "__main__":
    main()


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
    delay_seconds = 2  # Customize the delay duration in seconds
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
            time.sleep(randrange(2, 5))

    # Update the published articles record
    published_articles.extend(new_articles)
    with open('published_articles.json', 'w', encoding="utf-8") as file:
        json.dump(published_articles, file)

# Run the publish_articles coroutine
asyncio.run(publish_articles())
# ////////////////////////////////////////////////////////////////

