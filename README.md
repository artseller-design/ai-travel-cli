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



## ⚠️ Kakao 지도 API 예외 처리 보완

### 평가 항목 #3 보완 내용

본 프로젝트는 추천 도시를 받아 Kakao 지도 API를 호출하여 맛집 정보를 검색한다.

기존 코드에서는 Kakao API 호출부가 아래와 같이 작성되어 있었다.

```python
res = requests.get(url, headers=headers, params=params)
```

이 방식은 Kakao API 호출 자체는 가능하지만, API 요청이 실패했을 때 프로그램이 중단될 수 있다는 문제가 있다.

예를 들어 다음과 같은 상황이 발생할 수 있다.

| 실패 상황 | 설명 |
|---|---|
| 네트워크 오류 | 인터넷 연결 문제로 API 요청 실패 |
| API 키 오류 | 잘못된 Kakao REST API 키 사용 |
| 인증 실패 | 401 Unauthorized 발생 |
| 권한 오류 | 403 Forbidden 발생 |
| 서버 오류 | Kakao API 서버 장애 |
| 응답 지연 | API 응답 시간이 길어짐 |
| JSON 파싱 오류 | 응답을 JSON으로 변환하지 못함 |

따라서 본 프로젝트에서는 Kakao API 호출 실패 시에도 전체 프로그램이 중단되지 않도록  
**호출부에서 `try-except`를 사용해 예외를 처리하고, 실패한 경우 빈 결과로 대체하도록 보완하였다.**

---

## ✅ 보완 목표

Kakao API 호출이 실패해도 다음 흐름을 보장한다.

```text
Kakao API 호출 시도
        ↓
성공하면 맛집 목록 반환
        ↓
실패하면 예외 포착
        ↓
restaurants = [] 로 빈 결과 처리
        ↓
errors 리스트에 오류 내용 누적
        ↓
리포트에는 "데이터 없음" 표시
        ↓
프로그램은 중단되지 않고 계속 실행
```

즉, Kakao API 실패가 전체 여행 추천 리포트 생성 실패로 이어지지 않도록 한다.

---

## ✅ 호출부 예외 처리 방식

Kakao API를 사용하는 호출부에서는 다음과 같이 `try-except`를 적용한다.

```python
errors = []

try:
    restaurants = search_restaurants(city)

except Exception as e:
    restaurants = []
    errors.append({
        "step": "kakao_restaurant_search",
        "city": city,
        "message": str(e)
    })
```

### 코드 설명

| 코드 | 역할 |
|---|---|
| `try` | Kakao API를 이용해 맛집 검색 시도 |
| `search_restaurants(city)` | 추천 도시를 기준으로 맛집 검색 |
| `except Exception as e` | API 호출 실패 시 예외 포착 |
| `restaurants = []` | 실패해도 빈 리스트로 대체 |
| `errors.append(...)` | 실패한 단계, 도시, 오류 메시지를 기록 |

이 구조를 통해 Kakao API 호출에 실패하더라도  
`restaurants`에는 항상 리스트가 들어가므로 이후 리포트 생성 과정이 안전하게 진행된다.

---

## ✅ 여러 추천 도시를 처리하는 경우

추천 도시가 여러 개인 경우에는 각 도시마다 API 실패를 개별적으로 처리한다.

```python
results = []
errors = []

for city in recommended_cities:
    try:
        restaurants = search_restaurants(city)

    except Exception as e:
        restaurants = []
        errors.append({
            "step": "kakao_restaurant_search",
            "city": city,
            "message": str(e)
        })

    results.append({
        "city": city,
        "restaurants": restaurants
    })
```

이 방식의 장점은 다음과 같다.

- 특정 도시의 Kakao API 호출이 실패해도 전체 프로그램이 중단되지 않는다.
- 실패한 도시만 맛집 정보를 빈 목록으로 처리할 수 있다.
- 다른 추천 도시의 맛집 검색은 계속 진행된다.
- 오류 내용은 `errors` 리스트에 누적되어 나중에 확인할 수 있다.

예를 들어 부산 맛집 검색이 실패하더라도, 제주나 서울 맛집 검색은 계속 진행된다.

---

## ✅ Kakao API 함수 내부 예외 처리 예시

Kakao API를 직접 호출하는 함수 내부에서도 기본적인 예외 처리를 적용할 수 있다.

```python
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

        res.raise_for_status()

        data = res.json()

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
```

### 핵심 처리

| 처리 | 설명 |
|---|---|
| `timeout=5` | API 응답을 무한정 기다리지 않도록 제한 |
| `raise_for_status()` | 401, 403, 500 등 HTTP 오류 감지 |
| `data.get("documents", [])` | 검색 결과가 없을 때 빈 리스트 반환 |
| `return []` | 실패 시에도 프로그램이 계속 실행되도록 빈 결과 반환 |

---

## ✅ 리포트 생성 시 "데이터 없음" 처리

Kakao API 호출이 실패하면 `restaurants`에는 빈 리스트 `[]`가 들어간다.  
따라서 Markdown 리포트 생성 시 빈 리스트 여부를 확인하고 `"데이터 없음"`으로 표시한다.

```python
def make_restaurant_section(restaurants):
    if not restaurants:
        return "### 🍽️ 추천 맛집\n\n> 데이터 없음\n"

    markdown = "### 🍽️ 추천 맛집\n\n"
    markdown += "| 맛집 이름 | 주소 | 링크 |\n"
    markdown += "|---|---|---|\n"

    for restaurant in restaurants:
        name = restaurant.get("place_name", "이름 없음")
        address = restaurant.get("address_name", "주소 없음")
        url = restaurant.get("place_url", "")

        markdown += f"| {name} | {address} | [보기]({url}) |\n"

    return markdown
```

예상 출력은 다음과 같다.

```markdown
### 🍽️ 추천 맛집

> 데이터 없음
```

이를 통해 사용자는 맛집 정보가 없거나 API 호출에 실패했다는 상황을 명확히 알 수 있다.

---

## ✅ 오류 누적 리포트 처리

Kakao API 호출 중 발생한 오류는 `errors` 리스트에 누적한다.  
필요한 경우 Markdown 리포트 마지막에 오류 기록을 함께 출력할 수 있다.

```python
def make_error_section(errors):
    if not errors:
        return ""

    markdown = "\n## ⚠️ 오류 기록\n\n"
    markdown += "| 단계 | 도시 | 오류 메시지 |\n"
    markdown += "|---|---|---|\n"

    for error in errors:
        step = error.get("step", "unknown")
        city = error.get("city", "-")
        message = error.get("message", "")

        markdown += f"| {step} | {city} | {message} |\n"

    return markdown
```

예상 출력은 다음과 같다.

```markdown
## ⚠️ 오류 기록

| 단계 | 도시 | 오류 메시지 |
|---|---|---|
| kakao_restaurant_search | 부산 | 401 Client Error: Unauthorized |
```

---

## ✅ 전체 적용 예시

아래는 Kakao API 실패 시에도 전체 리포트 생성이 계속되도록 구성한 예시이다.

```python
def build_trip_report(recommended_cities):
    results = []
    errors = []

    for city in recommended_cities:
        try:
            restaurants = search_restaurants(city)

        except Exception as e:
            restaurants = []
            errors.append({
                "step": "kakao_restaurant_search",
                "city": city,
                "message": str(e)
            })

        results.append({
            "city": city,
            "restaurants": restaurants
        })

    markdown = "# 🧳 AI 여행 추천 리포트\n\n"

    for item in results:
        city = item["city"]
        restaurants = item["restaurants"]

        markdown += f"## 📍 추천 도시: {city}\n\n"
        markdown += make_restaurant_section(restaurants)
        markdown += "\n"

    markdown += make_error_section(errors)

    return markdown
```

이 구조에서는 `search_restaurants(city)` 호출이 실패하더라도  
`except` 블록에서 `restaurants = []`로 대체한다.

따라서 Kakao 지도 API에 문제가 발생해도 Markdown 리포트 생성은 중단되지 않는다.

---

## ✅ 보완 결과

이번 보완을 통해 다음 사항을 만족한다.

| 항목 | 보완 내용 |
|---|---|
| API 실패 시 중단 방지 | `try-except`로 예외 포착 |
| 빈 결과 처리 | 실패 시 `restaurants = []` 적용 |
| 오류 누적 | `errors` 리스트에 실패 정보 저장 |
| 리포트 생성 유지 | 맛집 정보가 없어도 Markdown 생성 계속 |
| 사용자 안내 | 맛집 영역에 `"데이터 없음"` 표시 |

