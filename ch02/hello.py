import asyncio
import time
from fastapi import FastAPI

app = FastAPI()


# [비동기 전용] 외부 뉴스 호출 시뮬레이션
async def fetch_news_async(source_name: str, delay: float):
    print(f"📡 [Async] {source_name} 수집 시작...")
    await asyncio.sleep(delay)
    return f"{source_name} 데이터"

    # [동기 전용] 외부 뉴스 호출 시뮬레이션


def fetch_news_sync(source_name: str, delay: float):
    print(f" [Sync] {source_name} 수집 시작...")
    time.sleep(delay)  # 서버 전체를 멈추게 함
    return f"{source_name} 데이터"


# 1. 비동기 방식: 모든 요청을 동시에 (약 2.5초 소요)
@app.get("/search-news-async")
async def search_news_async():
    start = time.perf_counter()

    # 세 작업을 동시에 실행 예약
    results = await asyncio.gather(
        fetch_news_async("네이버", 1.5),
        fetch_news_async("다음", 2.5),
        fetch_news_async("구글", 0.5)
    )

    end = time.perf_counter()
    return {"mode": "async", "duration": f"{end - start:.2f}s", "data": results}


# 2. 동기 방식: 하나씩 순서대로 (약 4.5초 소요)
@app.get("/search-news-sync")
def search_news_sync():
    start = time.perf_counter()

    # 하나가 끝나야 다음 줄로 넘어감 (Blocking)
    res1 = fetch_news_sync("네이버", 1.5)
    res2 = fetch_news_sync("다음", 2.5)
    res3 = fetch_news_sync("구글", 0.5)

    end = time.perf_counter()
    return {
        "mode": "sync",
        "duration": f"{end - start:.2f}s",
        "data": [res1, res2, res3]
    }