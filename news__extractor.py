import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime, timedelta

# Initialize Chrome WebDriver with headless option
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

# Dictionary to store the news data
dct__df = {'title': [], 'summary': [], 'publication_date': [], 'source': [], 'url': []}

def func__ext_urls__bbc():
    url__bbc = 'https://www.bbc.com/news'
    soup = BeautifulSoup(requests.get(url__bbc).text, 'html.parser')
    news__urls = list(set([f"https://www.bbc.com{item['href']}" for item in soup.find_all('a', href=True) if item['href'].startswith('/news/articles/') and not item['href'].startswith('/news/av/')]))[:20]
    return news__urls

def func__ext_urls__cnn():
    url__cnn = "https://www.cnn.com"
    soup = BeautifulSoup(requests.get(url__cnn).text, 'html.parser')
    news__urls = list(set([url__cnn + link['href'] if link['href'].startswith('/') else link['href'] for link in soup.find_all('a', href=True) if f'/{datetime.now().year}/' in link['href'] and 'video' not in link['href']]))[:20]
    return news__urls

def preprocess_summary(text, max_sentences=4):
    soup = BeautifulSoup(text, 'html.parser')
    paragraphs = [p.text.strip() for p in soup.find_all('p') if p.text.strip()]
    combined_text = ' '.join(paragraphs)
    
    # Remove extra spaces and newlines
    combined_text = re.sub(r'\s+', ' ', combined_text).strip()
    
    # Split into sentences and limit to max_sentences
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', combined_text)
    summary = ' '.join(sentences[:max_sentences])
    
    return summary

def func__ext_news__bbc(url):
    try:
        driver.get(url)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        published_datetime = re.findall(r'<time class="sc-2b5e3b35-2 fkLXLN">(.*?)</time>', str(page_source))[-1]
        published_dt = int(re.findall(r'\d+\.?\d*', published_datetime)[-1])
        published_td = str(published_datetime.split(' ')[1])
        timedelta__param_args = {
            'weeks': published_dt if published_td in ['week', 'weeks'] else 0,
            'days': published_dt if published_td in ['day', 'days'] else 0,
            'hours': published_dt if published_td in ['hour', 'hours'] else 0,
            'minutes': published_dt if published_td in ['minute', 'minutes'] else 0,
            'seconds': published_dt if published_td in ['second', 'seconds'] else 0
        }
        dt__td = timedelta(**timedelta__param_args)
        dt__dtn = datetime.now()
        dt__dt = (dt__dtn - dt__td).date().strftime("%Y-%m-%d")
        title = soup.title.string if soup.title else 'No Title'
        summary = preprocess_summary(page_source)
        publication_date = dt__dt
        source = 'BBC'
        return {'title': title, 'summary': summary, 'publication_date': publication_date, 'source': source, 'url': url}
    except Exception as e:
        print(f"Error processing BBC article at {url}: {e}")
        return None

def func__ext_news__cnn(url):
    try:
        soup = BeautifulSoup(requests.get(url).content, 'html.parser')
        title = soup.title.string if soup.title else 'No Title'
        summary = preprocess_summary(soup.prettify())
        publication_date = "-".join(url.split('/')[3:6])
        source = 'CNN'
        return {'title': title, 'summary': summary, 'publication_date': publication_date, 'source': source, 'url': url}
    except Exception as e:
        print(f"Error processing CNN article at {url}: {e}")
        return None

# Fetch news URLs from BBC and CNN
news__urls__bbc = func__ext_urls__bbc()
news__urls__cnn = func__ext_urls__cnn()
news__urls = news__urls__bbc + news__urls__cnn

# Extract news data from each URL
for url in news__urls:
    try:
        if 'bbc.com' in url:
            dct__func = func__ext_news__bbc(url)
        elif 'cnn.com' in url:
            dct__func = func__ext_news__cnn(url)
        if dct__func:  # Only append if extraction was successful
            dct__df['title'].append(dct__func['title'])
            dct__df['summary'].append(dct__func['summary'])
            dct__df['publication_date'].append(dct__func['publication_date'])
            dct__df['source'].append(dct__func['source'])
            dct__df['url'].append(dct__func['url'])
    except Exception as e:
        print(f"Failed to process {url}: {e}")

# Quit the WebDriver
driver.quit()

# Convert the dictionary to a DataFrame and save to CSV
df__csv = pd.DataFrame(dct__df).drop_duplicates(subset=['title', 'summary', 'url']).reset_index(drop=True)
df__csv.to_csv('news_articles.csv', index=False)