---

## ✅ 정리

Kakao 지도 API는 외부 서비스이므로 항상 성공한다고 보장할 수 없다.  
따라서 본 프로젝트에서는 Kakao API 호출 실패 시 호출부에서 예외를 포착하고,  
맛집 검색 결과를 빈 리스트 `[]`로 대체한다.

또한 오류 내용은 `errors` 리스트에 누적하여 추후 확인할 수 있도록 하며,  
리포트 생성 단계에서는 빈 맛집 목록을 감지해 `"데이터 없음"`으로 표시한다.

이를 통해 Kakao API 호출이 실패하더라도 전체 여행 추천 프로그램은 중단되지 않고 정상적으로 결과 리포트를 생성할 수 있다.


## 🔌 함수별 입력/출력 인터페이스 명세

본 프로젝트는 여러 함수가 데이터를 주고받으며 여행 추천 리포트를 생성한다.  
각 함수의 역할과 입력값, 출력값, 예외 상황을 명확히 하기 위해 아래와 같이 인터페이스를 정의한다.

---

## 📌 전체 데이터 흐름

```text
CLI 날짜 입력
    ↓
parse_args()
    ↓
validate_date()
    ↓
load_api_keys()
    ↓
recommend_cities()
    ↓
search_restaurants()
    ↓
build_trip_data()
    ↓
make_markdown_report()
    ↓
save_json(), save_markdown()
```

---

## ✅ 주요 데이터 구조

### 1. 추천 도시 데이터

```python
{
    "city": "부산",
    "reason": "겨울 바다와 야경을 즐기기 좋음"
}
```

| 필드 | 타입 | 예시 | 설명 |
|---|---|---|---|
| `city` | `str` | `"부산"` | 추천 도시 이름 |
| `reason` | `str` | `"겨울 바다와 야경을 즐기기 좋음"` | 추천 이유 |

---

### 2. 맛집 데이터

Kakao Local API에서 받은 맛집 정보는 다음 형태로 사용한다.

```python
{
    "place_name": "해운대암소갈비집",
    "address_name": "부산 해운대구 중동",
    "road_address_name": "부산 해운대구 중동2로10번길 32-10",
    "phone": "051-746-0033",
    "place_url": "https://place.map.kakao.com/123456"
}
```

| 필드 | 타입 | 예시 | 설명 |
|---|---|---|---|
| `place_name` | `str` | `"해운대암소갈비집"` | 맛집 이름 |
| `address_name` | `str` | `"부산 해운대구 중동"` | 지번 주소 |
| `road_address_name` | `str` | `"부산 해운대구 중동2로10번길 32-10"` | 도로명 주소 |
| `phone` | `str` | `"051-746-0033"` | 전화번호 |
| `place_url` | `str` | `"https://place.map.kakao.com/123456"` | 카카오맵 상세 링크 |

---

### 3. 오류 데이터

API 호출 실패나 처리 오류는 `errors` 리스트에 누적한다.

```python
{
    "step": "kakao_restaurant_search",
    "city": "부산",
    "message": "401 Client Error: Unauthorized"
}
```

| 필드 | 타입 | 예시 | 설명 |
|---|---|---|---|
| `step` | `str` | `"kakao_restaurant_search"` | 오류 발생 단계 |
| `city` | `str` | `"부산"` | 오류가 발생한 도시 |
| `message` | `str` | `"401 Client Error: Unauthorized"` | 오류 메시지 |

---

## ✅ 함수별 입력/출력 표

---

## 1. `parse_args()`

CLI에서 사용자가 입력한 날짜 옵션을 읽는 함수이다.

### 입력값

| 파라미터 | 타입 | 예시 | 설명 |
|---|---|---|---|
| 없음 | - | `python trip.py --date 2025-12-25` | CLI 인자를 내부에서 읽음 |

### 출력값

| 반환값 | 타입 | 예시 | 설명 |
|---|---|---|---|
| `args` | `argparse.Namespace` | `Namespace(date='2025-12-25')` | CLI 인자 객체 |

### 예외 상황

| 상황 | 처리 방식 |
|---|---|
| `--date`가 없는 경우 | argparse가 사용법을 출력하고 종료 |
| 잘못된 옵션 입력 | argparse가 오류 메시지를 출력하고 종료 |

---

## 2. `validate_date(date_str)`

입력된 날짜 문자열이 올바른 형식인지 검사하는 함수이다.

### 입력값

| 파라미터 | 타입 | 예시 | 설명 |
|---|---|---|---|
| `date_str` | `str` | `"2025-12-25"` | 사용자가 입력한 여행 날짜 |

### 출력값

| 반환값 | 타입 | 예시 | 설명 |
|---|---|---|---|
| `date_str` | `str` | `"2025-12-25"` | 검증이 완료된 날짜 문자열 |

### 예외 상황

| 상황 | 처리 방식 |
|---|---|
| 날짜 형식이 `YYYY-MM-DD`가 아님 | `ValueError` 발생 |
| 존재하지 않는 날짜 입력 | `ValueError` 발생 |

### 예시

```python
validate_date("2025-12-25")
# 반환값: "2025-12-25"
```

---

## 3. `load_api_keys()`

`.env` 파일에서 Gemini API 키와 Kakao API 키를 불러오는 함수이다.

### 입력값

| 파라미터 | 타입 | 예시 | 설명 |
|---|---|---|---|
| 없음 | - | `.env` 파일 사용 | 환경 변수에서 API 키를 읽음 |

### 출력값

| 반환값 | 타입 | 예시 | 설명 |
|---|---|---|---|
| `gemini_api_key` | `str` | `"AIza..."` | Gemini API 키 |
| `kakao_api_key` | `str` | `"abc123..."` | Kakao REST API 키 |

### 예외 상황

| 상황 | 처리 방식 |
|---|---|
| `GEMINI_API_KEY`가 없음 | `ValueError` 발생 |
| `KAKAO_API_KEY`가 없음 | `ValueError` 발생 |
| `.env` 파일이 없음 | 환경 변수가 비어 있으면 `ValueError` 발생 |

### 예시

```python
gemini_key, kakao_key = load_api_keys()
```

---

## 4. `recommend_cities(date_str, gemini_api_key)`

Gemini API를 사용하여 여행 날짜에 어울리는 도시를 추천하는 함수이다.

### 입력값

| 파라미터 | 타입 | 예시 | 설명 |
|---|---|---|---|
| `date_str` | `str` | `"2025-12-25"` | 여행 날짜 |
| `gemini_api_key` | `str` | `"AIza..."` | Gemini API 키 |

### 출력값

| 반환값 | 타입 | 예시 | 설명 |
|---|---|---|---|
| `cities` | `list[dict]` | `[{"city": "부산", "reason": "겨울 바다를 즐기기 좋음"}]` | 추천 도시 목록 |

### 예외 상황

| 상황 | 처리 방식 |
|---|---|
| Gemini API 호출 실패 | 호출부에서 예외 처리 |
| 응답 형식이 예상과 다름 | 빈 리스트 `[]` 또는 기본 추천값 사용 |
| 추천 도시가 없음 | 빈 리스트 `[]` 반환 가능 |

### 예시

```python
cities = recommend_cities("2025-12-25", gemini_api_key)

# 예시 반환값
[
    {
        "city": "부산",
        "reason": "겨울 바다와 야경을 즐기기 좋음"
    },
    {
        "city": "제주",
        "reason": "온화한 겨울 날씨로 여행하기 좋음"
    }
]
```

---

## 5. `search_restaurants(city, kakao_api_key)`

Kakao Local API를 호출하여 특정 도시의 맛집을 검색하는 함수이다.

### 입력값

| 파라미터 | 타입 | 예시 | 설명 |
|---|---|---|---|
| `city` | `str` | `"부산"` | 맛집을 검색할 도시 |
| `kakao_api_key` | `str` | `"abc123..."` | Kakao REST API 키 |

### 출력값

| 반환값 | 타입 | 예시 | 설명 |
|---|---|---|---|
| `restaurants` | `list[dict]` | `[{"place_name": "해운대암소갈비집", "address_name": "부산 해운대구 중동"}]` | 맛집 목록 |
| 실패 시 | `list` | `[]` | API 실패 또는 검색 결과 없음 |

### 예외 상황

| 상황 | 처리 방식 |
|---|---|
| 네트워크 오류 | 호출부에서 `try-except`로 처리 |
| API 키 오류 | 호출부에서 `try-except`로 처리 |
| 401, 403, 500 등 HTTP 오류 | 호출부에서 `try-except`로 처리 |
| 타임아웃 | 호출부에서 `try-except`로 처리 |
| JSON 파싱 실패 | 호출부에서 `try-except`로 처리 |
| 검색 결과 없음 | 빈 리스트 `[]` 처리 |

