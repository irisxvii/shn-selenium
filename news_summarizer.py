from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager  # Replace with your browser's driver
from bs4 import BeautifulSoup

def get_news_articles(sources, interests):
    driver = webdriver.Chrome(ChromeDriverManager().install())  # Replace with your browser's driver
    articles = []
    for source in sources:
        driver.get(source)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "article-list")))  # Adjust selector as needed

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        article_elements = soup.find_all('article')  # Replace with appropriate selector for article elements

        for article in article_elements:
            headline = article.find('h2', class_='headline').text.strip()  # Replace with selectors for headline and summary
            summary = article.find('p', class_='summary').text.strip()  # Replace with selectors for headline and summary
            if any(interest.lower() in headline.lower() for interest in interests):
                articles.append({"headline": headline, "summary": summary})

    driver.quit()
    return articles

from transformers import pipeline

# Use t5-base model
model_name = "t5-base"

summarization_pipeline = pipeline("summarization", model=model_name)

def summarize_articles(articles):
    summaries = []
    for article in articles:
        summary = summarization_pipeline(article["summary"], max_length=100, truncation=True)  # Adjust parameters as needed
        summaries.append({"headline": article["headline"], "summary": summary[0]['summary_text']})
    return summaries


import argparse

def main():
    parser = argparse.ArgumentParser(description="Automated News Summarizer")
    parser.add_argument("--sources", nargs="+", required=True, help="List of news source URLs")
    parser.add_argument("--interests", nargs="+", required=True, help="List of user interests")
    args = parser.parse_args()

    articles = get_news_articles(args.sources, args.interests)
    summaries = summarize_articles(articles)

    for summary in summaries:
        print(f"Headline: {summary['headline']}\nSummary: {summary['summary']}")

if __name__ == "__main__":
    main()
