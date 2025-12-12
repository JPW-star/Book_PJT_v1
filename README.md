# 📚 Book Community Service (Book The Garden)

## 📖 Project Overview
사용자들이 도서 정보를 탐색하고, 감상평(Review)을 공유하며 소통할 수 있는 **도서 커뮤니티 플랫폼**입니다.
**Django REST Framework** 기반의 견고한 백엔드와 **Vue 3**를 활용한 반응형 프론트엔드로 구축되었습니다.

## 🛠 Tech Stack
*   **Backend**: Python, Django, DRF (Django REST Framework), SimpleJWT, SQLite
*   **Frontend**: Vue 3 (Composition API), Pinia, Vue Router, Axios
*   **External API**: Aladin TTB API (도서 데이터 수집)

## ✨ Key Features
*   **Auth**: 회원가입, 로그인(JWT 인증), 프로필 관리, 유저 팔로우/언팔로우
*   **Books**: 베스트셀러 도서 목록 조회, 도서 상세 정보 확인
*   **Community**: 리뷰(게시글) 작성/수정/삭제, 댓글 기능, 좋아요(Like) 기능

## 🚀 How to Run

### 1. Backend (Django)
```bash
cd back-django

# 가상환경 생성 및 실행
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 라이브러리 설치
pip install -r requirements.txt

# DB 마이그레이션
python manage.py migrate

# 초기 도서 데이터 수집 (알라딘 API -> DB)
# .env 파일에 TTB_KEY 설정 필요
python populate_books.py

# 서버 실행
python manage.py runserver
```

### 2. Frontend (Vue 3)
```bash
cd front-vue/vue-project

# 의존성 설치
npm install

# 개발 서버 실행
npm run dev
```

## 📂 Project Structure
*   `back-django/`: Django API Server (Accounts, Books, Community apps)
*   `front-vue/`: Vue.js Client Application