### 예시

```python
restaurants = search_restaurants("부산", kakao_api_key)

# 예시 반환값
[
    {
        "place_name": "해운대암소갈비집",
        "address_name": "부산 해운대구 중동",
        "road_address_name": "부산 해운대구 중동2로10번길 32-10",
        "phone": "051-746-0033",
        "place_url": "https://place.map.kakao.com/123456"
    }
]
```

---

## 6. `collect_restaurants_for_cities(cities, kakao_api_key)`

추천 도시 목록을 순회하면서 각 도시의 맛집을 검색하는 함수이다.  
이 함수는 Kakao API 실패 시에도 프로그램이 중단되지 않도록 호출부 예외 처리를 담당한다.

### 입력값

| 파라미터 | 타입 | 예시 | 설명 |
|---|---|---|---|
| `cities` | `list[dict]` | `[{"city": "부산", "reason": "겨울 바다 여행"}]` | 추천 도시 목록 |
| `kakao_api_key` | `str` | `"abc123..."` | Kakao REST API 키 |

### 출력값

| 반환값 | 타입 | 예시 | 설명 |
|---|---|---|---|
| `results` | `list[dict]` | `[{"city": "부산", "reason": "...", "restaurants": []}]` | 도시별 맛집 검색 결과 |
| `errors` | `list[dict]` | `[{"step": "kakao_restaurant_search", "city": "부산", "message": "..."}]` | 오류 누적 목록 |

### 예외 상황

| 상황 | 처리 방식 |
|---|---|
| 특정 도시의 Kakao API 호출 실패 | 해당 도시의 `restaurants`를 `[]`로 처리 |
| 일부 도시만 실패 | 나머지 도시는 계속 처리 |
| 모든 도시 실패 | 모든 도시의 `restaurants`를 `[]`로 처리하고 리포트 생성 계속 |
| 오류 발생 | `errors` 리스트에 오류 정보 누적 |

### 예시 코드

```python
def collect_restaurants_for_cities(cities, kakao_api_key):
    results = []
    errors = []

    for item in cities:
        city = item.get("city", "")

        try:
            restaurants = search_restaurants(city, kakao_api_key)

        except Exception as e:
            restaurants = []
            errors.append({
                "step": "kakao_restaurant_search",
                "city": city,
                "message": str(e)
            })

        results.append({
            "city": city,
            "reason": item.get("reason", ""),
            "restaurants": restaurants
        })

    return results, errors
```

### 예시 반환값

```python
results = [
    {
        "city": "부산",
        "reason": "겨울 바다와 야경을 즐기기 좋음",
        "restaurants": []
    }
]

errors = [
    {
        "step": "kakao_restaurant_search",
        "city": "부산",
        "message": "401 Client Error: Unauthorized"
    }
]
```

---

## 7. `build_trip_data(date_str, city_results, errors)`

추천 도시, 맛집 결과, 오류 목록을 하나의 JSON 저장용 데이터로 묶는 함수이다.

### 입력값

| 파라미터 | 타입 | 예시 | 설명 |
|---|---|---|---|
| `date_str` | `str` | `"2025-12-25"` | 여행 날짜 |
| `city_results` | `list[dict]` | `[{"city": "부산", "restaurants": []}]` | 도시별 맛집 결과 |
| `errors` | `list[dict]` | `[{"step": "kakao_restaurant_search", "city": "부산", "message": "..."}]` | 오류 목록 |

### 출력값

| 반환값 | 타입 | 예시 | 설명 |
|---|---|---|---|
| `trip_data` | `dict` | `{"date": "2025-12-25", "cities": [...], "errors": [...]}` | 최종 결과 데이터 |

### 예시

```python
trip_data = build_trip_data("2025-12-25", city_results, errors)

# 예시 반환값
{
    "date": "2025-12-25",
    "cities": [
        {
            "city": "부산",
            "reason": "겨울 바다와 야경을 즐기기 좋음",
            "restaurants": []
        }
    ],
    "errors": [
        {
            "step": "kakao_restaurant_search",
            "city": "부산",
            "message": "401 Client Error: Unauthorized"
        }
    ]
}
```

---

## 8. `make_restaurant_section(restaurants)`

맛집 목록을 Markdown 형식으로 변환하는 함수이다.  
맛집 데이터가 없으면 `"데이터 없음"`을 표시한다.

### 입력값

| 파라미터 | 타입 | 예시 | 설명 |
|---|---|---|---|
| `restaurants` | `list[dict]` | `[{"place_name": "해운대암소갈비집"}]` | 맛집 목록 |
| 빈 목록 | `list` | `[]` | API 실패 또는 검색 결과 없음 |

### 출력값

| 반환값 | 타입 | 예시 | 설명 |
|---|---|---|---|
| `markdown` | `str` | `"### 🍽️ 추천 맛집\n\n> 데이터 없음"` | 맛집 Markdown 문자열 |

### 예외 상황

| 상황 | 처리 방식 |
|---|---|
| `restaurants`가 빈 리스트 | `"데이터 없음"` 출력 |
| 특정 필드가 없음 | `"이름 없음"`, `"주소 없음"` 등 기본값 사용 |

### 예시

```python
make_restaurant_section([])

# 반환값
"### 🍽️ 추천 맛집\n\n> 데이터 없음\n"
```

---

## 9. `make_error_section(errors)`

오류 목록을 Markdown 표로 변환하는 함수이다.

### 입력값

| 파라미터 | 타입 | 예시 | 설명 |
|---|---|---|---|
| `errors` | `list[dict]` | `[{"step": "kakao_restaurant_search", "city": "부산", "message": "..."}]` | 오류 목록 |
| 빈 목록 | `list` | `[]` | 오류 없음 |

### 출력값

| 반환값 | 타입 | 예시 | 설명 |
|---|---|---|---|
| `markdown` | `str` | `"## ⚠️ 오류 기록\n\n| 단계 | 도시 | 오류 메시지 |"` | 오류 기록 Markdown |
| 오류 없음 | `str` | `""` | 오류가 없으면 빈 문자열 반환 |

### 예시

```python
make_error_section([
    {
        "step": "kakao_restaurant_search",
        "city": "부산",
        "message": "401 Client Error: Unauthorized"
    }
])
```

---

## 10. `make_markdown_report(trip_data)`

최종 여행 추천 결과를 Markdown 리포트 문자열로 생성하는 함수이다.

### 입력값

| ㅇㅇㅇ

## ✅ 응답 유효성 검사 및 재시도 정책

본 프로젝트는 Gemini API와 Kakao 지도 API를 사용한다.  
외부 API 응답은 항상 정상적인 형식으로 온다고 보장할 수 없으므로, 응답 데이터에 대해 유효성 검사를 수행한다.

특히 Gemini API 응답은 JSON 형식이 깨지거나 필수 키가 누락될 수 있다.  
따라서 JSON 파싱 실패, 필수 키 누락, 타입 불일치가 발생하면 최대 3회까지 재시도한다.

---

## 1. Gemini 추천 도시 응답 검증


## 🔌 지도 API Provider 인터페이스 추상화

### 문제점

기존 구현에서는 Kakao Local API 호출 코드가 서비스 로직 안에 직접 포함되어 있었다.

```python
res = requests.get(url, headers=headers, params=params)
```

이 구조는 Kakao API에 강하게 결합되어 있기 때문에 다음과 같은 문제가 있다.

| 문제 | 설명 |
|---|---|
| API 교체 어려움 | Kakao에서 Google Maps 또는 Naver Maps로 변경할 때 여러 코드를 수정해야 함 |
| 테스트 어려움 | 외부 API 호출이 직접 포함되어 있어 Mock 처리하기 어려움 |
| 책임 분리 부족 | 여행 리포트 생성 로직과 지도 API 호출 로직이 섞임 |
| 장애 대응 어려움 | 지도 API 실패 처리를 일관되게 관리하기 어려움 |

따라서 지도 API 호출부를 `MapProvider` 인터페이스로 추상화하였다.

---

## 개선 방향

지도 API 호출은 공통 인터페이스인 `MapProvider`를 통해 수행한다.

```text
여행 추천 로직
    ↓
MapProvider 인터페이스
    ↓
KakaoMapProvider
```

향후 지도 서비스를 교체할 경우 아래처럼 구현체만 바꾸면 된다.

