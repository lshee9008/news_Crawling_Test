import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = 'https://www.mk.co.kr'
TARGET_URL = 'https://www.mk.co.kr/news/economy/'
HEADERS = {'User-Agent': 'Mozilla/5.0'}

# 메인 페이지 요청
res = requests.get(TARGET_URL, headers=HEADERS)
soup = BeautifulSoup(res.text, 'html.parser')

# 뉴스 섹션 가져오기
articles_section = soup.select_one('section.news_sec.best_view_news_sec')
news_items = articles_section.select('li.news_node a.news_item')

results = []

for item in news_items:
    try:
        # 제목과 링크 추출
        title = item.select_one('h3.news_ttl').text.strip()
        link = urljoin(BASE_URL, item['href'])

        # 개별 기사 요청
        article_res = requests.get(link, headers=HEADERS)
        article_soup = BeautifulSoup(article_res.text, 'html.parser')

        # 본문 추출
        content_tag = article_soup.select_one('div.news_cnt_detail_wrap')  # 실제 클래스명 확인 필요
        if content_tag:
            content_text = content_tag.get_text(separator=' ', strip=True)
            content = content_text[:200] + '...' if len(content_text) > 200 else content_text
        else:
            content = '본문 없음'

        # 이미지 추출
        img_tag = content_tag.select_one('img') if content_tag else None
        if img_tag and img_tag.has_attr('src'):
            img_url = urljoin(BASE_URL, img_tag['src'])
        else:
            og_img_tag = article_soup.select_one('meta[property="og:image"]')
            img_url = og_img_tag['content'] if og_img_tag and og_img_tag.has_attr('content') else '이미지 없음'

        # 결과 저장
        results.append({
            'title': title,
            'link': link,
            'content': content,
            'image': img_url
        })

    except Exception as e:
        print(f"[❌ 오류 발생] 링크: {link}, 오류 메시지: {str(e)}")

# 결과 출력
for idx, article in enumerate(results, start=1):
    print(f"[{idx}] {article['title']}")
    print(f"🔗 링크: {article['link']}")
    print(f"📝 본문: {article['content']}")
    print(f"🖼️ 이미지: {article['image']}")
    print('-' * 80)