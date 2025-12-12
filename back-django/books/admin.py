from django.contrib import admin
from .models import Book

@admin.register(Book)  # 1. Book 모델을 관리자 페이지에 등록하는데, 아래 설정을 따르겠다!
class BookAdmin(admin.ModelAdmin):
    # 2. 목록 화면에 보여줄 컬럼들을 지정합니다. (이게 없으면 그냥 object (1) 처럼 나옵니다)
    list_display = ('title', 'author', 'publisher', 'isbn13')
    
    # 3. 우측 상단에 검색창을 만들고, 제목/저자/ISBN으로 검색하게 해줍니다.
    search_fields = ('title', 'author', 'isbn13')
