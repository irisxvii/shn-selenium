from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager  # Replace with your browser's driver
from bs4 import BeautifulSoup

def get_news_articles(sources, interests):
    articles = []
    options = Options()
    options.binary_location = ChromeDriverManager().install()  # Set ChromeDriver path

    # Create Chrome webdriver instance (replace with desired browser's driver if needed)
    driver = webdriver.Chrome(options=options)

    for source in sources:
        driver.get(source)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find relevant articles based on interests (adjust selectors as needed)
    for article in soup.find_all('article'):
        title_element = article.find('h2', class_='some-title-class')  # Replace with specific class
        if title_element:
            title = title_element.text.strip()
            url = article.find('a', href=True)['href']

    # Check if title contains any user interest keywords
    if any(interest.lower() in title.lower() for interest in interests):
        article_text = ""

    # Extract article text from the page (adjust selectors as needed)
    text_elements = article.find_all('p', class_='some-text-class')  # Replace with specific class
    for element in text_elements:
        article_text += element.text.strip()

    # Optionally, use requests to fetch full article content if needed
    # article_response = requests.get(url)
    # article_text = article_response.text  # Extract text from response

    articles.append({
        "title": title,
        "url": url,
        "text": article_text
    })

    driver.quit()  # Close the browser window
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
