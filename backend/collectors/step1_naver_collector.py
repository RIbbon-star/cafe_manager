import os
# 환경변수(API 키)를 읽기 위해
import sys

import requests
# HTTP 호출
from dotenv import load_dotenv
# load_dotenv() — .env 파일을 읽어 os.environ에 주입. 이 줄이 있어야 터미널에서 별도로 export 안 해도 .env가 자동 적용됨

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
# 윈도우 콘솔 기본 인코딩(cp949) 문제 방지용.
# hasattr로 먼저 확인하는 이유: 주피터 노트북의 stdout은 Jupyter 전용 OutStream 객체라 reconfigure가 없음.
# hasattr이 False면 건너뜀 → 터미널/노트북 양쪽에서 에러 없이 동작

load_dotenv()

NAVER_CLIENT_ID = os.environ["NAVER_CLIENT_ID"]
NAVER_CLIENT_SECRET = os.environ["NAVER_CLIENT_SECRET"]
# 대괄호 접근([]) — 키가 없으면 KeyError로 즉시 실패. .get()을 안 쓰는 이유: 조용히 None이 되어 나중에 API가 401을 뱉는 것보다, 시작 시점에 바로 원인을 알려주는 게 디버깅에 유리하기 때문

API_URL = "https://openapi.naver.com/v1/search/blog.json"
# 상수로 분리 — 나중에 쇼핑 API 등 다른 엔드포인트 추가 시 같은 패턴 재사용


def search_blog(query: str, display: int = 10, sort: str = "sim") -> list[dict]:
# 타입 힌트 + 기본값 — search_blog("아인슈페너")만 호출해도 동작하도록
    """네이버 블로그 검색 결과를 리스트로 반환한다.

    Args:
        query: 검색어 (예: "아인슈페너 레시피")
        display: 가져올 결과 수 (최대 100)
        sort: "sim"=정확도순, "date"=최신순
    """
    headers = {
    # 네이버 API는 인증 정보를 URL 파라미터가 아니라 HTTP 헤더로 요구함
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
    }
    params = {"query": query, "display": display, "sort": sort}
    # params를 딕셔너리로 넘기면 requests가 ?query=...&display=5 형태로 자동 조립 (한글 URL 인코딩도 알아서 처리)
    resp = requests.get(API_URL, headers=headers, params=params, timeout=10) # timeout=10 — 응답이 10초 안에 안 오면 포기. 없으면 무한 대기 가능
    resp.raise_for_status() # 200이 아니면 여기서 예외 발생. 이 줄이 없으면 키가 틀려도(401) 에러 없이 빈 데이터로 넘어가서 다음 단계에서 원인 불명 오류가 남 200  → OK, 성공 401  → Unauthorized, 인증 실패 (키가 틀림) 404  → Not Found 500  → 서버 에러
    return resp.json()["items"] # ["items"] — 응답 JSON에서 검색 결과 배열만 추출


if __name__ == "__main__":
# 이 파일을 직접 실행할 때만 아래 테스트 코드가 돎. 나중에 from collectors.step1_naver_collector import search_blog로 가져다 쓸 때는 실행 안 됨 — 모듈 조립의 핵심 관례
    results = search_blog("아인슈페너 레시피", display=5)
    for i, item in enumerate(results, start=1):
        print(f"[{i}] {item['title']}")
        print(f"    링크: {item['link']}")
        print(f"    요약: {item['description'][:60]}...")
        print()
