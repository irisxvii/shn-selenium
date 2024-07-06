from transformers import T5Tokenizer, T5ForConditionalGeneration
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup
import requests

def summarize_article(article_text):
    """
    Summarizes a given article text using the T5 model.

    Args:
        article_text: The text of the article to summarize.

    Returns:
        A string containing the summarized article.
    """

    # Replace with your model name or path to a fine-tuned model
    model_name = "t5-base"
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)

    # Preprocess article text (optional, may involve tokenization, padding, etc.)
    inputs = tokenizer(article_text, return_tensors="pt", truncation=True, max_length=512)

    # Generate summary
    summary_ids = model.generate(**inputs)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return summary

def get_news_articles(sources, interests, headless=True):
    """
    Fetches news articles from the specified sources, focusing on user interests.

    Args:
        sources: A list of news source URLs.
        interests: A list of user interests (keywords) for filtering articles.
        headless: (Optional) Whether to run Chrome in headless mode (default: True).

    Returns:
        A list of dictionaries, where each dictionary contains the title, URL, and text of a news article.
    """

    options = Options()

    # Set headless mode if desired
    if headless:
        options.add_argument("--headless")

    # Use Service to manage ChromeDriver (replace with your actual path)
    service = Service(executable_path="C:/Users/Keerthana A R/selenium/chromedriver-win64/chromedriver.exe")

    articles = []
    driver = None
    try:
        # Create Chrome webdriver instance using the options and service
        driver = webdriver.Chrome(service=service, options=options)

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
                        # ... (unchanged)

                        articles.append({
                            "title": title,
                            "url": url,
                            "text": article_text
                        })

    except Exception as e:
        print(f"Error fetching articles: {e}")
    finally:
        if driver:
            driver.quit()  # Close the browser window

    return articles

def main():
    """
    Main function to execute the news summarization process.
    """

    # Get command-line arguments (replace with argparse if needed)
    sources = ["https://www.nytimes.com/", "https://www.bbc.com/"]
    interests = ["technology", "business"]

    articles = get_news_articles(sources, interests)

    for article in articles:
        summary = summarize_article(article["text"])
        print(f"\nTitle: {article['title']}")
        print(f"URL: {article['url']}")
        print(f"Summary: {summary}\n")

if __name__ == "__main__":
    main()