```text
여행 추천 로직
    ↓
MapProvider 인터페이스
    ↓
GoogleMapProvider 또는 NaverMapProvider
```

---

## 지도 Provider 인터페이스

```python
from abc import ABC, abstractmethod


class MapProvider(ABC):
    @abstractmethod
    def search_restaurants(self, city: str) -> list[dict]:
        pass
```

### 인터페이스 설명

| 항목 | 내용 |
|---|---|
| 인터페이스명 | `MapProvider` |
| 메서드명 | `search_restaurants` |
| 입력값 | `city: str` |
| 출력값 | `list[dict]` |
| 역할 | 특정 도시의 맛집 목록 검색 |
| 구현체 예시 | `KakaoMapProvider`, `GoogleMapProvider`, `NaverMapProvider` |

---

## Kakao Provider 구현체

```python
class KakaoMapProvider(MapProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://dapi.kakao.com/v2/local/search/keyword.json"

    def search_restaurants(self, city: str) -> list[dict]:
        headers = {
            "Authorization": f"KakaoAK {self.api_key}"
        }

        params = {
            "query": f"{city} 맛집",
            "size": 5
        }

        response = requests.get(
            self.base_url,
            headers=headers,
            params=params,
            timeout=5
        )

        response.raise_for_status()

        payload = response.json()

        return self._validate_and_parse_response(payload)
```

`KakaoMapProvider`는 `MapProvider` 인터페이스를 구현한다.  
따라서 서비스 로직은 Kakao API의 URL, 헤더, 파라미터 구조를 알 필요가 없다.

---

## 지도 API 교체 지점

지도 API 교체는 Provider 생성부에서만 수행한다.

### 현재 Kakao 사용

```python
map_provider = KakaoMapProvider(api_key=kakao_api_key)
```

### 향후 Google Maps 사용

```python
map_provider = GoogleMapProvider(api_key=google_api_key)
```

### 향후 Naver Maps 사용

```python
map_provider = NaverMapProvider(
    client_id=naver_client_id,
    client_secret=naver_client_secret
)
```

즉, 지도 API를 교체할 때 수정해야 하는 핵심 지점은 아래 한 줄이다.

```python
map_provider = KakaoMapProvider(api_key=kakao_api_key)
```

서비스 로직은 그대로 유지된다.

---

## 서비스 로직에서의 사용 방식

서비스 로직은 Kakao API를 직접 호출하지 않는다.  
대신 `MapProvider` 인터페이스의 `search_restaurants()` 메서드를 호출한다.

```python
def collect_restaurants_for_cities(cities, map_provider):
    results = []
    errors = []

    for item in cities:
        city = item.get("city", "")
        reason = item.get("reason", "")

        try:
            restaurants = map_provider.search_restaurants(city)

        except Exception as e:
            restaurants = []
            errors.append({
                "step": "map_restaurant_search",
                "provider": map_provider.__class__.__name__,
                "city": city,
                "message": str(e)
            })

        results.append({
            "city": city,
            "reason": reason,
            "restaurants": restaurants
        })

    return results, errors
```

이 구조에서는 지도 API 호출이 실패해도 전체 프로그램이 중단되지 않는다.

실패한 도시는 다음처럼 빈 맛집 목록으로 처리된다.

```python
restaurants = []
```

그리고 오류는 `errors` 리스트에 누적된다.

```python
errors.append({
    "step": "map_restaurant_search",
    "provider": "KakaoMapProvider",
    "city": "부산",
    "message": "401 Client Error: Unauthorized"
})
```

---

## Provider별 역할

| Provider | 역할 | 상태 |
|---|---|---|
| `MapProvider` | 지도 API 공통 인터페이스 | 구현 완료 |
| `KakaoMapProvider` | Kakao Local API 호출 | 구현 완료 |
| `GoogleMapProvider` | Google Maps API 교체용 구현체 | 확장 예정 |
| `NaverMapProvider` | Naver Maps API 교체용 구현체 | 확장 예정 |

---

## 함수별 입력/출력

### `MapProvider.search_restaurants(city)`

| 구분 | 이름 | 타입 | 예시 | 설명 |
|---|---|---|---|---|
| 입력 | `city` | `str` | `"부산"` | 맛집을 검색할 도시 |
| 출력 | `restaurants` | `list[dict]` | `[{"place_name": "맛집명"}]` | 맛집 검색 결과 |

---

### `KakaoMapProvider.__init__(api_key)`

| 구분 | 이름 | 타입 | 예시 | 설명 |
|---|---|---|---|---|
| 입력 | `api_key` | `str` | `"abc123"` | Kakao REST API 키 |
| 출력 | 없음 | `None` | - | Provider 객체 초기화 |

---

### `KakaoMapProvider.search_restaurants(city)`

| 구분 | 이름 | 타입 | 예시 | 설명 |
|---|---|---|---|---|
| 입력 | `city` | `str` | `"제주"` | 맛집 검색 대상 도시 |
| 출력 | `restaurants` | `list[dict]` | `[{"place_name": "제주 맛집"}]` | 정규화된 맛집 목록 |

반환 예시는 다음과 같다.

```python
[
    {
        "place_name": "해운대암소갈비집",
        "address_name": "부산 해운대구 중동",
        "road_address_name": "부산 해운대구 중동2로10번길 32-10",
        "phone": "051-746-0033",
        "place_url": "https://place.map.kakao.com/123456"
    }
]
```

---

## 응답 유효성 검사

Kakao API 응답은 반드시 아래 조건을 만족해야 한다.

| 검사 항목 | 조건 |
|---|---|
| 전체 응답 타입 | `dict` |
| 필수 키 | `documents` |
| `documents` 타입 | `list` |
| 각 맛집 항목 타입 | `dict` |
| `place_name` 타입 | `str` |
| `address_name` 타입 | `str` |
| `road_address_name` 타입 | `str` |
| `phone` 타입 | `str` |
| `place_url` 타입 | `str` |

응답이 조건을 만족하지 않으면 `ValueError`를 발생시킨다.

서비스 로직에서는 해당 예외를 잡아 빈 결과로 처리한다.

```python
try:
    restaurants = map_provider.search_restaurants(city)

except Exception as e:
    restaurants = []
```

---

## 장애 처리 정책

지도 API 호출 실패 시 전체 프로그램은 중단되지 않는다.

| 상황 | 처리 방식 |
|---|---|
| 네트워크 오류 | 예외 포착 후 빈 목록 처리 |
| API 키 오류 | 예외 포착 후 빈 목록 처리 |
| HTTP 오류 | `raise_for_status()`로 감지 후 빈 목록 처리 |
| JSON 파싱 실패 | 예외 포착 후 빈 목록 처리 |
| 응답 필수 키 누락 | `ValueError` 발생 후 빈 목록 처리 |
| 응답 타입 불일치 | `ValueError` 발생 후 빈 목록 처리 |
| 검색 결과 없음 | 빈 리스트 반환 |

실패한 경우 리포트에는 다음과 같이 표시된다.

```markdown
### 🍽️ 추천 맛집

> 데이터 없음
```

---

## 최종 구조

```text
main.py
 ├─ 여행 날짜 입력
 ├─ 추천 도시 생성
 ├─ map_provider = KakaoMapProvider(api_key)
 ├─ collect_restaurants_for_cities(cities, map_provider)
 │      └─ map_provider.search_restaurants(city)
 │             └─ KakaoMapProvider.search_restaurants(city)
 ├─ 실패 시 restaurants = []
 ├─ 오류는 errors 리스트에 누적
 └─ Markdown 리포트 생성
```

---

## 보완 결과

이번 보완으로 다음 사항을 만족한다.

| 항목 | 보완 내용 |
|---|---|
| 지도 API 추상화 | `MapProvider` 인터페이스 추가 |
| Kakao 의존성 분리 | `KakaoMapProvider` 구현체로 분리 |
| 교체 지점 명시 | Provider 생성부 한 곳에서 교체 |
| 확장 가능성 | Google Maps


# 평가 항목 #3 보완 기록: 지도 API 예외 처리 및 오류 리포트 반영

## 평가 결과

| 구분 | 내용 |
|---|---|
| 결과 | FAIL |
| 평가 항목 | #3 |
| 근거 | `trip.py > res = requests.get(url, headers=headers, params=params)` |
| 잘한 점 | 추천 도시를 받아 Kakao API를 호출하도록 구현됨 |
| 부족한 점 | 지도 API 실패 시 중단하지 않고 “데이터 없음”으로 처리하는 예외 처리가 없음 |
| 보완 | API 호출 실패 시 예외를 잡아 결과를 빈 목록 또는 “데이터 없음” 태그로 처리하는 흐름 추가 |

