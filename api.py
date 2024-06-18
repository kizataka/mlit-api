import os
import requests
from dotenv import load_dotenv

# APIキーを指定
load_dotenv()  # .envファイルの読み込み
API_KEY = os.getenv('API_KEY')

# APIのエンドポイントを指定
API_URL = "https://www.mlit-data.jp/api/v1/graphql"

# GraphQLクエリ
query = '''
query search($term: Any) {
  search(term: $term, phraseMatch: true, first: 0, size: 10) {
    totalNumber
    searchResults {
      id
      title
      dataset_id
      metadata
    }
  }
}
'''

headers = {
    "Content-Type": "application/json",
    "apikey": API_KEY
}

# 検索キーワードを指定
term = "神戸7"

payload = {
    "query": query,
    "variables": {"term": term}
}

response = requests.post(API_URL, json=payload, headers=headers)
response.raise_for_status()
data = response.json()

# ソースコードのを指定
source_code = "PORT28001010001"

# ソースコードが一致するデータの抽出
for result in data["data"]["search"]["searchResults"]:
    metadata = result["metadata"]
    if metadata.get("NGI:source_code") == source_code:
        latitude = metadata.get("NGI:latitude")
        longitude = metadata.get("NGI:longitude")
        boring_length = metadata.get("NGI:boring_length")
        
        # 抽出した情報を表示
        print(f"Title: {result['title']}")
        print(f"Latitude: {latitude}")
        print(f"Longitude: {longitude}")
        print(f"Boring Length: {boring_length}")
        break
else:
    print("指定されたソースコードに一致するデータが見つかりませんでした。")