# 🧳 AI 여행 추천 CLI 프로그램

Gemini AI와 카카오 지도 API를 활용한 여행지 추천 프로그램입니다.
날짜를 입력하면 AI가 여행 도시를 추천하고, 실제 맛집 정보까지 찾아줍니다!

## ✨ 주요 기능

- 🤖 **AI 여행지 추천**: Gemini가 날씨와 행사를 고려해 도시를 추천
- 🗺️ **실제 맛집 검색**: 카카오 지도 API로 진짜 맛집 정보 제공
- 💾 **자동 저장**: 결과를 JSON과 Markdown 파일로 저장

## 🛠️ 사용 기술

- Python 3
- Google Gemini API
- Kakao Local API
- argparse, requests, python-dotenv

## 📦 설치 방법

1. 필요한 패키지 설치

pip install google-generativeai requests python-dotenv

2. `.env` 파일 생성 후 API 키 입력

GEMINI_API_KEY=your_gemini_key
KAKAO_API_KEY=your_kakao_key

## 🚀 실행 방법
python trip.py --date 2025-12-25

## ⚠️ 주의 사항

- 🔒 `.env` 파일에는 API 키가 들어있으니 **절대 외부에 공유하지 마세요!**
- 🚫 GitHub에 올릴 때는 `.gitignore`에 `.env`를 추가하세요.
- 📝 API 키를 코드에 직접 작성하지 말고, 반드시 `.env`에서 불러오세요.