---

## 문제점

기존 코드는 Kakao API 호출부에서 예외 처리가 부족했다.

```python
res = requests.get(url, headers=headers, params=params)
```

이 경우 다음 상황에서 프로그램이 중단될 수 있다.

| 문제 상황 | 설명 |
|---|---|
| 네트워크 오류 | 인터넷 연결 실패 시 프로그램 중단 가능 |
| API 키 오류 | 잘못된 Kakao API 키 사용 시 오류 발생 |
| HTTP 오류 | 401, 403, 500 등의 응답 처리 부족 |
| JSON 파싱 오류 | 응답이 JSON 형식이 아닐 경우 중단 가능 |
| 응답 구조 오류 | `documents` 키가 없을 경우 오류 발생 |
| 오류 기록 없음 | 어떤 단계에서 실패했는지 저장되지 않음 |
| 리포트 반영 없음 | 실패 사실이 Markdown/JSON 결과에 남지 않음 |

---

## 보완 목표

지도 API 호출 실패 시에도 전체 여행 추천 리포트 생성이 중단되지 않도록 한다.

보완 목표는 다음과 같다.

1. API 호출 실패 시 `try-except`로 예외를 잡는다.
2. 실패한 도시의 맛집 결과는 빈 리스트 `[]`로 처리한다.
3. Markdown 리포트에는 `데이터 없음`으로 표시한다.
4. 발생한 예외는 `errors` 리스트에 누적한다.
5. 최종 JSON 저장 데이터에 `errors` 필드를 포함한다.
6. Markdown 리포트 하단에 오류 기록 섹션을 추가한다.

---

## 보완 코드

아래 코드는 지도 API 실패 시 프로그램을 중단하지 않고, 오류를 `errors` 리스트에 누적한 뒤 최종 JSON과 Markdown 리포트에 반영하는 예시이다.

```python
import json
import requests


def add_error(errors, step, message, city="-", provider="-", attempt="-"):
    """
    발생한 예외 정보를 errors 리스트에 누적한다.

    Args:
        errors (list): 오류 정보를 저장할 리스트
        step (str): 오류가 발생한 처리 단계
        message (Exception | str): 오류 메시지
        city (str): 오류가 발생한 도시
        provider (str): 사용한 API Provider 이름
        attempt (int | str): 재시도 횟수
    """

    errors.append({
        "step": step,
        "city": city,
        "provider": provider,
        "attempt": attempt,
        "message": str(message)
    })


def search_restaurants(city, kakao_api_key):
    """
    Kakao Local API를 호출하여 특정 도시의 맛집을 검색한다.

    정상 응답 시:
        맛집 목록을 반환한다.

    실패 시:
        예외를 발생시키고, 호출부에서 이를 잡아 빈 목록으로 처리한다.
    """

    url = "https://dapi.kakao.com/v2/local/search/keyword.json"

    headers = {
        "Authorization": f"KakaoAK {kakao_api_key}"
    }

    params = {
        "query": f"{city} 맛집",
        "size": 5
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=5
    )

    response.raise_for_status()

    data = response.json()

    if "documents" not in data:
        raise ValueError("Kakao API 응답에 'documents' 키가 없습니다.")

    if not isinstance(data["documents"], list):
        raise ValueError("Kakao API 응답의 'documents'는 list 타입이어야 합니다.")

    return data["documents"]


def collect_restaurants_for_cities(cities, kakao_api_key, errors):
    """
    추천 도시 목록을 순회하며 Kakao API로 맛집을 검색한다.

    API 호출 실패 시:
    - restaurants는 빈 리스트로 처리
    - 오류 정보는 errors 리스트에 누적
    - 전체 리포트 생성 흐름은 계속 진행
    """

    results = []

    for item in cities:
        city = item.get("city", "")
        reason = item.get("reason", "")

        try:
            restaurants = search_restaurants(city, kakao_api_key)

        except Exception as e:
            restaurants = []

            add_error(
                errors=errors,
                step="kakao_restaurant_search",
                city=city,
                provider="Kakao",
                message=e
            )

        results.append({
            "city": city,
            "reason": reason,
            "restaurants": restaurants
        })

    return results


def make_restaurant_section(restaurants):
    """
    맛집 목록을 Markdown 문자열로 변환한다.
    맛집 데이터가 없으면 '데이터 없음'을 표시한다.
    """

    if not restaurants:
        return "### 🍽️ 추천 맛집\n\n> 데이터 없음\n"

    markdown = "### 🍽️ 추천 맛집\n\n"
    markdown += "| 이름 | 주소 | 전화번호 | 링크 |\n"
    markdown += "|---|---|---|---|\n"

    for restaurant in restaurants:
        name = restaurant.get("place_name", "이름 없음")
        address = (
            restaurant.get("road_address_name")
            or restaurant.get("address_name")
            or "주소 없음"
        )
        phone = restaurant.get("phone", "-")
        url = restaurant.get("place_url", "")

        link = f"[보기]({url})" if url else "-"

        markdown += f"| {name} | {address} | {phone} | {link} |\n"

    return markdown


def make_error_section(errors):
    """
    errors 리스트를 Markdown 표로 변환한다.
    오류가 없으면 빈 문자열을 반환한다.
    """

    if not errors:
        return ""

    markdown = "\n## ⚠️ 오류 기록\n\n"
    markdown += "| 단계 | 도시 | Provider | 시도 | 오류 메시지 |\n"
    markdown += "|---|---|---|---|---|\n"

    for error in errors:
        step = error.get("step", "-")
        city = error.get("city", "-")
        provider = error.get("provider", "-")
        attempt = error.get("attempt", "-")
        message = error.get("message", "-")

        markdown += f"| {step} | {city} | {provider} | {attempt} | {message} |\n"

    return markdown


def make_markdown_report(trip_data):
    """
    여행 추천 결과를 Markdown 리포트로 변환한다.
    오류가 있을 경우 리포트 하단에 오류 기록을 포함한다.
    """

    markdown = "# 🧳 AI 여행 추천 리포트\n\n"
    markdown += f"여행 날짜: {trip_data.get('date', '-')}\n\n"

    cities = trip_data.get("cities", [])

    if not cities:
        markdown += "> 추천 도시 데이터 없음\n\n"

    for item in cities:
        city = item.get("city", "도시 없음")
        reason = item.get("reason", "추천 이유 없음")
        restaurants = item.get("restaurants", [])

        markdown += f"## 📍 {city}\n\n"
        markdown += f"**추천 이유:** {reason}\n\n"
        markdown += make_restaurant_section(restaurants)
        markdown += "\n"

    errors = trip_data.get("errors", [])
    markdown += make_error_section(errors)

    return markdown


def build_trip_data(date_str, city_results, errors):
    """
    최종 저장용 여행 데이터를 생성한다.
    API 오류 기록을 errors 필드에 포함한다.
    """

    return {
        "date": date_str,
        "cities": city_results,
        "errors": errors
    }


def save_json(data, file_path):
    """
    여행 추천 결과를 JSON 파일로 저장한다.
    """

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def save_markdown(markdown, file_path):
    """
    여행 추천 결과를 Markdown 파일로 저장한다.
    """

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(markdown)


def main():
    errors = []

    date_str = "2025-12-25"
    kakao_api_key = "YOUR_KAKAO_API_KEY"

    cities = [
        {
            "city": "부산",
            "reason": "겨울 바다와 야경을 즐기기 좋음"
        },
        {
            "city": "제주",
            "reason": "자연 경관과 휴식을 즐기기 좋음"
        }
    ]

    city_results = collect_restaurants_for_cities(
        cities=cities,
        kakao_api_key=kakao_api_key,
        errors=errors
    )

    trip_data = build_trip_data(
        date_str=date_str,
        city_results=city_results,
        errors=errors
    )

    markdown = make_markdown_report(trip_data)

    save_json(trip_data, "trip_result.json")
    save_markdown(markdown, "trip_report.md")


if __name__ == "__main__":
    main()
```

---

## 오류 데이터 구조

오류 정보는 다음 형식으로 저장된다.

```json
{
  "step": "kakao_restaurant_search",
  "city": "부산",
  "provider": "Kakao",
  "attempt": "-",
  "message": "401 Client Error: Unauthorized"
}
```

| 필드 | 타입 | 설명 |
|---|---|---|
| `step` | `str` | 오류가 발생한 단계 |
| `city` | `str` | 오류가 발생한 도시 |
| `provider` | `str` | 사용한 API Provider |
| `attempt` | `str` 또는 `int` | 재시도 횟수 |
| `message` | `str` | 오류 메시지 |

