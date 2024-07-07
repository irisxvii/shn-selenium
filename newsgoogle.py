from transformers import T5Tokenizer, T5ForConditionalGeneration
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time

def summarize_article(article_text):
    model_name = "t5-base"
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)

    inputs = tokenizer(article_text, return_tensors="pt", truncation=True, max_length=512)
    summary_ids = model.generate(**inputs)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return summary

def get_news_articles(source, interests):
    articles = []
    options = webdriver.ChromeOptions()
    # Replace 'path/to/chromedriver' with your actual path
    chromedriver_path = "C:\Users\Keerthana A R\selenium\chromedriver-win64\chromedriver.exe"
    #options.add_argument("chromedriver_autodownload=False")  # Avoid automatic download
    #options.add_argument("use_existing_chrome=True")  # Prefer existing Chrome instance
    try:
        user_agent = UserAgent().chrome  # Get a random user-agent string
        options.add_argument(f"user-agent={user_agent}")

        driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
        driver.get(source)

        # Wait for content to load (adjust wait time as needed)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "WwrzXb"))
        )

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Implement your logic to find articles based on interests
        for result in soup.find_all('div', class_='WwrzXb'):
            title_element = result.find('h3', class_='gnews_titleA')  # Update if needed
            if title_element:
                title = title_element.text.strip()
                url_element = result.find('a', href=True)
                if url_element and any(interest.lower() in title.lower() for interest in interests):
                    url = url_element['href']
                    article_text = ""
                    text_elements = result.find_all('p', class_='some-text-class')  # Update if needed
                    for element in text_elements:
                        article_text += element.text.strip()
                    articles.append({
                        "title": title,
                        "url": url,
                        "text": article_text
                    })

        time.sleep(5)  # Delay between requests (respectful scraping)

    except Exception as e:
        print(f"Error fetching articles from {source}: {e}")
        driver.quit()  # Close the browser window on error

    finally:
        driver.quit()  # Close the browser window regardless

    return articles

# Define your target website
source = "https://news.google.com/"

# Define your interests
interests = ["technology", "business"]

if __name__ == "__main__":
    articles = get_news_articles(source, interests)

    print("Today is Saturday, July 6, 2024 and here are the results:")
    print("=====================")
    for i, article in enumerate(articles, start=1):
        summary = summarize_article(article["text"])
        print(f"**Article {i}**")
        print(f"Title: {article['title']}")
        print(f"URL: {article['url']}")
        print(f"Summary: {summary}")
        print("---------------------")
