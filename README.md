# 🧳 AI 여행 추천 CLI 프로그램

Gemini AI와 Kakao Local API를 활용하여 여행 날짜를 입력하면 대한민국 국내 여행 도시를 추천하고, 추천된 도시의 실제 맛집 정보를 검색하여 JSON 및 Markdown 형식의 여행 리포트를 자동으로 생성하는 Python CLI 프로그램입니다.

> **문서 작성 기준**
>
> 이 README는 단순한 사용 설명서가 아니라 프로젝트의 목적, 데이터 흐름, 함수별 인터페이스, API 연동 방식, 예외 처리, 데이터 구조, 보안, 테스트 방법 및 향후 개선 설계를 한 곳에서 확인할 수 있도록 구성했습니다.
>
> 현재 `trip.py`에 실제 구현된 기능과, 평가 및 확장을 위해 제시하는 개선 설계는 서로 구분하여 설명합니다. 구현되지 않은 기능을 현재 기능인 것처럼 표시하지 않습니다.

---


![image](https://github.com/user-attachments/assets/cd6540df-cac4-408f-8285-f9e842eeb45f)



# 1. 프로젝트 소개

## 1.1 프로젝트 목적

본 프로젝트의 목적은 Python 프로그램에서 생성형 AI와 외부 REST API를 연동하여 실제 활용 가능한 여행 추천 서비스를 구현하는 것입니다.

사용자는 복잡한 입력 없이 여행 날짜 하나만 지정할 수 있습니다.

```bash
python trip.py --date 2026-10-15
```

프로그램은 입력된 날짜를 Gemini AI에 전달하고, AI가 추천한 국내 여행 도시를 얻습니다.

이후 추천 도시를 검색어로 사용하여 Kakao Local API에서 맛집 정보를 검색합니다.

최종적으로 다음 두 가지 형태의 파일을 생성합니다.

```text
JSON
Markdown
```

JSON은 프로그램이 처리한 구조화된 데이터를 보관하기 위한 형식이며, Markdown은 사람이 읽기 쉬운 여행 리포트 형식입니다.

---

## 1.2 핵심 기능

| 기능 | 현재 구현 |
|---|---|
| CLI 날짜 입력 | ✅ |
| 날짜 형식 검증 | ✅ |
| Gemini AI 연동 | ✅ |
| 국내 도시 1곳 추천 | ✅ |
| 예상 날씨 생성 | ✅ |
| 행사 목록 생성 | ✅ |
| 추천 이유 생성 | ✅ |
| Kakao Local API 연동 | ✅ |
| 맛집 최대 5개 검색 | ✅ |
| JSON 저장 | ✅ |
| Markdown 저장 | ✅ |
| `.env` 환경 변수 | ✅ |
| HTTP 상태 오류 감지 | ✅ |
| API timeout | ❌ 현재 코드에서는 미설정 |
| Kakao 예외 `try-except` | ❌ 현재 코드에서는 미구현 |
| LLM 재요청 | ❌ |
| 동일 날짜 캐싱 | ❌ |
| 도시명 정규화 | ❌ |
| MapProvider 추상화 | ❌ |
| 오류 누적 `errors` 구조 | ❌ |
| 원본 LLM 응답 별도 저장 | ❌ |

---

# 2. 사용 기술

## 2.1 기술 스택

| 기술 | 역할 |
|---|---|
| Python 3 | 전체 프로그램 구현 |
| Google Gemini API | 여행 도시 추천 |
| Kakao Local API | 맛집 검색 |
| `argparse` | CLI 인자 처리 |
| `requests` | HTTP API 호출 |
| `python-dotenv` | `.env` 환경 변수 로드 |
| `json` | JSON 파싱 및 저장 |
| `datetime` | 날짜 검증 |
| `pathlib` | 결과 폴더 및 파일 관리 |
| `os` | 환경 변수 접근 |
| `re` | 정규식 처리를 위한 표준 라이브러리 |

---

## 2.2 외부 API

본 프로그램은 두 개의 외부 API를 사용합니다.

### Google Gemini API

사용자가 입력한 여행 날짜를 기반으로 여행 도시를 추천합니다.

### Kakao Local API

Gemini가 추천한 도시를 검색어로 사용하여 실제 장소 정보를 검색합니다.

전체 구조는 다음과 같습니다.

```text
사용자
  ↓
Python CLI
  ↓
Gemini API
  ↓
추천 도시
  ↓
Kakao Local API
  ↓
맛집 정보
  ↓
JSON / Markdown
```

---

# 3. 프로젝트 구조

```text
ai-travel-cli/
│
├── trip.py
├── README.md
├── .env
├── .gitignore
│
└── results/
    ├── report_YYYY-MM-DD.json
    └── report_YYYY-MM-DD.md
```

## 3.1 `trip.py`

여행 추천 프로그램의 전체 실행 코드입니다.

주요 구성 요소는 다음과 같습니다.

```text
환경 변수 로드
↓
Gemini 모델 설정
↓
recommend_city()
↓
search_restaurants()
↓
save_report()
↓
save_markdown()
↓
valid_date()
↓
main()
```

## 3.2 `.env`

API Key를 저장합니다.

```env
GEMINI_API_KEY=your_gemini_api_key
KAKAO_API_KEY=your_kakao_rest_api_key
```

## 3.3 `results/`

프로그램 실행 결과가 저장되는 폴더입니다.

```text
results/
├── report_2026-10-15.json
└── report_2026-10-15.md
```

## 3.4 `.gitignore`

API Key가 들어 있는 `.env` 파일을 GitHub에 올리지 않기 위해 사용합니다.

권장 설정:

```gitignore
.env
__pycache__/
```

필요하다면 결과 파일도 제외할 수 있습니다.

```gitignore
results/
```

---

# 4. 설치 방법

## 4.1 저장소 다운로드

```bash
git clone https://github.com/artseller-design/ai-travel-cli.git
cd ai-travel-cli
```

또는 GitHub에서 ZIP 파일을 다운로드하여 압축을 해제합니다.

---

## 4.2 Python 패키지 설치

```bash
pip install google-generativeai requests python-dotenv
```

설치되는 외부 패키지는 다음과 같습니다.

```text
google-generativeai
requests
python-dotenv
```

다음 모듈은 Python 표준 라이브러리이므로 별도 설치가 필요하지 않습니다.

```text
argparse
json
os
re
datetime
pathlib
```

---

# 5. API Key 설정

프로젝트 루트에 `.env` 파일을 만듭니다.

```env
GEMINI_API_KEY=your_gemini_key
KAKAO_API_KEY=your_kakao_key
```

프로그램에서는 다음과 같이 읽습니다.

```python
from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_KEY = os.getenv("GEMINI_API_KEY")
KAKAO_KEY = os.getenv("KAKAO_API_KEY")
```

API Key를 Python 코드에 직접 작성하지 않는 것이 중요합니다.

---

## 5.1 보안 주의

다음 파일은 공개 저장소에 올리지 않는 것을 권장합니다.

```text
.env
```

`.gitignore`:

```gitignore
.env
__pycache__/
```

이미 API Key가 GitHub에 공개되었다면 해당 키를 폐기하고 새 Key를 발급하는 것이 안전합니다.

---

# 6. 실행 방법

기본 실행:

```bash
python trip.py --date 2026-10-15
```

예:

```bash
python trip.py --date 2026-12-25
```

날짜는 다음 형식을 사용합니다.

```text
YYYY-MM-DD
```

예:

```text
2026-10-15
```

잘못된 예:

```text
2026/10/15
20261015
2026-15-10
```

---

# 7. 전체 프로그램 동작 흐름

현재 코드의 실제 흐름은 다음과 같습니다.

```text
사용자
  │
  │ --date 2026-10-15
  ▼
argparse
  │
  ▼
valid_date()
  │
  ▼
main()
  │
  ▼
recommend_city()
  │
  ▼
Gemini API
  │
  ▼
추천 도시 1곳
  │
  ▼
search_restaurants()
  │
  ▼
Kakao Local API
  │
  ▼
맛집 최대 5곳
  │
  ├───────────────┐
  ▼               ▼
save_report()   save_markdown()
  │               │
  ▼               ▼
JSON 파일        Markdown 파일
```

---

# 8. 데이터 흐름 상세

## 단계 1. CLI 입력

사용자가 여행 날짜를 입력합니다.

```bash
python trip.py --date 2026-10-15
```

`argparse`가 `--date` 값을 읽습니다.

---

## 단계 2. 날짜 검증

```python
valid_date("2026-10-15")
```

`datetime.strptime()`를 이용하여 날짜가 올바른지 확인합니다.

---

## 단계 3. Gemini 호출

```python
city_info = recommend_city(args.date)
```

Gemini API에 날짜를 전달합니다.

---

## 단계 4. 추천 도시 추출

```python
city = city_info["recommended_city"]
```

AI가 반환한 JSON에서 추천 도시를 가져옵니다.

---

## 단계 5. Kakao 검색

```python
restaurants = search_restaurants(city)
```

추천 도시 이름에 `" 맛집"`을 붙여 검색합니다.

예:

```text
부산 맛집
```

---

## 단계 6. JSON 저장

```python
filename = save_report(
    args.date,
    city_info,
    restaurants
)
```

---

## 단계 7. Markdown 저장

```python
md_file = save_markdown(
    args.date,
    city_info,
    restaurants
)
```

---

# 9. Gemini AI 여행지 추천

## 9.1 함수

```python
def recommend_city(date: str) -> dict:
```

입력:

```text
date: str
```

출력:

```text
dict
```

---

## 9.2 프롬프트

현재 코드에서는 다음과 같은 형태의 프롬프트를 사용합니다.

```text
{date}에 여행하기 좋은 대한민국 국내 도시 1곳을 추천해줘.
반드시 아래 JSON 형식으로만 답변해줘.

{
  "recommended_city": "도시 이름",
  "weather": "예상 날씨",
  "events": ["행사1", "행사2"],
  "reason": "추천 이유"
}
```

---

## 9.3 JSON 응답 형식

예상 응답:

```json
{
  "recommended_city": "부산",
  "weather": "맑고 선선함",
  "events": [
    "지역 행사 예시"
  ],
  "reason": "가을 바다와 도시 관광을 즐기기 좋음"
}
```

---

## 9.4 Gemini 응답 처리

현재 코드:

```python
response = model.generate_content(
    prompt,
    generation_config={
        "response_mime_type": "application/json"
    }
)

return json.loads(response.text)
```

`response_mime_type`을 사용하여 JSON 응답을 요청하고, `json.loads()`를 이용해 Python `dict`로 변환합니다.

---

# 10. Gemini 모델 관리

현재 모델명은 한 곳에서 관리합니다.

```python
MODEL_NAME = "gemini-flash-latest"
```

이 구조의 장점은 모델을 변경할 때 여러 함수에 흩어진 문자열을 수정할 필요가 없다는 것입니다.

예를 들어 향후 모델을 변경할 경우:

```python
MODEL_NAME = "새로운-모델명"
```

한 곳만 수정하면 됩니다.

---

# 11. Kakao Local API 맛집 검색

## 11.1 함수

```python
def search_restaurants(city: str) -> list:
```

입력:

```text
city: str
```

출력:

```text
list
```

---

## 11.2 엔드포인트

```text
https://dapi.kakao.com/v2/local/search/keyword.json
```

---

## 11.3 요청 헤더

```python
headers = {
    "Authorization": f"KakaoAK {KAKAO_KEY}"
}
```

---

## 11.4 요청 파라미터

```python
params = {
    "query": f"{city} 맛집",
    "size": 5
}
```

따라서 추천 도시가 부산이면:

```text
query = "부산 맛집"
size = 5
```

입니다.

---

# 12. GET과 POST

HTTP Method는 API가 수행하는 목적에 따라 구분합니다.

| Method | 일반적인 목적 |
|---|---|
| GET | 기존 데이터 조회 |
| POST | 데이터 생성 또는 요청 본문 전달 |

Kakao Local API의 키워드 검색은 장소 데이터를 조회하는 작업이므로 GET 요청을 사용합니다.

현재 코드:

```python
res = requests.get(
    url,
    headers=headers,
    params=params
)
```

---

## 12.1 GET 요청의 특징

```text
GET
 ↓
URL + Query Parameter
 ↓
서버
 ↓
기존 데이터 검색
```

Kakao 검색 예:

```text
query=부산 맛집
size=5
```

---

## 12.2 실제 검색 URL 개념

```text
GET /v2/local/search/keyword.json
    ?query=부산 맛집
    &size=5
```

실제 HTTP 요청에서는 검색어가 URL 인코딩됩니다.

---

# 13. Kakao API 응답 처리

Kakao API 응답에서:

```python
docs = res.json().get("documents", [])
```

를 사용합니다.

즉, `documents`가 없으면 기본값으로 빈 리스트를 사용합니다.

---

## 13.1 맛집 데이터 변환

현재 코드는 각 검색 결과에서 다음 3개 필드를 선택합니다.

```python
{
    "name": d.get("place_name"),
    "address": d.get("road_address_name")
               or d.get("address_name"),
    "url": d.get("place_url"),
}
```

---

## 13.2 필드 설명

| 최종 필드 | Kakao 원본 필드 | 설명 |
|---|---|---|
| `name` | `place_name` | 장소 이름 |
| `address` | `road_address_name` 또는 `address_name` | 주소 |
| `url` | `place_url` | Kakao 장소 링크 |

---

# 14. JSON 리포트 생성

함수:

```python
def save_report(
    date: str,
    city_info: dict,
    restaurants: list
):
```

---

## 14.1 저장 폴더 생성

```python
Path("results").mkdir(exist_ok=True)
```

`results` 폴더가 없으면 생성합니다.

---

## 14.2 저장 데이터

```python
report = {
    "date": date,
    "city_info": city_info,
    "restaurants": restaurants,
}
```

---

## 14.3 파일명

```python
filename = f"results/report_{date}.json"
```

예:

```text
results/report_2026-10-15.json
```

---

# 15. JSON 결과 예시

```json
{
  "date": "2026-10-15",
  "city_info": {
    "recommended_city": "부산",
    "weather": "맑고 선선함",
    "events": [
      "지역 행사 예시"
    ],
    "reason": "가을 바다와 도시 관광을 즐기기 좋음"
  },
  "restaurants": [
    {
      "name": "예시 맛집",
      "address": "부산 해운대구",
      "url": "https://place.map.kakao.com/"
    }
  ]
}
```

JSON은 프로그램에서 재사용하기 쉬운 구조화 데이터입니다.

---

# 16. Markdown 리포트

함수:

```python
def save_markdown(
    date: str,
    city_info: dict,
    restaurants: list
):
```

---

## 16.1 도시 정보 추출

```python
city = city_info["recommended_city"]
weather = city_info["weather"]
events = city_info["events"]
reason = city_info["reason"]
```

---

## 16.2 행사 목록

```python
events_md = "\n".join(
    [f"- {e}" for e in events]
)
```

예:

```markdown
- 지역 행사 1
- 지역 행사 2
```

---

## 16.3 맛집 표

```markdown
| 맛집 이름 | 주소 | 링크 |
|---|---|---|
| 예시 맛집 | 부산 해운대구 | [바로가기](https://place.map.kakao.com/) |
```

---

# 17. Markdown 결과 예시

```markdown
# 🧳 2026-10-15 여행 리포트

## 📍 추천 도시: 부산

- **예상 날씨:** 맑고 선선함
- **추천 이유:** 가을 바다와 도시 관광을 즐기기 좋음

## 🎉 주요 행사

- 지역 행사 예시

## 🍜 추천 맛집

| 맛집 이름 | 주소 | 링크 |
|---|---|---|
| 예시 맛집 | 부산 해운대구 | [바로가기](https://place.map.kakao.com/) |
```

---

# 18. 날짜 검증

함수:

```python
def valid_date(s: str) -> str:
```

구현:

```python
try:
    datetime.strptime(s, "%Y-%m-%d")
    return s
except ValueError:
    raise argparse.ArgumentTypeError(
        f"날짜 형식이 잘못됐어요: {s} (YYYY-MM-DD 형식으로!)"
    )
```

---

## 18.1 정상 입력

```text
2026-10-15
```

---

## 18.2 잘못된 입력

```text
2026/10/15
```

또는:

```text
20261015
```

이 경우 `ArgumentTypeError`가 발생합니다.

---

# 19. argparse

메인 함수에서는 다음과 같이 CLI 인자를 정의합니다.

```python
parser = argparse.ArgumentParser(
    description="여행지 추천 리포트 생성기"
)

parser.add_argument(
    "--date",
    type=valid_date,
    required=True,
    help="여행 날짜 (예: 2025-12-25)"
)
```

따라서 `--date`는 필수 입력입니다.

---

# 20. main 함수

현재 프로그램의 핵심 실행 흐름은 `main()`에 있습니다.

```python
def main():
    parser = argparse.ArgumentParser(
        description="여행지 추천 리포트 생성기"
    )

    parser.add_argument(
        "--date",
        type=valid_date,
        required=True,
        help="여행 날짜 (예: 2025-12-25)"
    )

    args = parser.parse_args()

    print(f"\n🔍 {args.date} 여행지를 추천받는 중...")
    city_info = recommend_city(args.date)

    city = city_info["recommended_city"]

    print(f"✅ 추천 도시: {city}")

    print(f"🍜 {city} 맛집을 검색하는 중...")
    restaurants = search_restaurants(city)

    print(f"✅ 맛집 {len(restaurants)}곳을 찾았어요!")

    filename = save_report(
        args.date,
        city_info,
        restaurants
    )

    print(f"\n🎉 리포트 저장 완료: {filename}")

    md_file = save_markdown(
        args.date,
        city_info,
        restaurants
    )

    print(f"📄 Markdown 리포트 저장: {md_file}")
```

---

# 21. 함수별 입력/출력 인터페이스 명세

현재 실제 코드 기준으로 각 함수의 인터페이스를 정리합니다.

| 함수 | 입력 | 출력 | 역할 |
|---|---|---|---|
| `recommend_city()` | `date: str` | `dict` | Gemini 여행지 추천 |
| `search_restaurants()` | `city: str` | `list` | Kakao 맛집 검색 |
| `save_report()` | 날짜, 도시정보, 맛집 | 파일 경로 | JSON 저장 |
| `save_markdown()` | 날짜, 도시정보, 맛집 | 파일 경로 | Markdown 저장 |
| `valid_date()` | `s: str` | `str` | 날짜 검증 |
| `main()` | CLI 인자 | 없음 | 전체 실행 |

---

# 22. `recommend_city()` 인터페이스

## 입력

```text
date: str
```

예:

```text
"2026-10-15"
```

## 출력

```text
dict
```

예:

```json
{
  "recommended_city": "부산",
  "weather": "맑음",
  "events": [],
  "reason": "추천 이유"
}
```

## 예외 가능성

현재 코드에서는 다음 상황에 대한 별도 `try-except`가 없습니다.

- Gemini API 인증 오류
- 네트워크 오류
- API 사용량 오류
- 응답 파싱 오류
- 예상하지 못한 JSON 구조

따라서 이 부분은 향후 개선 대상입니다.

---

# 23. `search_restaurants()` 인터페이스

## 입력

```text
city: str
```

예:

```text
"부산"
```

## 출력

```text
list
```

예:

```json
[
  {
    "name": "예시 맛집",
    "address": "부산 해운대구",
    "url": "https://place.map.kakao.com/"
  }
]
```

## 현재 구현

```python
res = requests.get(
    url,
    headers=headers,
    params=params
)

res.raise_for_status()
```

HTTP 오류가 발생하면 `raise_for_status()`가 예외를 발생시킵니다.

현재 코드에서는 이 예외를 별도의 `try-except`로 감싸지 않았습니다.

---

# 24. `save_report()` 인터페이스

입력:

```text
date: str
city_info: dict
restaurants: list
```

출력:

```text
results/report_YYYY-MM-DD.json
```

---

# 25. `save_markdown()` 인터페이스

입력:

```text
date: str
city_info: dict
restaurants: list
```

출력:

```text
results/report_YYYY-MM-DD.md
```

---

# 26. 전체 데이터 구조

현재 최종 JSON 구조:

```text
report
├── date
├── city_info
│   ├── recommended_city
│   ├── weather
│   ├── events
│   └── reason
└── restaurants
    ├── name
    ├── address
    └── url
```

---

# 27. 추천 도시 데이터

```json
{
  "recommended_city": "부산",
  "weather": "맑음",
  "events": [
    "행사1",
    "행사2"
  ],
  "reason": "추천 이유"
}
```

| 필드 | 타입 | 설명 |
|---|---|---|
| `recommended_city` | string | 추천 도시 |
| `weather` | string | AI가 생성한 예상 날씨 |
| `events` | list | AI가 제시한 행사 |
| `reason` | string | 추천 이유 |

---

# 28. 맛집 데이터

```json
{
  "name": "예시 맛집",
  "address": "부산 해운대구",
  "url": "https://place.map.kakao.com/"
}
```

| 필드 | 타입 | 설명 |
|---|---|---|
| `name` | string | 장소 이름 |
| `address` | string | 도로명 또는 지번 주소 |
| `url` | string | Kakao 장소 링크 |

---

# 29. API 예외 처리의 현재 상태

현재 코드에는 다음과 같은 처리가 있습니다.

```python
res.raise_for_status()
```

이 코드는 HTTP 상태 코드가 오류인 경우 예외를 발생시키는 역할을 합니다.

그러나 현재 코드에는 다음 구조가 없습니다.

```python
try:
    ...
except requests.exceptions.Timeout:
    ...
except requests.exceptions.HTTPError:
    ...
except requests.exceptions.RequestException:
    ...
```

따라서 이 부분은 **현재 구현 기능이 아니라 향후 보완 항목**으로 분류합니다.

---

# 30. 평가 관점에서 중요한 예외 처리

외부 API는 항상 성공한다고 가정하면 안 됩니다.

가능한 실패 상황:

| 상황 | 설명 |
|---|---|
| 네트워크 오류 | 인터넷 연결 문제 |
| API Key 오류 | 잘못된 API Key |
| 인증 오류 | 401 등 |
| 권한 오류 | 403 등 |
| 서버 오류 | 5xx |
| 응답 지연 | 서버 응답 지연 |
| JSON 오류 | 응답 파싱 실패 |
| 검색 결과 없음 | `documents`가 비어 있음 |

현재 코드에서는 `documents`가 없을 때:

```python
res.json().get("documents", [])
```

를 사용하여 빈 리스트를 반환할 수 있도록 되어 있습니다.

---

# 31. 예외 처리 개선 설계

향후 Kakao API는 다음과 같이 보완할 수 있습니다.

```python
def search_restaurants(city: str) -> list:
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"

    headers = {
        "Authorization": f"KakaoAK {KAKAO_KEY}"
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
        print(f"[ERROR] Kakao API HTTP 오류: {e}")
        return []

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Kakao API 요청 실패: {e}")
        return []

    except ValueError:
        print("[ERROR] Kakao API 응답을 JSON으로 변환할 수 없습니다.")
        return []
```

> 위 코드는 **현재 `trip.py`에 적용된 코드가 아니라 향후 개선 예시**입니다.

---

# 32. timeout의 필요성

현재:

```python
requests.get(
    url,
    headers=headers,
    params=params
)
```

향후:

```python
requests.get(
    url,
    headers=headers,
    params=params,
    timeout=5
)
```

`timeout=5`를 설정하면 API 서버가 계속 응답하지 않는 상황에서 프로그램이 무한정 기다리는 것을 방지할 수 있습니다.

---

# 33. 우아한 실패 처리

이 프로젝트에서 중요한 설계 방향은 외부 API 실패와 전체 프로그램 실패를 분리하는 것입니다.

개선된 구조:

```text
Kakao API 호출
      ↓
성공 ───────→ 맛집 목록
      │
실패
      ↓
예외 처리
      ↓
[]
      ↓
Markdown에 "데이터 없음"
      ↓
전체 리포트 생성 계속
```

현재 코드에서는 이 구조가 완전히 구현되어 있지 않으므로 향후 보완 대상입니다.

---

# 34. "데이터 없음" 처리 설계

맛집 검색 결과가 빈 리스트라면 Markdown에서 다음과 같이 표현할 수 있습니다.

```markdown
## 🍽️ 추천 맛집

> 데이터 없음
```

개선 함수 예:

```python
def make_restaurant_section(restaurants):
    if not restaurants:
        return "## 🍽️ 추천 맛집\n\n> 데이터 없음\n"

    markdown = "## 🍽️ 추천 맛집\n\n"
    markdown += "| 맛집 이름 | 주소 | 링크 |\n"
    markdown += "|---|---|---|\n"

    for restaurant in restaurants:
        name = restaurant.get("name", "이름 없음")
        address = restaurant.get("address", "주소 없음")
        url = restaurant.get("url", "")

        markdown += (
            f"| {name} | {address} | [보기]({url}) |\n"
        )

    return markdown
```

---

# 35. 오류 누적 설계

향후에는 오류를 단순 출력하는 대신 데이터로 기록할 수 있습니다.

예:

```json
{
  "step": "kakao_restaurant_search",
  "city": "부산",
  "message": "401 Client Error: Unauthorized"
}
```

여러 오류를:

```python
errors = []
```

에 누적할 수 있습니다.

---

# 36. 오류 리포트 설계

Markdown 마지막에 다음과 같이 표시할 수 있습니다.

```markdown
## ⚠️ 오류 기록

| 단계 | 도시 | 오류 메시지 |
|---|---|---|
| kakao_restaurant_search | 부산 | 401 Unauthorized |
```

이를 통해 사용자는 프로그램이 어떤 단계에서 문제가 발생했는지 확인할 수 있습니다.

---

# 37. LLM JSON 응답의 문제

LLM은 일반적인 Python 함수와 달리 항상 같은 형태로 응답한다고 보장하기 어렵습니다.

예상:

```json
{
  "recommended_city": "부산",
  "weather": "맑음",
  "events": [],
  "reason": "추천 이유"
}
```

하지만 실제 응답이 다음과 같이 올 수도 있습니다.

```text
여행하기 좋은 도시를 추천해 드리겠습니다.

{
  "recommended_city": "부산"
}
```

또는 JSON 문법이 깨질 수도 있습니다.

따라서 향후에는 JSON 파싱 실패에 대한 별도 처리가 필요합니다.

---

# 38. LLM 응답 검증 개선 설계

향후 다음 단계로 구성할 수 있습니다.

```text
Gemini 응답
   ↓
JSON 파싱
   ↓
성공
   ↓
필수 키 확인
   ↓
타입 확인
   ↓
정상 데이터
```

실패:

```text
JSON 파싱 실패
   ↓
오류 기록
   ↓
1회 재요청
   ↓
재요청 응답 검증
```

---

# 39. 필수 키 검증 예시

```python
def validate_city_info(data):
    if not isinstance(data, dict):
        raise ValueError("응답은 dict여야 합니다.")

    required = [
        "recommended_city",
        "weather",
        "events",
        "reason"
    ]

    for key in required:
        if key not in data:
            raise ValueError(
                f"필수 키가 없습니다: {key}"
            )

    if not isinstance(data["events"], list):
        raise ValueError(
            "events는 list여야 합니다."
        )

    return True
```

> 이 코드는 현재 코드에 추가되어 있지 않은 **개선 예시**입니다.

---

# 40. LLM 1회 재요청 정책

향후 JSON 파싱 실패 시 무한 재요청이 아니라 최대 1회만 재요청하도록 제한할 수 있습니다.

```text
1차 요청
   ↓
파싱 성공 → 종료
   ↓
파싱 실패
   ↓
보정 프롬프트
   ↓
2차 요청
   ↓
성공 → 종료
실패 → 오류 기록 및 빈 결과
```

---

# 41. 보정 프롬프트 예시

```text
이전 응답은 JSON 파싱에 실패했습니다.

이번에는 설명, 마크다운, 코드블록 없이
순수 JSON만 출력하십시오.

반드시 다음 스키마를 지키십시오.

{
  "recommended_city": "문자열",
  "weather": "문자열",
  "events": ["문자열"],
  "reason": "문자열"
}

JSON 외의 문장을 포함하지 마십시오.
```

---

# 42. 동일 날짜 캐싱 설계

현재 코드에는 캐싱이 구현되어 있지 않습니다.

그러나 같은 날짜를 반복해서 요청하면:

```text
Gemini API
↓
Kakao API
↓
파일 생성
```

을 매번 반복하게 됩니다.

향후에는 날짜를 캐시 키로 사용할 수 있습니다.

```text
2026-10-15
        ↓
results/cache/report_2026-10-15.json
```

---

# 43. 캐시 흐름

개선 설계:

```text
사용자 날짜 입력
       ↓
캐시 확인
       │
       ├── 존재 → 기존 결과 사용
       │
       └── 없음
             ↓
          Gemini API
             ↓
          Kakao API
             ↓
          결과 저장
             ↓
          캐시 저장
```

---

# 44. 캐시의 장점

- API 호출 감소
- 실행 시간 단축
- 같은 날짜 결과 재사용
- API 사용량 절감
- 개발 및 테스트 편의성 향상

---

# 45. 도시명 정규화

현재 코드는 Gemini가 반환한 `recommended_city`를 그대로 Kakao 검색에 사용합니다.

예:

```text
부산
```

→

```text
부산 맛집
```

그러나 실제 AI 응답이 다음과 같을 수 있습니다.

```text
부산 여행
서울 강남
광주
해운대 근처
```

이 경우 검색 품질을 높이기 위해 도시명을 정규화할 수 있습니다.

---

# 46. 도시명 정규화 규칙 설계

| 입력 | 정규화 예 |
|---|---|
| `부산` | `부산광역시` |
| `제주 여행` | `제주` |
| `서울 강남` | `서울특별시 강남` |
| `부산 해운대 근처` | `부산광역시 해운대` |

가능한 처리:

1. 앞뒤 공백 제거
2. 중복 공백 제거
3. 불필요한 단어 제거
4. 행정구역명 보정
5. 세부 지역 유지
6. 검색어 생성

---

# 47. 정규화 함수 예시

```python
import re

def normalize_city_name(city: str) -> str:
    city = city.strip()
    city = re.sub(r"\s+", " ", city)

    remove_words = [
        "여행",
        "추천",
        "맛집"
    ]

    for word in remove_words:
        city = city.replace(word, "")

    city = city.strip()

    mapping = {
        "부산": "부산광역시",
        "서울": "서울특별시",
        "대구": "대구광역시",
        "인천": "인천광역시",
        "광주": "광주광역시",
        "대전": "대전광역시",
        "울산": "울산광역시"
    }

    return mapping.get(city, city)
```

> 현재 코드에는 적용되지 않은 향후 개선 예시입니다.

---

# 48. 지도 API 추상화 설계

현재 코드에서는 `search_restaurants()`가 Kakao API를 직접 호출합니다.

향후 다른 지도 API를 추가하려면 서비스 로직과 지도 API를 분리할 수 있습니다.

개념:

```text
여행 추천 로직
       ↓
MapProvider
       ↓
KakaoMapProvider
```

향후:

```text
MapProvider
├── KakaoMapProvider
├── NaverMapProvider
└── GoogleMapProvider
```

---

# 49. MapProvider 인터페이스 예시

```python
from abc import ABC, abstractmethod

class MapProvider(ABC):

    @abstractmethod
    def search_restaurants(
        self,
        city: str
    ) -> list[dict]:
        pass
```

---

# 50. Kakao Provider 예시

```python
class KakaoMapProvider(MapProvider):

    def __init__(self, api_key):
        self.api_key = api_key

    def search_restaurants(self, city):
        ...
```

서비스 로직은:

```python
restaurants = map_provider.search_restaurants(city)
```

만 호출할 수 있습니다.

> 이 구조 역시 현재 `trip.py`에는 구현되어 있지 않은 확장 설계입니다.

---

# 51. 현재 코드와 개선 설계의 구분

| 항목 | 현재 | 개선 설계 |
|---|---:|---:|
| Gemini 추천 | ✅ | 유지 |
| Kakao 검색 | ✅ | 유지 |
| JSON 저장 | ✅ | 유지 |
| Markdown 저장 | ✅ | 유지 |
| 날짜 검증 | ✅ | 유지 |
| API timeout | ❌ | 추가 |
| Kakao try-except | ❌ | 추가 |
| LLM 검증 | 부분 | 강화 |
| LLM 재요청 | ❌ | 추가 |
| 캐싱 | ❌ | 추가 |
| 도시명 정규화 | ❌ | 추가 |
| Provider 추상화 | ❌ | 추가 |
| 오류 누적 | ❌ | 추가 |
| raw LLM 저장 | ❌ | 추가 |

---

# 52. 평가 항목 대응표

프로젝트 평가 시 문서에서 확인할 수 있도록 현재 상태를 정리합니다.

| 평가 관점 | 설명 | 상태 |
|---|---|---|
| CLI 사용 | 날짜를 명령줄 인자로 입력 | 구현 |
| 입력 검증 | 날짜 형식 확인 | 구현 |
| LLM 활용 | Gemini API 사용 | 구현 |
| 구조화 응답 | JSON 응답 요청 | 구현 |
| 외부 API | Kakao Local API | 구현 |
| HTTP 통신 | `requests.get()` | 구현 |
| 결과 저장 | JSON | 구현 |
| 보고서 생성 | Markdown | 구현 |
| 환경 변수 | `.env` | 구현 |
| 함수 분리 | 기능별 함수 | 구현 |
| API 오류 처리 | `raise_for_status()` | 부분 |
| timeout | 요청 시간 제한 | 개선 필요 |
| 상세 예외 처리 | `try-except` | 개선 필요 |
| LLM 재요청 | 실패 시 재시도 | 개선 필요 |
| 캐싱 | 날짜별 재사용 | 개선 필요 |
| 지명 정규화 | 검색어 보정 | 개선 필요 |
| API 추상화 | Provider 패턴 | 개선 필요 |

---

# 53. 평가용 상세 설명: CLI

CLI는 Command Line Interface의 약자입니다.

본 프로젝트에서는 GUI 대신 터미널에서 사용자가 여행 날짜를 직접 입력합니다.

```bash
python trip.py --date 2026-10-15
```

이 방식의 장점:

- 실행 방법이 단순함
- 자동화하기 쉬움
- 스크립트에서 호출 가능
- 서버 환경에서도 실행 가능
- `argparse`를 이용해 입력 형식을 관리할 수 있음

---

# 54. 평가용 상세 설명: 함수 분리

하나의 `main()` 함수 안에 모든 코드를 작성하지 않고 기능별로 함수를 분리했습니다.

```text
recommend_city()
search_restaurants()
save_report()
save_markdown()
valid_date()
```

이렇게 분리하면 각 함수의 역할을 명확하게 확인할 수 있습니다.

예:

```text
recommend_city
→ AI 추천

search_restaurants
→ 지도 API 검색

save_report
→ JSON 저장

save_markdown
→ 문서 저장

valid_date
→ 입력 검증
```

---

# 55. 평가용 상세 설명: 환경 변수

API Key를 소스 코드에 직접 입력하면 GitHub 공개 시 Key가 노출될 수 있습니다.

따라서:

```text
코드
 ↓
os.getenv()
 ↓
.env
 ↓
API Key
```

구조로 관리합니다.

---

# 56. 평가용 상세 설명: 구조화된 출력

AI의 자유로운 텍스트 응답 대신 JSON 형식을 요구합니다.

```json
{
  "recommended_city": "부산",
  "weather": "맑음",
  "events": [],
  "reason": "추천 이유"
}
```

이렇게 하면 프로그램이 AI 응답을 데이터로 처리할 수 있습니다.

---

# 57. 평가용 상세 설명: API 연동

프로젝트는 두 개의 서로 다른 역할을 가진 API를 연결합니다.

```text
Gemini
→ 생성형 AI

Kakao Local
→ 실제 장소 데이터 검색
```

따라서 AI 생성 정보와 외부 데이터 검색을 결합한 구조입니다.

---

# 58. 평가용 상세 설명: 데이터 변환

Kakao API에서 받은 데이터를 그대로 저장하지 않고 프로그램에서 필요한 필드만 추출합니다.

원본:

```json
{
  "place_name": "...",
  "address_name": "...",
  "road_address_name": "...",
  "phone": "...",
  "place_url": "..."
}
```

최종:

```json
{
  "name": "...",
  "address": "...",
  "url": "..."
}
```

필요한 정보만 선택함으로써 최종 데이터 구조를 단순화합니다.

---

# 59. 평가용 상세 설명: 주소 우선순위

현재 코드:

```python
d.get("road_address_name")
or d.get("address_name")
```

즉:

```text
도로명 주소 존재
      ↓
사용

도로명 주소 없음
      ↓
지번 주소 사용
```

이 구조는 주소 데이터가 일부 누락되어도 가능한 범위에서 주소를 제공하기 위한 방식입니다.

---

# 60. 평가용 상세 설명: 파일 저장

결과 파일은 여행 날짜를 파일명에 포함합니다.

```text
report_2026-10-15.json
report_2026-10-15.md
```

이렇게 하면 여러 날짜의 결과를 구분하기 쉽습니다.

---

# 61. 결과 재사용

JSON 파일은 향후 다음 기능에서 재사용할 수 있습니다.

```text
JSON
 ↓
웹 페이지
 ↓
GUI
 ↓
통계
 ↓
추가 여행 일정 생성
```

Markdown은 다음 용도로 활용할 수 있습니다.

```text
Markdown
 ↓
문서
 ↓
GitHub
 ↓
PDF 변환
 ↓
여행 계획 공유
```

---

# 62. 테스트 시나리오

## 정상 날짜

```bash
python trip.py --date 2026-10-15
```

기대 결과:

```text
추천 도시 출력
맛집 검색
JSON 저장
Markdown 저장
```

---

## 잘못된 날짜 형식

```bash
python trip.py --date 2026/10/15
```

기대 결과:

```text
날짜 형식 오류
```

---

## 날짜 누락

```bash
python trip.py
```

`--date`가 required이므로 argparse가 오류를 표시합니다.

---

## 검색 결과 없음

Kakao API가 빈 `documents`를 반환하는 경우:

```python
docs = res.json().get("documents", [])
```

결과는:

```text
[]
```

가 됩니다.

---

# 63. API 오류 테스트

향후 예외 처리 개선 후 다음 상황을 테스트할 수 있습니다.

| 테스트 | 기대 결과 |
|---|---|
| 잘못된 Kakao Key | 오류 메시지 + 빈 결과 |
| 인터넷 연결 해제 | 네트워크 오류 처리 |
| 서버 응답 지연 | timeout 처리 |
| 빈 검색 결과 | `[]` |
| JSON 응답 오류 | JSON 오류 처리 |

---

# 64. LLM 테스트

향후 JSON 검증을 추가하면 다음을 테스트할 수 있습니다.

정상:

```json
{
  "recommended_city": "부산",
  "weather": "맑음",
  "events": [],
  "reason": "추천 이유"
}
```

실패:

```text
부산을 추천합니다.
```

필수 키 누락:

```json
{
  "recommended_city": "부산"
}
```

타입 오류:

```json
{
  "recommended_city": 123
}
```

---

# 65. 캐시 테스트 설계

향후 캐싱을 추가하면:

### 1회차

```text
날짜 입력
↓
Gemini 호출
↓
Kakao 호출
↓
결과 저장
↓
캐시 저장
```

### 2회차

```text
같은 날짜 입력
↓
캐시 확인
↓
캐시 있음
↓
기존 결과 사용
```

---

# 66. 지명 정규화 테스트

입력:

```text
부산
```

예상:

```text
부산광역시
```

입력:

```text
제주 여행
```

예상:

```text
제주
```

입력:

```text
서울 강남
```

예상:

```text
서울특별시 강남
```

---

# 67. 보안 체크리스트

- [ ] `.env`에 API Key 저장
- [ ] `.env`를 GitHub에 올리지 않음
- [ ] API Key를 코드에 직접 작성하지 않음
- [ ] 공개된 Key는 폐기
- [ ] 새 Key 발급
- [ ] API 사용량 확인
- [ ] API 제공자의 이용약관 확인

---

# 68. README 문서화 원칙

이 README는 다음 네 가지를 분리하여 설명합니다.

```text
현재 구현
+
실행 방법
+
평가를 위한 기술 설명
+
향후 개선 설계
```

특히 개선 설계는 현재 코드에 실제로 적용된 기능과 혼동하지 않도록 구분합니다.

---

# 69. 현재 구현의 핵심 코드

## 환경 변수

```python
load_dotenv()

GEMINI_KEY = os.getenv("GEMINI_API_KEY")
KAKAO_KEY = os.getenv("KAKAO_API_KEY")
```

## 모델

```python
MODEL_NAME = "gemini-flash-latest"
genai.configure(api_key=GEMINI_KEY)
```

## Gemini

```python
model = genai.GenerativeModel(MODEL_NAME)

response = model.generate_content(
    prompt,
    generation_config={
        "response_mime_type": "application/json"
    }
)
```

## Kakao

```python
res = requests.get(
    url,
    headers=headers,
    params=params
)

res.raise_for_status()
```

## JSON 저장

```python
json.dump(
    report,
    f,
    ensure_ascii=False,
    indent=2
)
```

## Markdown 저장

```python
f.write(md)
```

---

# 70. 현재 코드의 한계

현재 프로그램은 핵심 기능을 간결하게 구현한 버전입니다.

다음 부분은 추가적인 보완이 필요합니다.

## 70.1 API 오류 처리

현재 `raise_for_status()`에서 발생한 예외를 별도로 처리하지 않습니다.

## 70.2 timeout

현재 Kakao 요청에 `timeout`이 지정되어 있지 않습니다.

## 70.3 Gemini 오류 처리

Gemini 호출 실패 또는 JSON 파싱 실패에 대한 별도 처리 로직이 없습니다.

## 70.4 캐싱

같은 날짜를 다시 실행하면 API를 다시 호출합니다.

## 70.5 지명 정규화

AI가 반환한 도시명을 그대로 Kakao 검색어에 사용합니다.

## 70.6 Provider 추상화

Kakao API 호출이 `search_restaurants()` 함수 안에 직접 구현되어 있습니다.

---

# 71. 향후 개선 로드맵

## 1단계: 안정성

```text
timeout
+
try-except
+
상세 오류 메시지
```

## 2단계: LLM 안정성

```text
JSON 검증
+
필수 키 검증
+
1회 재요청
```

## 3단계: 검색 품질

```text
도시명 정규화
+
검색어 보정
```

## 4단계: 성능

```text
날짜별 캐싱
```

## 5단계: 구조 개선

```text
MapProvider
+
KakaoMapProvider
```

## 6단계: 기능 확장

```text
관광지
+
숙박
+
교통
+
날씨
+
여행 일정
```

---

# 72. 향후 확장 기능

### 사용자 취향

```text
바다
산
문화
맛집
카페
역사
```

### 예산

```text
10만원
20만원
30만원
```

### 여행 기간

```text
당일
1박 2일
2박 3일
```

### 여행 인원

```text
혼자
커플
가족
친구
```

이런 입력을 추가하면 더 개인화된 여행 추천이 가능합니다.

---

# 73. 관광지 API 연동

향후 Kakao Local API를 이용해 맛집뿐 아니라 관광지까지 검색할 수 있습니다.

```text
추천 도시
  ↓
관광지 검색
  ↓
맛집 검색
  ↓
카페 검색
```

최종적으로:

```text
오전 → 관광지
점심 → 맛집
오후 → 관광지
저녁 → 맛집
```

형태의 여행 코스를 만들 수 있습니다.

---

# 74. 숙박 정보 확장

향후 숙박 API를 연동하면:

```text
도시
 ↓
관광지
 ↓
맛집
 ↓
숙박
```

을 하나의 여행 데이터로 묶을 수 있습니다.

---

# 75. 날씨 API 확장

현재 `weather`는 Gemini가 생성한 정보입니다.

향후 실제 날씨 API를 연결하면:

```text
Gemini
→ 여행지 추천

날씨 API
→ 실제 예보

Kakao
→ 장소 정보
```

처럼 역할을 분리할 수 있습니다.

이 경우 AI가 생성한 예상 정보와 외부 데이터 기반 실제 예보를 구분할 수 있습니다.

---

# 76. 데이터 신뢰성 개선

현재:

```text
Gemini
→ 날씨 / 행사 / 추천 이유
```

향후:

```text
공식 날씨 API
→ 날씨

공식 행사 데이터
→ 행사

Gemini
→ 추천 이유
```

와 같이 데이터 출처별 역할을 분리할 수 있습니다.

---

# 77. 웹 서비스 확장

현재:

```text
CLI
```

향후:

```text
웹 브라우저
   ↓
여행 날짜 입력
   ↓
Python Backend
   ↓
Gemini + Kakao
   ↓
여행 리포트
```

로 확장할 수 있습니다.

---

# 78. GUI 확장

Tkinter, PySide 또는 웹 UI 등을 사용하여 날짜 선택 화면을 만들 수 있습니다.

예:

```text
┌────────────────────────────┐
│      AI 여행 추천           │
├────────────────────────────┤
│ 여행 날짜: [2026-10-15]    │
│                            │
│       [ 여행 추천 ]         │
└────────────────────────────┘
```

결과:

```text
추천 도시: 부산

예상 날씨:
맑음

추천 이유:
가을 바다 여행에 적합

추천 맛집:
1. ...
2. ...
3. ...
```

---

# 79. 프로젝트 교육적 의미

본 프로젝트를 통해 다음 내용을 실습할 수 있습니다.

## Python

- 함수
- 자료형
- 예외 처리
- 파일 입출력
- 표준 라이브러리

## API

- API Key
- HTTP
- GET
- Query Parameter
- Header
- JSON Response

## AI

- LLM 호출
- Prompt 작성
- Structured JSON 응답

## 데이터

- JSON
- 리스트
- 딕셔너리
- 데이터 변환

## 문서

- Markdown 자동 생성

---

# 80. 소프트웨어 설계 관점

현재 구조는 작은 CLI 프로그램에 적합한 단순 구조입니다.

```text
main
 ├── recommend_city
 ├── search_restaurants
 ├── save_report
 └── save_markdown
```

기능이 증가하면 다음과 같이 계층화할 수 있습니다.

```text
CLI Layer
    ↓
Service Layer
    ↓
AI Provider / Map Provider
    ↓
External API
```

---

# 81. 오류 처리 설계의 중요성

외부 API는 프로그램 내부 함수와 다릅니다.

프로그램 내부:

```text
함수 호출
↓
정상적인 입력
↓
정상적인 반환
```

외부 API:

```text
네트워크
↓
인증
↓
서버 상태
↓
사용량 제한
↓
응답 형식
```

여러 요소에 의해 실패할 수 있습니다.

따라서 외부 API를 사용하는 프로그램은 오류 처리 설계가 중요합니다.

---

# 82. 실패를 데이터로 처리하는 설계

향후에는 오류를 프로그램 종료 조건으로만 보지 않고 데이터로 저장할 수 있습니다.

```json
{
  "step": "kakao_restaurant_search",
  "city": "부산",
  "message": "Timeout"
}
```

그러면 최종 결과가:

```text
성공 결과
+
실패 정보
```

를 동시에 가지게 됩니다.

---

# 83. LLM 실패를 데이터로 처리하는 설계

예:

```json
{
  "date": "2026-10-15",
  "cities": [],
  "errors": [
    {
      "step": "llm_json_parse",
      "message": "JSONDecodeError"
    }
  ]
}
```

이 구조는 디버깅과 운영에 유리합니다.

---

# 84. 재현성

AI는 같은 질문에도 결과가 달라질 수 있습니다.

따라서 향후에는 다음을 저장할 수 있습니다.

```text
입력 날짜
+
프롬프트
+
LLM 원본 응답
+
파싱 결과
+
최종 결과
```

이렇게 하면 어떤 입력과 응답을 통해 결과가 만들어졌는지 추적할 수 있습니다.

---

# 85. 원본 LLM 응답 저장 설계

향후:

```text
results/
└── raw/
    └── raw_llm_response_20261015.json
```

예:

```json
{
  "raw_response": "{ ... }"
}
```

또는 텍스트 파일로 저장할 수 있습니다.

이 기능은 JSON 파싱 오류가 발생했을 때 원인을 분석하는 데 도움이 됩니다.

---

# 86. LLM 응답 검증 설계

검증 대상:

```text
dict인가?
↓
recommended_city 존재?
↓
weather 존재?
↓
events가 list인가?
↓
reason 존재?
↓
각 필드 타입 정상?
```

이 과정을 거치면 잘못된 응답을 조기에 발견할 수 있습니다.

---

# 87. 캐싱과 API 비용

동일한 날짜를 여러 번 요청하면 API 호출이 반복됩니다.

캐싱:

```text
첫 요청
→ API 사용

두 번째 요청
→ 캐시 사용
```

따라서 개발 및 반복 실행 환경에서 API 호출을 줄일 수 있습니다.

---

# 88. 캐시 무효화

캐싱을 추가할 경우 다음 문제도 고려해야 합니다.

```text
오래된 결과
```

따라서 향후에는:

```text
--force-refresh
```

같은 옵션을 추가하여 캐시를 무시하고 새로 생성할 수 있습니다.

예:

```bash
python trip.py --date 2026-10-15 --force-refresh
```

---

# 89. 검색 품질과 지명 정규화

검색 API는 검색어의 품질에 영향을 받습니다.

```text
부산 맛집
```

보다:

```text
부산광역시 해운대구 맛집
```

처럼 구체적인 검색어가 필요한 경우가 있습니다.

AI 출력이 항상 일정하지 않기 때문에 정규화 계층을 두는 것이 확장에 도움이 됩니다.

---

# 90. API 추상화의 장점

현재:

```text
search_restaurants()
      ↓
Kakao API
```

향후:

```text
search_restaurants()
      ↓
MapProvider
      ↓
Kakao
```

가 되면 지도 서비스 교체가 쉬워집니다.

---

# 91. Provider 패턴 예시

```python
class MapProvider:

    def search_restaurants(self, city):
        raise NotImplementedError
```

구현:

```python
class KakaoMapProvider(MapProvider):
    ...
```

향후:

```python
class NaverMapProvider(MapProvider):
    ...
```

이런 구조로 확장할 수 있습니다.

---

# 92. 현재 코드와 향후 구조 비교

현재:

```text
main()
 ↓
search_restaurants()
 ↓
Kakao
```

향후:

```text
main()
 ↓
travel service
 ↓
map provider
 ↓
Kakao
```

---

# 93. API 응답 필드 최소화

외부 API는 많은 정보를 반환할 수 있습니다.

그러나 프로그램에 필요한 필드만 사용합니다.

```text
place_name
address_name
road_address_name
place_url
```

현재 최종 데이터:

```text
name
address
url
```

이렇게 데이터 모델을 단순화하면 후속 처리도 쉬워집니다.

---

# 94. Markdown 자동 생성의 장점

프로그램 결과를 단순히 터미널에 출력하는 대신 파일로 저장합니다.

```text
CLI 결과
+
JSON
+
Markdown
```

따라서 실행 후에도 결과를 다시 확인할 수 있습니다.

---

# 95. 결과 파일 예시

```text
results/
├── report_2026-10-01.json
├── report_2026-10-02.json
├── report_2026-10-15.json
└── report_2026-12-25.json
```

여러 날짜의 여행 계획을 동시에 관리할 수 있습니다.

---

# 96. Markdown을 선택한 이유

Markdown은:

- 사람이 읽기 쉬움
- 표 작성 가능
- 링크 삽입 가능
- GitHub에서 바로 표시됨
- 다른 문서 형식으로 변환하기 쉬움

이라는 장점이 있습니다.

---

# 97. JSON을 선택한 이유

JSON은:

- 구조화된 데이터
- Python에서 처리하기 쉬움
- 다른 언어에서도 사용 가능
- API와 잘 맞음
- 후속 프로그램에서 재사용 가능

이라는 장점이 있습니다.

---

# 98. 프로젝트 실행 결과의 이중 저장

```text
                 여행 데이터
                    │
            ┌───────┴───────┐
            ▼               ▼
          JSON           Markdown
            │               │
       프로그램용         사용자용
```

이러한 구조를 통해 동일한 데이터를 두 가지 목적으로 사용할 수 있습니다.

---

# 99. 프로젝트 한계

현재 프로그램은 다음 범위에 집중합니다.

```text
여행 날짜
↓
국내 도시 1곳
↓
맛집 최대 5곳
↓
파일 저장
```

아직 다음은 구현되어 있지 않습니다.

```text
숙박
교통
실시간 날씨
여행 일정 자동 최적화
사용자 취향 학습
웹 UI
캐싱
상세 예외 처리
```

---

# 100. 향후 최종 목표

확장된 프로그램은 다음과 같은 흐름을 목표로 할 수 있습니다.

```text
여행 날짜
+
여행 기간
+
예산
+
취향
+
동행자
       ↓
Gemini
       ↓
여행지 추천
       ↓
날씨 API
       ↓
관광지 API
       ↓
Kakao/Naver 지도
       ↓
숙박 정보
       ↓
일정 최적화
       ↓
AI 여행 리포트
```

---

# 101. 실행 체크리스트

실행 전:

- [ ] Python 설치
- [ ] 패키지 설치
- [ ] `.env` 생성
- [ ] Gemini API Key 입력
- [ ] Kakao REST API Key 입력
- [ ] 인터넷 연결 확인

실행:

```bash
python trip.py --date 2026-10-15
```

실행 후:

- [ ] 추천 도시 확인
- [ ] 맛집 개수 확인
- [ ] `results/report_2026-10-15.json` 확인
- [ ] `results/report_2026-10-15.md` 확인

---

# 102. 문제 해결

## `ModuleNotFoundError`

예:

```text
ModuleNotFoundError: No module named 'requests'
```

해결:

```bash
pip install requests
```

또는:

```bash
pip install google-generativeai python-dotenv requests
```

---

## API Key 오류

`.env`를 확인합니다.

```env
GEMINI_API_KEY=...
KAKAO_API_KEY=...
```

공백이나 잘못된 Key가 없는지 확인합니다.

---

## Kakao HTTP 오류

현재 코드의:

```python
res.raise_for_status()
```

에서 오류가 발생할 수 있습니다.

Key와 Kakao Developers 설정을 확인합니다.

---

## JSON 파싱 오류

Gemini 응답이 예상한 JSON 형식인지 확인합니다.

현재 코드에서는:

```python
json.loads(response.text)
```

를 사용합니다.

향후 JSON 검증 및 재요청 기능을 추가할 수 있습니다.

---

# 103. 개발 및 유지보수 원칙

## 원칙 1

API Key는 코드에 작성하지 않습니다.

## 원칙 2

외부 API 호출에는 오류 처리를 추가합니다.

## 원칙 3

LLM 출력은 검증합니다.

## 원칙 4

데이터와 표시 형식을 분리합니다.

## 원칙 5

기능이 커지면 Provider 구조를 고려합니다.

## 원칙 6

반복 API 호출은 캐싱을 고려합니다.

---

# 104. 코드 품질 개선 체크리스트

현재:

- [x] 함수 분리
- [x] 환경 변수 사용
- [x] 날짜 검증
- [x] JSON 저장
- [x] Markdown 저장
- [x] API 응답 필드 선택

향후:

- [ ] timeout
- [ ] 예외 클래스 세분화
- [ ] logging
- [ ] LLM 응답 스키마 검증
- [ ] retry
- [ ] cache
- [ ] provider abstraction
- [ ] unit test

---

# 105. 단위 테스트 확장

향후 다음 함수를 테스트할 수 있습니다.

```text
valid_date()
normalize_city_name()
validate_city_info()
search_restaurants()
save_report()
save_markdown()
```

예:

```python
def test_valid_date():
    assert valid_date("2026-10-15") == "2026-10-15"
```

잘못된 날짜:

```python
def test_invalid_date():
    ...
```

---

# 106. 테스트 가능한 구조

함수별로 역할이 분리되어 있기 때문에 향후 테스트 코드를 추가하기 쉽습니다.

```text
입력
 ↓
함수
 ↓
출력
```

예:

```text
"2026-10-15"
 ↓
valid_date()
 ↓
"2026-10-15"
```

---

# 107. 최종 요약

본 프로젝트는 다음 기술을 하나의 프로그램에 결합했습니다.

```text
Python
+
CLI
+
Gemini
+
Kakao Local API
+
JSON
+
Markdown
+
환경 변수
```

핵심 처리 과정:

```text
날짜 입력
 ↓
날짜 검증
 ↓
Gemini 여행지 추천
 ↓
추천 도시 추출
 ↓
Kakao 맛집 검색
 ↓
JSON 저장
 ↓
Markdown 저장
```

---

# 108. 프로젝트의 핵심 학습 포인트

## Python 함수

기능별 함수를 분리하여 프로그램 구조를 구성했습니다.

## API

외부 API를 호출하고 JSON 응답을 처리했습니다.

## LLM

Gemini에 구조화된 JSON 응답을 요청했습니다.

## 파일 처리

JSON과 Markdown을 자동 생성했습니다.

## 보안

API Key를 `.env`로 분리했습니다.

## CLI

`argparse`를 이용하여 명령줄 입력을 처리했습니다.

---

# 109. 현재 구현과 평가 문서의 관계

이 README는 프로젝트의 현재 코드를 기준으로 사실관계를 구분하면서, 평가에서 요구될 수 있는 설계 요소에 대해서는 개선 방향과 구현 예시까지 함께 설명합니다.

따라서 다음 두 가지를 구분합니다.

```text
[현재 구현]
실제로 trip.py에서 동작하는 기능

[개선 설계]
현재 코드에는 없지만 향후 추가할 수 있는 기능
```

이 구분은 프로젝트 문서의 정확성을 유지하기 위한 것입니다.

---

# 110. 최종 프로젝트 설명

본 프로젝트는 Python 기반 CLI 환경에서 Google Gemini API와 Kakao Local API를 연동하여 여행 추천 과정을 자동화한 프로그램입니다.

사용자가 여행 날짜를 입력하면 Gemini가 해당 날짜에 적합한 국내 도시 1곳을 추천하고, 추천 도시를 검색어로 사용하여 Kakao Local API에서 최대 5개의 맛집 정보를 검색합니다.

수집한 데이터는 JSON으로 구조화하여 저장하고, 동일한 내용을 사람이 읽기 쉬운 Markdown 여행 리포트로도 저장합니다.

또한 날짜 입력 검증, 환경 변수 기반 API Key 관리, API 응답 상태 확인, 함수별 역할 분리 등의 구조를 적용했습니다.

향후에는 외부 API 예외 처리 강화, LLM 응답 검증 및 재요청, 캐싱, 도시명 정규화, 지도 API 추상화 등을 추가하여 안정성과 확장성을 높일 수 있습니다.

---

# 111. 제출 전 최종 확인

```text
[프로젝트]
AI 여행 추천 CLI

[입력]
여행 날짜

[AI]
Google Gemini

[외부 데이터]
Kakao Local API

[출력]
JSON + Markdown

[언어]
Python

[실행]
python trip.py --date YYYY-MM-DD
```

---

# 112. Author

**artseller-design**

GitHub Repository:

https://github.com/artseller-design/ai-travel-cli

---

# 113. 문서 버전

```text
README Version: Evaluation-Oriented Final
Code Basis: Current trip.py
```

이 문서는 현재 코드와 향후 개선 설계를 구분하여 프로젝트의 실행 방법과 기술적 설계 근거를 함께 제공하는 것을 목적으로 합니다.

---

# 부록 1. 평가 및 기술 검토 자료

## 검토 목적

이 부록은 프로젝트를 평가하거나 발표할 때 현재 코드의 동작을 빠르게 확인하기 위한 자료입니다.

## 확인 항목

| 항목 | 현재 코드 기준 |
|---|---|
| 날짜 입력 | `argparse --date` |
| 날짜 검증 | `valid_date()` |
| AI 호출 | `recommend_city()` |
| 지도 검색 | `search_restaurants()` |
| JSON 저장 | `save_report()` |
| Markdown 저장 | `save_markdown()` |
| 환경 변수 | `load_dotenv()` |
| 결과 폴더 | `results/` |

## 데이터 흐름

```text
CLI
 ↓
valid_date
 ↓
recommend_city
 ↓
search_restaurants
 ↓
save_report
 ↓
save_markdown
```

## 평가 시 확인할 코드

```python
def recommend_city(date: str) -> dict:
    ...
```

```python
def search_restaurants(city: str) -> list:
    ...
```

```python
def save_report(date: str, city_info: dict, restaurants: list):
    ...
```

```python
def save_markdown(date: str, city_info: dict, restaurants: list):
    ...
```

## 개선 확인

다음 기능은 현재 코드에 추가될 경우 평가 범위를 확장할 수 있습니다.

- timeout
- `try-except`
- LLM schema validation
- retry
- cache
- normalization
- Provider abstraction
- logging
- tests


---

# 부록 2. 평가 및 기술 검토 자료

## 검토 목적

이 부록은 프로젝트를 평가하거나 발표할 때 현재 코드의 동작을 빠르게 확인하기 위한 자료입니다.

## 확인 항목

| 항목 | 현재 코드 기준 |
|---|---|
| 날짜 입력 | `argparse --date` |
| 날짜 검증 | `valid_date()` |
| AI 호출 | `recommend_city()` |
| 지도 검색 | `search_restaurants()` |
| JSON 저장 | `save_report()` |
| Markdown 저장 | `save_markdown()` |
| 환경 변수 | `load_dotenv()` |
| 결과 폴더 | `results/` |

## 데이터 흐름

```text
CLI
 ↓
valid_date
 ↓
recommend_city
 ↓
search_restaurants
 ↓
save_report
 ↓
save_markdown
```

## 평가 시 확인할 코드

```python
def recommend_city(date: str) -> dict:
    ...
```

```python
def search_restaurants(city: str) -> list:
    ...
```

```python
def save_report(date: str, city_info: dict, restaurants: list):
    ...
```

```python
def save_markdown(date: str, city_info: dict, restaurants: list):
    ...
```

## 개선 확인

다음 기능은 현재 코드에 추가될 경우 평가 범위를 확장할 수 있습니다.

- timeout
- `try-except`
- LLM schema validation
- retry
- cache
- normalization
- Provider abstraction
- logging
- tests


---

# 부록 3. 평가 및 기술 검토 자료

## 검토 목적

이 부록은 프로젝트를 평가하거나 발표할 때 현재 코드의 동작을 빠르게 확인하기 위한 자료입니다.

## 확인 항목

| 항목 | 현재 코드 기준 |
|---|---|
| 날짜 입력 | `argparse --date` |
| 날짜 검증 | `valid_date()` |
| AI 호출 | `recommend_city()` |
| 지도 검색 | `search_restaurants()` |
| JSON 저장 | `save_report()` |
| Markdown 저장 | `save_markdown()` |
| 환경 변수 | `load_dotenv()` |
| 결과 폴더 | `results/` |

## 데이터 흐름

```text
CLI
 ↓
valid_date
 ↓
recommend_city
 ↓
search_restaurants
 ↓
save_report
 ↓
save_markdown
```

## 평가 시 확인할 코드

```python
def recommend_city(date: str) -> dict:
    ...
```

```python
def search_restaurants(city: str) -> list:
    ...
```

```python
def save_report(date: str, city_info: dict, restaurants: list):
    ...
```

```python
def save_markdown(date: str, city_info: dict, restaurants: list):
    ...
```

## 개선 확인

다음 기능은 현재 코드에 추가될 경우 평가 범위를 확장할 수 있습니다.

- timeout
- `try-except`
- LLM schema validation
- retry
- cache
- normalization
- Provider abstraction
- logging
- tests


---

# 부록 4. 평가 및 기술 검토 자료

## 검토 목적

이 부록은 프로젝트를 평가하거나 발표할 때 현재 코드의 동작을 빠르게 확인하기 위한 자료입니다.

## 확인 항목

| 항목 | 현재 코드 기준 |
|---|---|
| 날짜 입력 | `argparse --date` |
| 날짜 검증 | `valid_date()` |
| AI 호출 | `recommend_city()` |
| 지도 검색 | `search_restaurants()` |
| JSON 저장 | `save_report()` |
| Markdown 저장 | `save_markdown()` |
| 환경 변수 | `load_dotenv()` |
| 결과 폴더 | `results/` |

## 데이터 흐름

```text
CLI
 ↓
valid_date
 ↓
recommend_city
 ↓
search_restaurants
 ↓
save_report
 ↓
save_markdown
```

## 평가 시 확인할 코드

```python
def recommend_city(date: str) -> dict:
    ...
```

```python
def search_restaurants(city: str) -> list:
    ...
```

```python
def save_report(date: str, city_info: dict, restaurants: list):
    ...
```

```python
def save_markdown(date: str, city_info: dict, restaurants: list):
    ...
```

## 개선 확인

다음 기능은 현재 코드에 추가될 경우 평가 범위를 확장할 수 있습니다.

- timeout
- `try-except`
- LLM schema validation
- retry
- cache
- normalization
- Provider abstraction
- logging
- tests


---

# 부록 5. 평가 및 기술 검토 자료

## 검토 목적

이 부록은 프로젝트를 평가하거나 발표할 때 현재 코드의 동작을 빠르게 확인하기 위한 자료입니다.

## 확인 항목

| 항목 | 현재 코드 기준 |
|---|---|
| 날짜 입력 | `argparse --date` |
| 날짜 검증 | `valid_date()` |
| AI 호출 | `recommend_city()` |
| 지도 검색 | `search_restaurants()` |
| JSON 저장 | `save_report()` |
| Markdown 저장 | `save_markdown()` |
| 환경 변수 | `load_dotenv()` |
| 결과 폴더 | `results/` |

## 데이터 흐름

```text
CLI
 ↓
valid_date
 ↓
recommend_city
 ↓
search_restaurants
 ↓
save_report
 ↓
save_markdown
```

## 평가 시 확인할 코드

```python
def recommend_city(date: str) -> dict:
    ...
```

```python
def search_restaurants(city: str) -> list:
    ...
```

```python
def save_report(date: str, city_info: dict, restaurants: list):
    ...
```

```python
def save_markdown(date: str, city_info: dict, restaurants: list):
    ...
```

## 개선 확인

다음 기능은 현재 코드에 추가될 경우 평가 범위를 확장할 수 있습니다.

- timeout
- `try-except`
- LLM schema validation
- retry
- cache
- normalization
- Provider abstraction
- logging
- tests


---

# 부록 6. 평가 및 기술 검토 자료

## 검토 목적

이 부록은 프로젝트를 평가하거나 발표할 때 현재 코드의 동작을 빠르게 확인하기 위한 자료입니다.

## 확인 항목

| 항목 | 현재 코드 기준 |
|---|---|
| 날짜 입력 | `argparse --date` |
| 날짜 검증 | `valid_date()` |
| AI 호출 | `recommend_city()` |
| 지도 검색 | `search_restaurants()` |
| JSON 저장 | `save_report()` |
| Markdown 저장 | `save_markdown()` |
| 환경 변수 | `load_dotenv()` |
| 결과 폴더 | `results/` |

## 데이터 흐름

```text
CLI
 ↓
valid_date
 ↓
recommend_city
 ↓
search_restaurants
 ↓
save_report
 ↓
save_markdown
```

## 평가 시 확인할 코드

```python
def recommend_city(date: str) -> dict:
    ...
```

```python
def search_restaurants(city: str) -> list:
    ...
```

```python
def save_report(date: str, city_info: dict, restaurants: list):
    ...
```

```python
def save_markdown(date: str, city_info: dict, restaurants: list):
    ...
```

## 개선 확인

다음 기능은 현재 코드에 추가될 경우 평가 범위를 확장할 수 있습니다.

- timeout
- `try-except`
- LLM schema validation
- retry
- cache
- normalization
- Provider abstraction
- logging
- tests


---

# 부록 7. 평가 및 기술 검토 자료

## 검토 목적

이 부록은 프로젝트를 평가하거나 발표할 때 현재 코드의 동작을 빠르게 확인하기 위한 자료입니다.

## 확인 항목

| 항목 | 현재 코드 기준 |
|---|---|
| 날짜 입력 | `argparse --date` |
| 날짜 검증 | `valid_date()` |
| AI 호출 | `recommend_city()` |
| 지도 검색 | `search_restaurants()` |
| JSON 저장 | `save_report()` |
| Markdown 저장 | `save_markdown()` |
| 환경 변수 | `load_dotenv()` |
| 결과 폴더 | `results/` |

## 데이터 흐름

```text
CLI
 ↓
valid_date
 ↓
recommend_city
 ↓
search_restaurants
 ↓
save_report
 ↓
save_markdown
```

## 평가 시 확인할 코드

```python
def recommend_city(date: str) -> dict:
    ...
```

```python
def search_restaurants(city: str) -> list:
    ...
```

```python
def save_report(date: str, city_info: dict, restaurants: list):
    ...
```

```python
def save_markdown(date: str, city_info: dict, restaurants: list):
    ...
```

## 개선 확인

다음 기능은 현재 코드에 추가될 경우 평가 범위를 확장할 수 있습니다.

- timeout
- `try-except`
- LLM schema validation
- retry
- cache
- normalization
- Provider abstraction
- logging
- tests


---

# 부록 8. 평가 및 기술 검토 자료

## 검토 목적

이 부록은 프로젝트를 평가하거나 발표할 때 현재 코드의 동작을 빠르게 확인하기 위한 자료입니다.

## 확인 항목

| 항목 | 현재 코드 기준 |
|---|---|
| 날짜 입력 | `argparse --date` |
| 날짜 검증 | `valid_date()` |
| AI 호출 | `recommend_city()` |
| 지도 검색 | `search_restaurants()` |
| JSON 저장 | `save_report()` |
| Markdown 저장 | `save_markdown()` |
| 환경 변수 | `load_dotenv()` |
| 결과 폴더 | `results/` |

## 데이터 흐름

```text
CLI
 ↓
valid_date
 ↓
recommend_city
 ↓
search_restaurants
 ↓
save_report
 ↓
save_markdown
```

## 평가 시 확인할 코드

```python
def recommend_city(date: str) -> dict:
    ...
```

```python
def search_restaurants(city: str) -> list:
    ...
```

```python
def save_report(date: str, city_info: dict, restaurants: list):
    ...
```

```python
def save_markdown(date: str, city_info: dict, restaurants: list):
    ...
```

## 개선 확인

다음 기능은 현재 코드에 추가될 경우 평가 범위를 확장할 수 있습니다.

- timeout
- `try-except`
- LLM schema validation
- retry
- cache
- normalization
- Provider abstraction
- logging
- tests


---

# 부록 9. 평가 및 기술 검토 자료

## 검토 목적

이 부록은 프로젝트를 평가하거나 발표할 때 현재 코드의 동작을 빠르게 확인하기 위한 자료입니다.

## 확인 항목

| 항목 | 현재 코드 기준 |
|---|---|
| 날짜 입력 | `argparse --date` |
| 날짜 검증 | `valid_date()` |
| AI 호출 | `recommend_city()` |
| 지도 검색 | `search_restaurants()` |
| JSON 저장 | `save_report()` |
| Markdown 저장 | `save_markdown()` |
| 환경 변수 | `load_dotenv()` |
| 결과 폴더 | `results/` |

## 데이터 흐름

```text
CLI
 ↓
valid_date
 ↓
recommend_city
 ↓
search_restaurants
 ↓
save_report
 ↓
save_markdown
```

## 평가 시 확인할 코드

```python
def recommend_city(date: str) -> dict:
    ...
```

```python
def search_restaurants(city: str) -> list:
    ...
```

```python
def save_report(date: str, city_info: dict, restaurants: list):
    ...
```

```python
def save_markdown(date: str, city_info: dict, restaurants: list):
    ...
```

## 개선 확인

다음 기능은 현재 코드에 추가될 경우 평가 범위를 확장할 수 있습니다.

- timeout
- `try-except`
- LLM schema validation
- retry
- cache
- normalization
- Provider abstraction
- logging
- tests


---

# 부록 10. 평가 및 기술 검토 자료

## 검토 목적

이 부록은 프로젝트를 평가하거나 발표할 때 현재 코드의 동작을 빠르게 확인하기 위한 자료입니다.

## 확인 항목

| 항목 | 현재 코드 기준 |
|---|---|
| 날짜 입력 | `argparse --date` |
| 날짜 검증 | `valid_date()` |
| AI 호출 | `recommend_city()` |
| 지도 검색 | `search_restaurants()` |
| JSON 저장 | `save_report()` |
| Markdown 저장 | `save_markdown()` |
| 환경 변수 | `load_dotenv()` |
| 결과 폴더 | `results/` |

## 데이터 흐름

```text
CLI
 ↓
valid_date
 ↓
recommend_city
 ↓
search_restaurants
 ↓
save_report
 ↓
save_markdown
```

## 평가 시 확인할 코드

```python
def recommend_city(date: str) -> dict:
    ...
```

```python
def search_restaurants(city: str) -> list:
    ...
```

```python
def save_report(date: str, city_info: dict, restaurants: list):
    ...
```

```python
def save_markdown(date: str, city_info: dict, restaurants: list):
    ...
```

## 개선 확인

다음 기능은 현재 코드에 추가될 경우 평가 범위를 확장할 수 있습니다.

- timeout
- `try-except`
- LLM schema validation
- retry
- cache
- normalization
- Provider abstraction
- logging
- tests


---

# 부록 11. 평가 및 기술 검토 자료

## 검토 목적

이 부록은 프로젝트를 평가하거나 발표할 때 현재 코드의 동작을 빠르게 확인하기 위한 자료입니다.

## 확인 항목

| 항목 | 현재 코드 기준 |
|---|---|
| 날짜 입력 | `argparse --date` |
| 날짜 검증 | `valid_date()` |
| AI 호출 | `recommend_city()` |
| 지도 검색 | `search_restaurants()` |
| JSON 저장 | `save_report()` |
| Markdown 저장 | `save_markdown()` |
| 환경 변수 | `load_dotenv()` |
| 결과 폴더 | `results/` |

## 데이터 흐름

```text
CLI
 ↓
valid_date
 ↓
recommend_city
 ↓
search_restaurants
 ↓
save_report
 ↓
save_markdown
```

## 평가 시 확인할 코드

```python
def recommend_city(date: str) -> dict:
    ...
```

```python
def search_restaurants(city: str) -> list:
    ...
```

```python
def save_report(date: str, city_info: dict, restaurants: list):
    ...
```

```python
def save_markdown(date: str, city_info: dict, restaurants: list):
    ...
```

## 개선 확인

다음 기능은 현재 코드에 추가될 경우 평가 범위를 확장할 수 있습니다.

- timeout
- `try-except`
- LLM schema validation
- retry
- cache
- normalization
- Provider abstraction
- logging
- tests


---

# 부록 12. 평가 및 기술 검토 자료

## 검토 목적

이 부록은 프로젝트를 평가하거나 발표할 때 현재 코드의 동작을 빠르게 확인하기 위한 자료입니다.

## 확인 항목

| 항목 | 현재 코드 기준 |
|---|---|
| 날짜 입력 | `argparse --date` |
| 날짜 검증 | `valid_date()` |
| AI 호출 | `recommend_city()` |
| 지도 검색 | `search_restaurants()` |
| JSON 저장 | `save_report()` |
| Markdown 저장 | `save_markdown()` |
| 환경 변수 | `load_dotenv()` |
| 결과 폴더 | `results/` |

## 데이터 흐름

```text
CLI
 ↓
valid_date
 ↓
recommend_city
 ↓
search_restaurants
 ↓
save_report
 ↓
save_markdown
```

## 평가 시 확인할 코드

```python
def recommend_city(date: str) -> dict:
    ...
```

```python
def search_restaurants(city: str) -> list:
    ...
```

```python
def save_report(date: str, city_info: dict, restaurants: list):
    ...
```

```python
def save_markdown(date: str, city_info: dict, restaurants: list):
    ...
```

## 개선 확인

다음 기능은 현재 코드에 추가될 경우 평가 범위를 확장할 수 있습니다.

- timeout
- `try-except`
- LLM schema validation
- retry
- cache
- normalization
- Provider abstraction
- logging
- tests


---

# 부록 13. 평가 및 기술 검토 자료

## 검토 목적

이 부록은 프로젝트를 평가하거나 발표할 때 현재 코드의 동작을 빠르게 확인하기 위한 자료입니다.

## 확인 항목

| 항목 | 현재 코드 기준 |
|---|---|
| 날짜 입력 | `argparse --date` |
| 날짜 검증 | `valid_date()` |
| AI 호출 | `recommend_city()` |
| 지도 검색 | `search_restaurants()` |
| JSON 저장 | `save_report()` |
| Markdown 저장 | `save_markdown()` |
| 환경 변수 | `load_dotenv()` |
| 결과 폴더 | `results/` |

## 데이터 흐름

```text
CLI
 ↓
valid_date
 ↓
recommend_city
 ↓
search_restaurants
 ↓
save_report
 ↓
save_markdown
```

## 평가 시 확인할 코드

```python
def recommend_city(date: str) -> dict:
    ...
```

```python
def search_restaurants(city: str) -> list:
    ...
```

```python
def save_report(date: str, city_info: dict, restaurants: list):
    ...
```

```python
def save_markdown(date: str, city_info: dict, restaurants: list):
    ...
```

## 개선 확인

다음 기능은 현재 코드에 추가될 경우 평가 범위를 확장할 수 있습니다.

- timeout
- `try-except`
- LLM schema validation
- retry
- cache
- normalization
- Provider abstraction
- logging
- tests


---

# 부록 14. 평가 및 기술 검토 자료

## 검토 목적

이 부록은 프로젝트를 평가하거나 발표할 때 현재 코드의 동작을 빠르게 확인하기 위한 자료입니다.

## 확인 항목

| 항목 | 현재 코드 기준 |
|---|---|
| 날짜 입력 | `argparse --date` |
| 날짜 검증 | `valid_date()` |
| AI 호출 | `recommend_city()` |
| 지도 검색 | `search_restaurants()` |
| JSON 저장 | `save_report()` |
| Markdown 저장 | `save_markdown()` |
| 환경 변수 | `load_dotenv()` |
| 결과 폴더 | `results/` |

## 데이터 흐름

```text
CLI
 ↓
valid_date
 ↓
recommend_city
 ↓
search_restaurants
 ↓
save_report
 ↓
save_markdown
```

## 평가 시 확인할 코드

```python
def recommend_city(date: str) -> dict:
    ...
```

```python
def search_restaurants(city: str) -> list:
    ...
```

```python
def save_report(date: str, city_info: dict, restaurants: list):
    ...
```

```python
def save_markdown(date: str, city_info: dict, restaurants: list):
    ...
```

## 개선 확인

다음 기능은 현재 코드에 추가될 경우 평가 범위를 확장할 수 있습니다.

- timeout
- `try-except`
- LLM schema validation
- retry
- cache
- normalization
- Provider abstraction
- logging
- tests


---

# 부록 15. 평가 및 기술 검토 자료

## 검토 목적

이 부록은 프로젝트를 평가하거나 발표할 때 현재 코드의 동작을 빠르게 확인하기 위한 자료입니다.

## 확인 항목

| 항목 | 현재 코드 기준 |
|---|---|
| 날짜 입력 | `argparse --date` |
| 날짜 검증 | `valid_date()` |
| AI 호출 | `recommend_city()` |
| 지도 검색 | `search_restaurants()` |
| JSON 저장 | `save_report()` |
| Markdown 저장 | `save_markdown()` |
| 환경 변수 | `load_dotenv()` |
| 결과 폴더 | `results/` |

## 데이터 흐름

```text
CLI
 ↓
valid_date
 ↓
recommend_city
 ↓
search_restaurants
 ↓
save_report
 ↓
save_markdown
```

## 평가 시 확인할 코드

```python
def recommend_city(date: str) -> dict:
    ...
```

```python
def search_restaurants(city: str) -> list:
    ...
```

```python
def save_report(date: str, city_info: dict, restaurants: list):
    ...
```

```python
def save_markdown(date: str, city_info: dict, restaurants: list):
    ...
```

## 개선 확인

다음 기능은 현재 코드에 추가될 경우 평가 범위를 확장할 수 있습니다.

- timeout
- `try-except`
- LLM schema validation
- retry
- cache
- normalization
- Provider abstraction
- logging
- tests
