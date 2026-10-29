import requests
from bs4 import BeautifulSoup
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
        time.sleep(0.5)

        # URLにアクセスしてHTMLを取得
        response = requests.get(current_url, timeout=10)
        response.raise_for_status()  # HTTPエラーが発生した場合に例外

        # HTMLを解析
        soup = BeautifulSoup(response.text, 'html.parser')

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

            # ドメインが同じで、まだ訪問していないURLをリストに追加
            if urlparse(absolute_url).netloc == domain and absolute_url not in visited:
                urls.append(absolute_url)

    except requests.exceptions.RequestException as e:
        print('アクセスできなかった')
        print(e)

# 辞書の内容をCSVファイルに書き込む
with open('sitemap.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['URL', 'Title'])  # ヘッダー行を書き込む
    for url, title in sitemap.items():
        writer.writerow([url, title])  # URLとタイトルを書き込む

print("サイトマップの作成が完了しました。sitemap.csvに保存されました。")
print ('取得したページ数:', len(sitemap))