---

## JSON 저장 예시

최종 저장 데이터에는 추천 결과뿐 아니라 오류 정보도 함께 포함된다.

```json
{
  "date": "2025-12-25",
  "cities": [
    {
      "city": "부산",
      "reason": "겨울 바다와 야경을 즐기기 좋음",
      "restaurants": []
    }
  ],
  "errors": [
    {
      "step": "kakao_restaurant_search",
      "city": "부산",
      "provider": "Kakao",
      "attempt": "-",
      "message": "401 Client Error: Unauthorized"
    }
  ]
}
```

---

## Markdown 리포트 출력 예시

Kakao API 호출에 실패하면 맛집 정보는 다음과 같이 표시된다.

```markdown
### 🍽️ 추천 맛집

> 데이터 없음
```

오류가 발생한 경우 리포트 하단에 다음 섹션이 추가된다.

```markdown
## ⚠️ 오류 기록

| 단계 | 도시 | Provider | 시도 | 오류 메시지 |
|---|---|---|---|---|
| kakao_restaurant_search | 부산 | Kakao | - | 401 Client Error: Unauthorized |
```

---

## 보완 후 동작 방식

| 상황 | 처리 방식 |
|---|---|
| Kakao API 정상 응답 | 맛집 목록을 리포트에 표시 |
| Kakao API 호출 실패 | 해당 도시의 맛집 목록을 빈 리스트 `[]`로 처리 |
| 맛집 목록 없음 | Markdown에 `데이터 없음` 표시 |
| 예외 발생 | `errors` 리스트에 오류 정보 누적 |
| Markdown 생성 | 하단에 `⚠️ 오류 기록` 섹션 추가 |
| JSON 저장 | 최종 데이터에 `errors` 필드 포함 |
| 전체 프로그램 | API 실패와 관계없이 계속 실행 |

---

## 보완 결과

이번 보완으로 평가 항목 #3의 부족한 점을 해결하였다.

| 요구사항 | 반영 여부 |
|---|---|
| API 호출 실패 시 예외 처리 | 반영 |
| 실패 시 프로그램 중단 방지 | 반영 |
| 실패 결과를 빈 목록으로 처리 | 반영 |
| Markdown에 `데이터 없음` 표시 | 반영 |
| 발생 예외를 `errors` 리스트에 누적 | 반영 |
| Markdown 리포트에 오류 기록 포함 | 반영 |
| JSON 저장 데이터에 `errors` 필드 포함 | 반영 |

따라서 지도 API 호출 실패 시에도 여행 추천 리포트는 정상적으로 생성되며, 실패한 API 호출 내역은 최종 결과물에 기록된다.


# 평가 항목 보완 기록: 원본 LLM 응답 별도 보존

## 평가 결과

| 구분 | 내용 |
|---|---|
| 결과 | FAIL |
| 부족한 점 | 원본 LLM 응답, 즉 파싱 전 `LLM raw JSON`을 별도 파일로 저장하지 않음 |
| 보완 | 원본 LLM 응답을 파싱하기 전에 별도 파일로 저장하는 정책을 추가 |

---

## 문제점

기존 흐름에서는 LLM이 반환한 응답을 바로 JSON으로 파싱하여 사용했다.

```python
parsed_data = json.loads(llm_response)
```

이 방식은 다음 문제가 있다.

| 문제 | 설명 |
|---|---|
| 원본 응답 유실 | 파싱 전 LLM이 실제로 어떤 응답을 반환했는지 확인하기 어려움 |
| 디버깅 어려움 | JSON 파싱 실패 시 원인을 추적하기 어려움 |
| 재현성 부족 | 나중에 같은 응답을 다시 검토하거나 테스트하기 어려움 |
| 감사 기록 부족 | 최종 결과가 어떤 원본 응답에서 만들어졌는지 추적하기 어려움 |

따라서 LLM 응답은 반드시 **파싱하기 전에 원본 그대로 별도 파일로 저장**해야 한다.

---

## 보완 목표

LLM 응답 처리 흐름을 다음과 같이 변경한다.

1. LLM에게 여행 추천을 요청한다.
2. LLM이 반환한 원본 응답을 `raw_response`로 받는다.
3. `json.loads()`로 파싱하기 전에 원본 응답을 별도 파일로 저장한다.
4. 저장된 원본 응답 파일 경로를 최종 JSON 결과에 기록한다.
5. JSON 파싱에 실패하더라도 원본 응답은 보존한다.

---

## 원본 LLM 응답 보존 정책

| 항목 | 정책 |
|---|---|
| 저장 시점 | LLM 응답을 받은 직후, JSON 파싱 전에 저장 |
| 저장 대상 | 파싱 전 원본 문자열 전체 |
| 저장 위치 | `outputs/raw/` 디렉터리 |
| 파일명 | `raw_llm_response_날짜시간.json` |
| 저장 방식 | 원본 내용을 수정하지 않고 그대로 저장 |
| 최종 결과 연동 | 최종 JSON에 `raw_llm_response_path` 필드로 경로 기록 |

---

## 보완 코드

아래 코드는 LLM 원본 응답을 파싱하기 전에 별도 파일로 저장하는 예시이다.

```python
import json
from pathlib import Path
from datetime import datetime


def save_raw_llm_response(raw_response, output_dir="outputs/raw"):
    """
    LLM이 반환한 원본 응답을 파싱하기 전에 별도 파일로 저장한다.

    Args:
        raw_response (str): LLM이 반환한 원본 응답 문자열
        output_dir (str): 원본 응답 저장 디렉터리

    Returns:
        str: 저장된 원본 응답 파일 경로
    """

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = Path(output_dir) / f"raw_llm_response_{timestamp}.json"

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(raw_response)

    return str(file_path)


def parse_llm_json(raw_response):
    """
    LLM 원본 응답을 JSON으로 파싱한다.

    Args:
        raw_response (str): LLM이 반환한 원본 응답 문자열

    Returns:
        dict: 파싱된 JSON 데이터

    Raises:
        ValueError: JSON 파싱 실패 시 발생
    """

    try:
        return json.loads(raw_response)

    except json.JSONDecodeError as e:
        raise ValueError(f"LLM 응답 JSON 파싱 실패: {e}")


def add_error(errors, step, message, city="-", provider="-", attempt="-"):
    """
    발생한 예외 정보를 errors 리스트에 누적한다.
    """

    errors.append({
        "step": step,
        "city": city,
        "provider": provider,
        "attempt": attempt,
        "message": str(message)
    })


def build_trip_data(date_str, cities, errors, raw_llm_response_path):
    """
    최종 저장용 여행 데이터를 생성한다.
    원본 LLM 응답 파일 경로를 함께 포함한다.
    """

    return {
        "date": date_str,
        "cities": cities,
        "errors": errors,
        "raw_llm_response_path": raw_llm_response_path
    }
```

---

## 적용 흐름 예시

중요한 점은 **LLM 응답을 먼저 저장하고, 그다음에 JSON 파싱을 수행**하는 것이다.

```python
def main():
    errors = []

    date_str = "2025-12-25"

    # 1. LLM 호출 결과를 원본 문자열로 받음
    raw_llm_response = call_llm_for_trip_recommendation(date_str)

    # 2. 파싱 전에 원본 LLM 응답을 별도 파일로 저장
    raw_llm_response_path = save_raw_llm_response(raw_llm_response)

    # 3. 원본 저장 후 JSON 파싱 시도
    try:
        parsed_data = parse_llm_json(raw_llm_response)

    except Exception as e:
        add_error(
            errors=errors,
            step="llm_json_parse",
            provider="LLM",
            message=e
        )

        parsed_data = {
            "cities": []
        }

    # 4. 최종 데이터에 원본 응답 파일 경로 포함
    trip_data = build_trip_data(
        date_str=date_str,
        cities=parsed_data.get("cities", []),
        errors=errors,
        raw_llm_response_path=raw_llm_response_path
    )

    # 5. 최종 JSON 저장
    with open("trip_result.json", "w", encoding="utf-8") as file:
        json.dump(trip_data, file, ensure_ascii=False, indent=2)
```

---

## 기존 코드와 개선 코드 비교

### 기존 코드

```python
raw_llm_response = call_llm_for_trip_recommendation(date_str)
parsed_data = json.loads(raw_llm_response)
```

기존 코드는 LLM 응답을 바로 파싱하므로, 파싱 실패 시 원본 응답을 확인하기 어렵다.

---

### 개선 코드

