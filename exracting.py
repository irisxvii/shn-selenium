from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()  

url = "https://edition.cnn.com"
driver.get(url)

#Find all elements with the class "container__headline-text"
headlines = driver.find_elements(By.CLASS_NAME, "container__headline-text")

# Extract the text content from each headline element
extracted_headlines = [headline.text for headline in headlines]

# Similar logic can be applied to extract summaries if available, 
# replacing "news-headline" with the appropriate class/ID for summaries.

extracted_headlines = [...]  # List of scraped headlines
extracted_summaries = [...]  # List of scraped summaries (if available)

import csv

with open("scraped_news.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Headline", "Summary"])  # Header row
    for headline, summary in zip(extracted_headlines, extracted_summaries):
        writer.writerow([headline, summary])  # Write each headline-summary pair


