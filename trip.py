import argparse
import json
import os
import re
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv
import google.generativeai as genai

# ── 환경변수 로드 ──
load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
KAKAO_KEY = os.getenv("KAKAO_API_KEY")

# ── 모델 이름 (여기 한 곳에서만 관리!) ──
MODEL_NAME = "gemini-flash-latest"   # ⭐ 최신 버전 자동 연결!
genai.configure(api_key=GEMINI_KEY)


# ── 1단계: 여행지 추천 ──
def recommend_city(date: str) -> dict:
    model = genai.GenerativeModel(MODEL_NAME)

    prompt = f"""
{date}에 여행하기 좋은 대한민국 국내 도시 1곳을 추천해줘.
반드시 아래 JSON 형식으로만 답변해줘.

{{
  "recommended_city": "도시 이름",
  "weather": "예상 날씨",
  "events": ["행사1", "행사2"],
  "reason": "추천 이유"
}}
"""

    response = model.generate_content(
        prompt,
        generation_config={"response_mime_type": "application/json"}
    )
    return json.loads(response.text)


# ── 2단계: 맛집 검색 (Kakao) ──
def search_restaurants(city: str) -> list:
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {"Authorization": f"KakaoAK {KAKAO_KEY}"}
    params = {"query": f"{city} 맛집", "size": 5}

    res = requests.get(url, headers=headers, params=params)
    res.raise_for_status()

    docs = res.json().get("documents", [])
    restaurants = []
    for d in docs:
        restaurants.append({
            "name": d.get("place_name"),
            "address": d.get("road_address_name") or d.get("address_name"),
            "url": d.get("place_url"),
        })
    return restaurants


# ── 3단계: 리포트 저장 (JSON) ──
def save_report(date: str, city_info: dict, restaurants: list):
    Path("results").mkdir(exist_ok=True)

    report = {
        "date": date,
        "city_info": city_info,
        "restaurants": restaurants,
    }

    filename = f"results/report_{date}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    return filename


# ── 3-2단계: Markdown 리포트 저장 ──
def save_markdown(date: str, city_info: dict, restaurants: list):
    Path("results").mkdir(exist_ok=True)

    city = city_info["recommended_city"]
    weather = city_info["weather"]
    events = city_info["events"]
    reason = city_info["reason"]

    # 행사 목록을 줄바꿈 리스트로
    events_md = "\n".join([f"- {e}" for e in events])

    # 맛집 목록을 표로
    rest_md = "| 맛집 이름 | 주소 | 링크 |\n|---|---|---|\n"
    for r in restaurants:
        rest_md += f"| {r['name']} | {r['address']} | [바로가기]({r['url']}) |\n"

    # 전체 Markdown 조립
    md = f"""# 🧳 {date} 여행 리포트

## 📍 추천 도시: {city}

- **예상 날씨:** {weather}
- **추천 이유:** {reason}

## 🎉 주요 행사
{events_md}

## 🍜 추천 맛집
{rest_md}
"""

    filename = f"results/report_{date}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(md)

    return filename


# ── 날짜 검증 ──
def valid_date(s: str) -> str:
    try:
        datetime.strptime(s, "%Y-%m-%d")
        return s
    except ValueError:
        raise argparse.ArgumentTypeError(f"날짜 형식이 잘못됐어요: {s} (YYYY-MM-DD 형식으로!)")


# ── 메인 ──
def main():
    parser = argparse.ArgumentParser(description="여행지 추천 리포트 생성기")
    parser.add_argument("--date", type=valid_date, required=True,
                        help="여행 날짜 (예: 2025-12-25)")
    args = parser.parse_args()

    print(f"\n🔍 {args.date} 여행지를 추천받는 중...")
    city_info = recommend_city(args.date)
    city = city_info["recommended_city"]
    print(f"✅ 추천 도시: {city}")

    print(f"🍜 {city} 맛집을 검색하는 중...")
    restaurants = search_restaurants(city)
    print(f"✅ 맛집 {len(restaurants)}곳을 찾았어요!")

    # JSON 저장
    filename = save_report(args.date, city_info, restaurants)
    print(f"\n🎉 리포트 저장 완료: {filename}")

    # ⭐ Markdown 저장
    md_file = save_markdown(args.date, city_info, restaurants)
    print(f"📄 Markdown 리포트 저장: {md_file}")


if __name__ == "__main__":
    main()