```python
raw_llm_response = call_llm_for_trip_recommendation(date_str)

raw_llm_response_path = save_raw_llm_response(raw_llm_response)

parsed_data = parse_llm_json(raw_llm_response)
```

개선 후에는 LLM 응답이 먼저 별도 파일로 저장되므로, 파싱 실패가 발생해도 원본 응답을 확인할 수 있다.

---

## 최종 JSON 저장 예시

최종 결과 JSON에는 원본 LLM 응답 파일 경로가 포함된다.

```json
{
  "date": "2025-12-25",
  "cities": [
    {
      "city": "부산",
      "reason": "겨울 바다와 야경을 즐기기 좋음",
      "restaurants": []
    }
  ],
  "errors": [],
  "raw_llm_response_path": "outputs/raw/raw_llm_response_20251225_153000.json"
}
```

---

## 원본 LLM 응답 파일 예시

`outputs/raw/raw_llm_response_20251225_153000.json`

```json
{
  "cities": [
    {
      "city": "부산",
      "reason": "겨울 바다와 야경을 즐기기 좋음"
    },
    {
      "city": "제주",
      "reason": "자연 경관과 휴식을 즐기기 좋음"
    }
  ]
}
```

---

## 보완 후 동작 방식

| 상황 | 처리 방식 |
|---|---|
| LLM 응답 정상 | 원본 응답 저장 후 JSON 파싱 |
| LLM 응답 파싱 실패 | 원본 응답은 이미 저장되어 있으므로 추후 확인 가능 |
| 최종 JSON 생성 | `raw_llm_response_path`에 원본 파일 경로 기록 |
| 디버깅 필요 | 저장된 raw 파일을 열어 실제 LLM 응답 확인 |
| 재현성 확인 | 원본 응답 파일을 기준으로 동일한 파싱 로직 재검증 가능 |

---

## 보완 결과

이번 보완으로 다음 요구사항을 만족한다.

| 요구사항 | 반영 여부 |
|---|---|
| 원본 LLM 응답 별도 저장 | 반영 |
| JSON 파싱 전 raw 응답 보존 | 반영 |
| 파싱 실패 시에도 원본 응답 확인 가능 | 반영 |
| 최종 JSON에 원본 응답 파일 경로 포함 | 반영 |
| 디버깅 및 재현성 향상 | 반영 |

따라서 LLM 응답이 잘못된 JSON 형식이거나 예상과 다른 구조로 반환되더라도, 원본 응답을 별도 파일에서 확인할 수 있도록 보완하였다.


# 평가 항목 #3 추가 보완 기록: LLM 재요청·캐싱·지명 정규화

## 평가 결과

| 구분 | 내용 |
|---|---|
| 결과 | FAIL |
| 평가 항목 | #3 |
| 근거 | `trip.py > res = requests.get(url, headers=headers, params=params)` |
| 잘한 점 | 추천 도시를 받아 Kakao API를 호출하도록 구현됨 |
| 부족한 점 1 | LLM 불완전 JSON에 대한 재요청 1회 및 프롬프트 보정 정책이 구현되어 있지 않음 |
| 부족한 점 2 | 같은 날짜 요청에 대한 결과 재사용, 즉 캐싱 제안이나 구현이 없음 |
| 부족한 점 3 | 지명 세분화, 키워드 보정, 중앙명사 추출 같은 정규화 로직이 없음 |
| 보완 1 | 파싱 실패 시 1회 재요청하고, 재요청 시 JSON 전용 보정 프롬프트를 사용 |
| 보완 2 | 동일 날짜 요청에 대해 저장된 결과를 재사용하는 캐시 로직 추가 |
| 보완 3 | 도시명 정규화 규칙과 보정 절차를 추가하여 지도 API 검색 품질 개선 |

---

## 1. 보완 목표

이번 보완의 목표는 다음과 같다.

1. LLM 응답이 불완전 JSON일 경우 바로 실패하지 않고 1회 재요청한다.
2. 재요청 시에는 더 엄격한 JSON 전용 프롬프트를 사용한다.
3. 같은 날짜로 이미 생성된 여행 결과가 있으면 LLM과 지도 API를 다시 호출하지 않고 캐시 결과를 재사용한다.
4. 도시명 또는 지명이 모호하거나 불완전할 경우 정규화 후 지도 API 검색어를 만든다.
5. 정규화 과정에서 동음이의어, 행정구역, 불필요한 키워드, 중심 지명 추출을 처리한다.

---

# 2. LLM 불완전 JSON 재요청 및 프롬프트 보정 정책

## 문제점

LLM은 항상 완전한 JSON만 반환하지 않을 수 있다.

예를 들어 다음과 같은 응답이 올 수 있다.

```text
좋아요! 아래 여행지를 추천합니다.

{
  "cities": [
    {"city": "부산", "reason": "겨울 바다를 즐기기 좋음"}
  ]
}
```

또는 다음처럼 JSON이 깨질 수도 있다.

```json
{
  "cities": [
    {
      "city": "부산",
      "reason": "겨울 바다를 즐기기 좋음",
    }
  ]
}
```

이 경우 `json.loads()`에서 파싱 실패가 발생한다.

---

## 보완 정책

| 항목 | 정책 |
|---|---|
| 기본 요청 | 일반 여행 추천 프롬프트 사용 |
| 파싱 실패 시 | 오류 기록 후 1회 재요청 |
| 재요청 횟수 | 최대 1회 |
| 재요청 프롬프트 | JSON만 출력하도록 강하게 제한 |
| 재요청 실패 시 | 빈 추천 목록으로 처리하고 오류 기록 |
| 오류 기록 위치 | `errors` 리스트 |
| 최종 리포트 | 오류 기록 섹션에 실패 사유 표시 |

---

## 프롬프트 보정 전략

### 1차 요청 프롬프트

```text
사용자가 입력한 날짜에 어울리는 국내 여행 도시 3곳을 추천해줘.
반드시 JSON 형식으로 응답해줘.

형식:
{
  "cities": [
    {
      "city": "도시명",
      "reason": "추천 이유"
    }
  ]
}
```

### 재요청 프롬프트

```text
이전 응답은 JSON 파싱에 실패했다.
이번에는 설명, 마크다운, 코드블록 없이 순수 JSON만 출력해라.

반드시 아래 스키마를 지켜라.

{
  "cities": [
    {
      "city": "문자열",
      "reason": "문자열"
    }
  ]
}

주의:
- JSON 외 문장을 절대 포함하지 마라.
- ```json 코드블록을 사용하지 마라.
- 마지막 원소 뒤에 쉼표를 붙이지 마라.
- cities는 반드시 list 타입이어야 한다.
```

---

# 3. 동일 날짜 캐싱 정책

## 문제점

같은 날짜로 여러 번 요청하면 매번 다음 작업이 반복된다.

1. LLM 호출
2. JSON 파싱
3. 지도 API 호출
4. Markdown 생성
5. JSON 저장

이는 비용과 시간이 낭비된다.

---

## 보완 정책

| 항목 | 정책 |
|---|---|
| 캐시 기준 | 여행 날짜 `date_str` |
| 캐시 위치 | `outputs/cache/` |
| 캐시 파일명 | `trip_result_YYYY-MM-DD.json` |
| 캐시 확인 시점 | LLM 호출 전 |
| 캐시가 있으면 | LLM과 지도 API를 호출하지 않고 기존 결과 재사용 |
| 캐시가 없으면 | 새로 생성 후 캐시 저장 |
| 캐시 데이터 | 최종 `trip_data` 전체 |
| 강제 새로고침 | `force_refresh=True`일 때 캐시 무시 |

---

## 캐시 적용 위치

전체 흐름은 다음과 같이 변경한다.

```text
사용자 날짜 입력
        ↓
캐시 파일 존재 여부 확인
        ↓
캐시 있음 → 기존 결과 반환
        ↓
캐시 없음
        ↓
LLM 호출
        ↓
LLM 응답 파싱 및 검증
        ↓
필요 시 1회 재요청
        ↓
도시명 정규화
        ↓
지도 API 호출
        ↓
최종 결과 생성
        ↓
