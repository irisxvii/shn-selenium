from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Replace with path to your webdriver (e.g., chromedriver)
driver = webdriver.Chrome()

# Target URL
url = "https://news.sky.com/"

driver.get(url)

# Wait for elements to load (adjust timeout as needed)
wait = WebDriverWait(driver, 10)

# Locate articles container (replace with specific class if needed)
articles = driver.find_element(By.XPATH, "//*[@id="main"]/div/section[1]/div/div[4]/article/div/div/div/div[2]/a")
articles.click()

# Extract information from each article (modify based on element structure)
for article in articles.find_elements(By.TAG_NAME, "p"):
    headline = article.find_element(By.TAG_NAME, "h1").text
    link = article.find_element(By.TAG_NAME, "a").get_attribute("href")

    # Print or store the extracted data (headline and link)
    print(f"Headline: {headline}")
    print(f"Link: {link}")
    print("-" * 50)

driver.quit()
