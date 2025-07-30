import requests
from bs4 import BeautifulSoup

url = 'https://www.mk.co.kr/news/economy/'
headers = {'User-Agent': 'Mozilla/5.0'}

res = requests.get(url, headers=headers)
# print(res.text)
soup = BeautifulSoup(res.text, 'html.parser')

articles = soup.select('section.news_sec.best_view_news_sec')

print(articles)