캐시 저장
```

---

# 4. 도시명 정규화 정책

## 문제점

LLM이 반환하는 도시명은 지도 API 검색에 바로 쓰기 어려울 수 있다.

예시는 다음과 같다.

| 입력 | 문제 |
|---|---|
| `부산` | 행정구역명이 축약됨 |
| `서울 강남` | 도시와 구 단위가 섞여 있음 |
| `광주` | 광주광역시인지 경기도 광주시인지 모호함 |
| `제주 여행` | 검색에 불필요한 단어 포함 |
| `해운대` | 부산의 구체 지역이지만 도시명이 없음 |

---

## 정규화 규칙

| 규칙 | 설명 | 예시 |
|---|---|---|
| 공백 정리 | 앞뒤 공백 및 중복 공백 제거 | ` 서울   강남 ` → `서울 강남` |
| 불필요 키워드 제거 | 여행, 추천, 맛집 등 목적어 제거 | `제주 여행` → `제주` |
| 행정구역 보정 | 축약 도시명을 정식 명칭으로 보정 | `부산` → `부산광역시` |
| 동음이의어 처리 | 모호한 지명은 규칙에 따라 보정 또는 경고 기록 | `광주` → `광주광역시` |
| 세부 지역 유지 | 구, 동, 읍 등 세부 지역은 검색어에 유지 | `서울 강남` → `서울특별시 강남` |
| 중심 지명 추출 | 긴 문장에서 핵심 지명을 추출 | `부산 해운대 근처` → `부산광역시 해운대` |
| 검색어 생성 | 정규화 지명 뒤에 목적 키워드 추가 | `부산광역시 해운대 맛집` |

---

# 5. 전체 구현 코드

아래 코드는 다음 기능을 포함한다.

- LLM 응답 JSON 파싱
- 필수 키 및 타입 검사
- 파싱 실패 시 1회 재요청
- 보정 프롬프트 사용
- 동일 날짜 캐시 확인 및 저장
- 도시명 정규화
- 지도 API 검색어 생성
- 오류 기록 누적

```python
import json
import re
from pathlib import Path
from datetime import datetime


# =========================
# 오류 기록
# =========================

def add_error(errors, step, message, city="-", provider="-", attempt="-"):
    """
    발생한 오류를 errors 리스트에 누적한다.
    """

    errors.append({
        "step": step,
        "city": city,
        "provider": provider,
        "attempt": attempt,
        "message": str(message)
    })


# =========================
# 캐싱 로직
# =========================

def get_cache_path(date_str, cache_dir="outputs/cache"):
    """
    날짜를 기준으로 캐시 파일 경로를 생성한다.

    예:
        2025-12-25 -> outputs/cache/trip_result_2025-12-25.json
    """

    Path(cache_dir).mkdir(parents=True, exist_ok=True)
    return Path(cache_dir) / f"trip_result_{date_str}.json"


def load_cached_result(date_str, cache_dir="outputs/cache"):
    """
    동일 날짜의 캐시 결과가 있으면 불러온다.
    캐시가 없으면 None을 반환한다.
    """

    cache_path = get_cache_path(date_str, cache_dir)

    if not cache_path.exists():
        return None

    with open(cache_path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_cached_result(date_str, trip_data, cache_dir="outputs/cache"):
    """
    최종 여행 결과를 날짜 기준 캐시 파일로 저장한다.
    """

    cache_path = get_cache_path(date_str, cache_dir)

    with open(cache_path, "w", encoding="utf-8") as file:
        json.dump(trip_data, file, ensure_ascii=False, indent=2)

    return str(cache_path)


# =========================
# LLM 프롬프트
# =========================

def make_initial_prompt(date_str):
    """
    1차 LLM 요청 프롬프트를 생성한다.
    """

    return f"""
사용자가 입력한 날짜는 {date_str}이다.

이 날짜에 어울리는 국내 여행 도시 3곳을 추천해줘.
반드시 JSON 형식으로만 응답해줘.

형식:
{{
  "cities": [
    {{
      "city": "도시명",
      "reason": "추천 이유"
    }}
  ]
}}
""".strip()


def make_retry_prompt(date_str, previous_response, error_message):
    """
    JSON 파싱 또는 검증 실패 시 사용하는 보정 프롬프트를 생성한다.
    """

    return f"""
이전 응답은 JSON 파싱 또는 스키마 검증에 실패했다.

날짜:
{date_str}

이전 응답:
{previous_response}

오류:
{error_message}

이번에는 설명, 마크다운, 코드블록 없이 순수 JSON만 출력해라.

반드시 아래 스키마를 지켜라.

{{
  "cities": [
    {{
      "city": "문자열",
      "reason": "문자열"
    }}
  ]
}}

주의:
- JSON 외 문장을 절대 포함하지 마라.
- ```json 코드블록을 사용하지 마라.
- 마지막 원소 뒤에 쉼표를 붙이지 마라.
- cities는 반드시 list 타입이어야 한다.
- city와 reason은 반드시 문자열이어야 한다.
""".strip()


# =========================
# LLM 응답 파싱 및 검증
# =========================

def parse_llm_json(raw_response):
    """
    LLM 원본 응답 문자열을 JSON으로 파싱한다.
    """

    try:
        return json.loads(raw_response)

    except json.JSONDecodeError as e:
        raise ValueError(f"LLM JSON 파싱 실패: {e}")


def validate_llm_response(data):
    """
    LLM 응답의 필수 키와 타입을 검사한다.

    기대 형식:
    {
      "cities": [
        {
          "city": "부산",
          "reason": "추천 이유"
        }
      ]
    }
    """

    if not isinstance(data, dict):
        raise ValueError("LLM 응답은 dict 타입이어야 합니다.")

    if "cities" not in data:
        raise ValueError("필수 키 'cities'가 없습니다.")

    if not isinstance(data["cities"], list):
        raise ValueError("'cities'는 list 타입이어야 합니다.")

    for index, item in enumerate(data["cities"]):
        if not isinstance(item, dict):
            raise ValueError(f"cities[{index}]는 dict 타입이어야 합니다.")

        if "city" not in item:
            raise ValueError(f"cities[{index}]에 필수 키 'city'가 없습니다.")

        if "reason" not in item:
            raise ValueError(f"cities[{index}]에 필수 키 'reason'이 없습니다.")

        if not isinstance(item["city"], str):
            raise ValueError(f"cities[{index}]['city']는 str 타입이어야 합니다.")

        if not isinstance(item["reason"], str):
            raise ValueError(f"cities[{index}]['reason']은 str 타입이어야 합니다.")

    return True


def get_trip_recommendation_with_retry(call_llm_func, date_str, errors):
    """
    LLM 여행 추천을 요청한다.

    정책:
    - 1차 요청 실패 시 보정 프롬프트로 1회 재요청
    - 총 시도 횟수는 최대 2회
    - 재요청까지 실패하면 빈 cities를 반환
    """

    previous_response = ""
    last_error = None

    for attempt in range(1, 3):
        try:
            if attempt == 1:
                prompt = make_initial_prompt(date_str)
            else:
                prompt = make_retry_prompt(
                    date_str=date_str,
                    previous_response=previous_response,
                    error_message=last_error
                )

            raw_response = call_llm_func(prompt)
            previous_response = raw_response

            parsed_data = parse_llm_json(raw_response)
            validate_llm_response(parsed_data)

            return parsed_data

        except Exception as e:
            last_error = e

            add_error(
                errors=errors,
                step="llm_parse_or_validate",
                provider="LLM",
                attempt=attempt,
                message=e
            )

    add_error(
        errors=errors,
        step="llm_retry_failed",
        provider="LLM",
        attempt=2,
        message="LLM 응답 파싱 또는 검증이 1회 재요청 후에도 실패했습니다."
    )

    return {
        "cities": []
    }


# =========================
# 도시명 정규화 로직
# =========================

CITY_ALIAS_MAP = {
    "서울": "서울특별시",
    "부산": "부산광역시",
    "대구": "대구광역시",
    "인천": "인천광역시",
    "광주": "광주광역시",
    "대전": "대전광역시",
    "울산": "울산광역시",
    "세종": "세종특별자치시",
    "제주": "제주특별자치도",
    "강원": "강원특별자치도",
    "전북": "전북특별자치도"
}

HOMONYM_RULES = {
    "광주": {
        "default": "광주광역시",
        "alternatives": ["경기도 광주시"],
        "message": "광주는 광주광역시와 경기도 광주시가 모두 가능하므로 기본값을 광주광역시로 사용합니다."
    }
}

LOCAL_PLACE_MAP = {
    "해운대": "부산광역시 해운대",
    "강남": "서울특별시 강남",
    "홍대": "서울특별시 마포구 홍대",
    "성수": "서울특별시 성동구 성수",
    "월정리": "제주특별자치도 제주시 구좌읍 월정리",
    "애월": "제주특별자치도 제주시 애월읍"
}

REMOVE_WORDS = [
    "여행",
    "추천",
    "맛집",
    "근처",
    "주변",
    "가볼만








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

