import requests
import json
from bs4 import BeautifulSoup
import time
import contextlib
from random import randrange
from typing import List

headers = {
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
}

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
