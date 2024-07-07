import requests
from bs4 import BeautifulSoup
from transformers import T5Tokenizer, T5ForConditionalGeneration

def summarize_article(url):
    # Web scraping
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    article_text = ''
    for paragraph in soup.find_all('p'):
        article_text += paragraph.get_text()

    # Summarization
    model_name = "t5-base"
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)

    inputs = tokenizer(article_text, return_tensors="pt", truncation=True, max_length=512)
    summary_ids = model.generate(**inputs)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return summary


text = """You may have seen that 2024's progress bar recently hit 50%. To mark that mildly terrifying milestone, we've decided to cast our eye back over the past six months and pick out our biggest tech highlights of the year so far.

There's been no shortage of those – from the arrival of Microsoft's new generation of AI-equipped Windows 11 laptops to Apple's latest iPad Pros, we've been given some real tech treats already.

You can jump straight into our list of the 11 best products we've tested so far this year below, with the list covering everything from Bluetooth speakers to OLED TVs and cameras.

Alternatively, if you're simply looking for a quick shot of buying advice in a particular tech genre, you can use the links on the left to jump to our mid-year tech roundups. They round up the highlights of 2024 so far across everything from MacBooks to wireless earbuds, and also take a look at what's coming in the next six months according to the rumor mill."""


print(summarize_article(text))