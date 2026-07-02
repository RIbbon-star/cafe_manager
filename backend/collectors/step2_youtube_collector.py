import os
import sys
from dotenv import load_dotenv
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()
YOUTUBE_API_KEY = os.environ["YOUTUBE_API_KEY"]

from googleapiclient.discovery import build

def search_youtube(query: str, max_results: int = 5) -> list[dict]:
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    # build() — 라이브러리가 YouTube API 클라이언트 객체를 만들어줌. URL 직접 안 써도 되는 이유가 여기 있음
    response = youtube.search().list(
        q=query,
        part="snippet",
        # snippet — 제목, 설명, 썸네일 등 기본 정보 묶음. 영상 ID도 여기 포함됨
        type="video",
        # type="video" — 재생목록·채널 제외하고 영상만 반환
        maxResults=max_results,
    ).execute()
    # .execute() — 여기서 실제 HTTP 요청이 날아감. Step 1의 requests.get()에 해당하는 부분
    return response["items"]

from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript(video_id: str) -> str | None:
    try:
        ytt = YouTubeTranscriptApi()
    # 인스턴스 생성 후 호출 — 새 버전 방식
        transcript = ytt.fetch(video_id)
        return " ".join([item.text for item in transcript])
    except Exception:
        return None
    # 자막 없는 영상은 None 반환
    # 새 버전은 딕셔너리가 아니라 객체라서 item["text"] 대신 item.text

if __name__ == "__main__":
    results = search_youtube("카페라떼", max_results=3)
    for i, item in enumerate(results, start=1):
        print(f"[{i}] {item["snippet"]["title"]}")
        print(f"    설명: {item["snippet"]["description"]}")
        print()

    for item in results:
        video_id = item["id"]["videoId"]
        text = get_transcript(video_id)
        if text:
            print("--- 자막 ---")
            print(text[:500])
            break