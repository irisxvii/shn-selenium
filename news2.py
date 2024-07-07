from transformers import T5Tokenizer, T5ForConditionalGeneration
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup
import requests

def summarize_article(article_text):
    model_name = "t5-base"
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)

    inputs = tokenizer(article_text, return_tensors="pt", truncation=True, max_length=512)
    summary_ids = model.generate(**inputs)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return summary

def get_news_articles(sources, interests, headless=True):
    options = Options()
    if headless:
        options.add_argument("--headless")

    service = Service(executable_path="C:/Users/Keerthana A R/selenium/chromedriver-win64/chromedriver.exe")
    articles = []
    driver = None
    try:
        driver = webdriver.Chrome(service=service, options=options)
        for source in sources:
            driver.get(source)
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            for article in soup.find_all('article'):
                title_element = article.find('h2', class_='some-title-class')
                if title_element:
                    title = title_element.text.strip()
                    url = article.find('a', href=True)['href']

                    if any(interest.lower() in title.lower() for interest in interests):
                        article_text = ""
                        text_elements = article.find_all('p', class_='some-text-class')
                        for element in text_elements:
                            article_text += element.text.strip()

                        articles.append({
                            "title": title,
                            "url": url,
                            "text": article_text
                        })

    except Exception as e:
        print(f"Error fetching articles: {e}")
    finally:
        if driver:
            driver.quit()

    return articles

def main():
    sources = ["https://www.nytimes.com/"]
    interests = ["technology", "business"]

    articles = get_news_articles(sources, interests)

    print("Today is Saturday, July 6, 2024 and here are the results:")
    print("=====================")
    for i, article in enumerate(articles, start=1):
        summary = summarize_article(article["text"])
        print(f"**Article {i}**")
        print(f"Title: {article['title']}")
        print(f"URL: {article['url']}")
        print(f"Summary: {summary}")
        print("---------------------")

if __name__ == "__main__":
    main()
