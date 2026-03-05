import os
import json
import random
import asyncio
from twikit import Client

async def post_tweet(client, tweet, retry=3):

    for attempt in range(retry):
        try:
            print(f"트윗 시도 {attempt+1}/{retry}")

            await client.create_tweet(text=tweet)

            print("트윗 완료")
            return True

        except Exception as e:
            print("트윗 실패:", e)

            if attempt < retry - 1:
                print("5초 후 재시도...")
                await asyncio.sleep(5)

    print("트윗 최종 실패")
    return False


async def main():

    try:

        print("쿠키 로그인 중...")

        client = Client()

        raw = json.loads(os.environ["TWITTER_COOKIES"])

        # 쿠키 형식 자동 변환
        if isinstance(raw, list):
            cookies = {c["name"]: c["value"] for c in raw}
        else:
            cookies = raw

        client.set_cookies(cookies)

        print("로그인 성공")

        if not os.path.exists("quotes.txt"):
            print("quotes.txt 파일이 없습니다.")
            return

        with open("quotes.txt", "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]

        if not lines:
            print("quotes.txt에 트윗할 문장이 없습니다.")
            return

        tweet = random.choice(lines)

        print("선택된 트윗:", tweet)

        # 트윗 전에 약간 대기 (봇 감지 방지)
        await asyncio.sleep(random.uniform(2, 5))

        await post_tweet(client, tweet)

    except Exception as e:
        print("전체 실행 오류:", e)


asyncio.run(main())
