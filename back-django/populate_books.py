import os
import django
import requests
from dotenv import load_dotenv

# 1. Django 환경 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'book_pjt.settings')
django.setup()

from books.models import Book

# 2. 환경변수 불러오기
load_dotenv()
TTB_KEY = os.environ.get('TTB_KEY')

def fetch_and_save_books():
    if not TTB_KEY or "your_" in TTB_KEY:
        print("Error: .env 파일에 올바른 TTB_KEY를 설정해주세요.")
        return

    # 알라딘 API 설정
    url = "http://www.aladin.co.kr/ttb/api/ItemList.aspx"
    params = {
        'ttbkey': TTB_KEY,
        'QueryType': 'Bestseller', # 베스트셀러
        'MaxResults': 50,          # 최대 50개
        'start': 1,
        'SearchTarget': 'Book',
        'output': 'js',
        'Version': '20131101'
    }

    print("알라딘 API로부터 도서 데이터를 가져오는 중...")
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        items = data.get('item', [])
        print(f"총 {len(items)}권의 도서를 발견했습니다.")

        for item in items:
            isbn = item.get('isbn13')
            if not isbn:
                continue
                
            book, created = Book.objects.update_or_create(
                isbn13=isbn,
                defaults={
                    'title': item.get('title', ''),
                    'author': item.get('author', ''),
                    'publisher': item.get('publisher', ''),
                    'cover': item.get('cover', ''),
                    'descriptions': item.get('description', ''),
                }
            )
            status = "Created" if created else "Updated"
            print(f"[{status}] {book.title}")
            
        print("\n도서 데이터 저장 완료!")

    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    fetch_and_save_books()
