# 🧳 AI 여행 추천 CLI 프로그램

Gemini AI와 카카오 지도 API를 활용한 여행지 추천 프로그램입니다.  
날짜를 입력하면 AI가 여행 도시를 추천하고, 실제 맛집 정보까지 찾아줍니다!

---

## ✨ 주요 기능

- 🤖 **AI 여행지 추천**: Gemini가 날짜, 날씨, 행사 등을 고려해 여행 도시를 추천
- 🗺️ **실제 맛집 검색**: 카카오 지도 API를 활용해 추천 도시의 맛집 정보 제공
- 💾 **자동 저장**: 추천 결과를 JSON과 Markdown 파일로 저장
- ⚠️ **API 예외 처리**: 외부 API 호출 실패 시 프로그램이 중단되지 않고 `"데이터 없음"`으로 처리

---

## 🛠️ 사용 기술

- Python 3
- Google Gemini API
- Kakao Local API
- argparse
- requests
- python-dotenv

---

## 📦 설치 방법

### 1. 필요한 패키지 설치

```bash
pip install google-generativeai requests python-dotenv

2. .env 파일 생성 후 API 키 입력
프로젝트 루트 폴더에 .env 파일을 만들고 아래 내용을 입력합니다.

GEMINI_API_KEY=your_gemini_key
KAKAO_API_KEY=your_kakao_key

🚀 실행 방법

python trip.py --date 2025-12-25
실행하면 입력한 날짜를 기준으로 AI가 여행 도시를 추천하고,
카카오 지도 API를 통해 해당 도시의 맛집 정보를 검색합니다.

📁 결과 저장
프로그램 실행 결과는 JSON 파일과 Markdown 파일로 저장됩니다.

예시:

results/
├── trip_2025-12-25.json
└── trip_2025-12-25.md
JSON 파일에는 프로그램이 처리한 원본 데이터가 저장되고,
Markdown 파일에는 사용자가 읽기 쉬운 여행 추천 리포트가 저장됩니다.

🔄 프로그램 동작 흐름

1. 사용자가 여행 날짜 입력
2. Gemini AI가 추천 여행 도시 생성
3. 추천 도시명을 기반으로 Kakao Local API 호출
4. 맛집 검색 결과 수집
5. 결과를 JSON / Markdown 파일로 저장
⚠️ API 예외 처리 및 우아한 실패 처리
본 프로그램은 Gemini API와 Kakao Local API 같은 외부 API를 사용합니다.
외부 API는 네트워크 문제, 인증 오류, 요청 제한 초과, 서버 장애 등으로 인해 실패할 수 있습니다.

따라서 Kakao 지도 API 호출 시 오류가 발생해도 프로그램이 중단되지 않도록
try-except를 사용해 예외 처리를 수행합니다.

처리 방식
Kakao API 호출 시 timeout을 설정하여 응답 지연으로 인한 무한 대기를 방지합니다.
HTTP 오류가 발생하면 raise_for_status()를 통해 오류를 감지합니다.
네트워크 오류, 인증 오류, 서버 오류, JSON 파싱 오류가 발생하면 프로그램을 종료하지 않습니다.
API 호출에 실패하면 빈 리스트 []를 반환합니다.
맛집 검색 결과가 비어 있으면 리포트에는 "데이터 없음"으로 표시합니다.
즉, 지도 API 호출이 실패하더라도 전체 여행 추천 리포트 생성은 계속 진행됩니다.

🗺️ Kakao API 실패 시 처리 흐름

Kakao 지도 API 호출
        ↓
성공하면 맛집 목록 반환
        ↓
실패하면 예외 처리
        ↓
빈 리스트 [] 반환
        ↓
Markdown 리포트에 "데이터 없음" 표시
        ↓
프로그램 정상 종료
✅ Kakao API 예외 처리 예시 코드

import requests

def search_restaurants(city, kakao_api_key):
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"

    headers = {
        "Authorization": f"KakaoAK {kakao_api_key}"
    }

    params = {
        "query": f"{city} 맛집",
        "size": 5
    }

    try:
        res = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=5
        )

        # 401, 403, 500 등 HTTP 오류 발생 시 예외 처리
        res.raise_for_status()

        data = res.json()

        # documents가 없을 경우 빈 리스트 반환
        return data.get("documents", [])

    except requests.exceptions.Timeout:
        print("[ERROR] Kakao API 요청 시간이 초과되었습니다.")
        return []

    except requests.exceptions.HTTPError as e:
        print(f"[ERROR] Kakao API HTTP 오류 발생: {e}")
        return []

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Kakao API 요청 실패: {e}")
        return []

    except ValueError:
        print("[ERROR] Kakao API 응답을 JSON으로 변환할 수 없습니다.")
        return []
위 코드에서는 Kakao API 호출이 실패해도 프로그램을 강제로 종료하지 않고
빈 리스트 []를 반환합니다.

📝 맛집 결과가 없을 때 리포트 처리
API 호출 결과가 없거나 API 호출에 실패한 경우,
Markdown 리포트에는 다음과 같이 "데이터 없음"으로 표시합니다.


def make_restaurant_report(restaurants):
    if not restaurants:
        return "## 🍽️ 추천 맛집\n\n> 데이터 없음\n"

    report = "## 🍽️ 추천 맛집\n\n"
    report += "| 맛집 이름 | 주소 | 링크 |\n"
    report += "|---|---|---|\n"

    for restaurant in restaurants:
        name = restaurant.get("place_name", "이름 없음")
        address = restaurant.get("address_name", "주소 없음")
        url = restaurant.get("place_url", "")

        report += f"| {name} | {address} | [바로가기]({url}) |\n"

    return report
이를 통해 사용자는 API 오류가 발생했는지 모르고 빈 화면을 보는 것이 아니라,
명확하게 맛집 데이터가 없다는 안내를 받을 수 있습니다.

📌 예외 처리 적용 이유
기존 방식처럼 단순히 아래 코드만 사용하는 경우,


res = requests.get(url, headers=headers, params=params)
API 요청이 실패하면 프로그램이 중간에 멈출 수 있습니다.

예를 들어 다음과 같은 상황이 발생할 수 있습니다.

상황	설명
네트워크 오류	인터넷 연결 문제로 API 요청 실패
API 키 오류	잘못된 Kakao API 키 사용
인증 실패	401 Unauthorized 발생
권한 없음	403 Forbidden 발생
서버 오류	Kakao API 서버 장애
응답 지연	API 서버 응답 시간이 너무 오래 걸림
JSON 오류	응답 데이터를 JSON으로 변환할 수 없음
검색 결과 없음	해당 도시의 맛집 검색 결과가 없음
따라서 본 프로젝트에서는 API 실패 상황을 고려하여
예외 발생 시 빈 결과를 반환하고, 리포트에는 "데이터 없음"으로 표시하도록 설계했습니다.

✅ 기대 효과
외부 API 장애가 발생해도 프로그램이 중단되지 않습니다.
사용자는 최소한의 여행 추천 결과를 받을 수 있습니다.
맛집 정보가 없을 경우에도 명확한 안내 문구가 표시됩니다.
전체 시스템의 안정성과 사용자 경험이 향상됩니다.
⚠️ 주의 사항
🔒 .env 파일에는 API 키가 들어있으니 절대 외부에 공유하지 마세요!
🚫 GitHub에 올릴 때는 .gitignore에 .env를 추가하세요.
📝 API 키를 코드에 직접 작성하지 말고, 반드시 .env에서 불러오세요.
🔑 Kakao API 사용 시 REST API 키를 사용해야 합니다.
🌐 Kakao Developers에서 Local API 사용 권한이 활성화되어 있는지 확인하세요.

🔐 .gitignore 예시
API 키 유출을 방지하기 위해 .gitignore 파일에 아래 내용을 추가합니다.

gitignore

.env
__pycache__/
results/
단, 결과 파일을 제출해야 하는 경우에는 results/는 제외하지 않아도 됩니다.

📌 최종 정리
이 프로젝트는 Gemini AI를 이용해 여행지를 추천하고,
Kakao Local API를 이용해 실제 맛집 정보를 검색하는 CLI 기반 여행 추천 프로그램입니다.

특히 외부 API 호출 실패 상황을 고려하여,
Kakao API 호출 중 오류가 발생해도 프로그램이 중단되지 않고
맛집 정보를 "데이터 없음"으로 처리하도록 구현했습니다.

이를 통해 일부 기능에 문제가 발생하더라도 전체 여행 추천 리포트는 정상적으로 생성됩니다.



이 README는 평가 항목 #3에서 지적한 내용을 잘 반영합니다.

핵심 보완 내용은 다음 3가지입니다.

1. `requests.get()` 실패 가능성을 설명함  
2. `try-except`, `timeout`, `raise_for_status()`를 사용한 예외 처리 방식을 명시함  
3. 실패 시 빈 리스트 `[]` 반환 후 `"데이터 없음"`으로 리포트에 표시한다고 설명함  

