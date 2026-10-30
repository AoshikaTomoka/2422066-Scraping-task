import requests
from bs4 import BeautifulSoup
from bs4.exceptions import ParserRejectedMarkup
import time
import csv
from urllib.parse import urljoin, urlparse

url = "https://www.musashino-u.ac.jp/"

domain = 'www.musashino-u.ac.jp'

sitemap = {}

urls = [url]

visited = []

while len(urls) > 0:
    # リストの先頭からURLを取り出す
    current_url = urls.pop(0)

    # すでにアクセスしたURLはスキップ
    if current_url in visited:
        continue

    visited.append(current_url)

    try:
        # サーバーの負荷を避けるために0,5秒待機
        time.sleep(0.3)

        response = requests.get(current_url, timeout=10)

        # HTTPエラーがあれば例外にする
        response.raise_for_status()

        # HTMLを解析する
        soup = BeautifulSoup(response.content, 'html.parser')

        # ページタイトルを取得
        title_tag = soup.find('title')

        if title_tag is not None:
            title = title_tag.get_text(strip=True)
        else:
            title = "No Title" 

        # URLをキー、titleを値として辞書に保存
        sitemap[current_url] = title

        # ページ内のリンクを取得
        for link in soup.find_all('a', href=True):
            href = link['href']
            # 絶対URLに変換
            absolute_url = urljoin(current_url, href)

            # #以降を取り除く
            absolute_url = absolute_url.split('#')[0]

            # ドメインが同じか確認
            if urlparse(absolute_url).netloc == domain:

                # 未訪問で、リストにもないURLだけ追加
                if absolute_url not in visited and absolute_url not in urls:
                    urls.append(absolute_url)

    except requests.exceptions.RequestException as e:
        print('アクセスできなかった:', current_url)
        print(e)
        continue

    except ParserRejectedMarkup as e:
        print('HTMLを解析できなかった:', current_url)
        print(e)
        continue

# 辞書の内容をCSVファイルに書き込む
with open('sitemap.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['URL', 'Title'])  # ヘッダー行を書き込む
    for url, title in sitemap.items():
        writer.writerow([url, title])  # URLとタイトルを書き込む

print("サイトマップの作成が完了。sitemap.csvに保存")
print ('取得したページ数:', len(sitemap))