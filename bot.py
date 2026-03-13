import os
import json
import random
import asyncio
from twikit import Client


async def human_delay(a, b):
    t = random.uniform(a, b)
    print(f"{round(t,1)}초 대기...")
    await asyncio.sleep(t)


async def random_human_actions(client):

    actions = [
        "timeline",
        "profile",
        "search"
    ]

    random.shuffle(actions)

    for act in actions[:2]:

        try:
            if act == "timeline":
                print("타임라인 확인...")
                await client.get_home_timeline()

            elif act == "profile":
                print("프로필 방문...")
                await client.get_user_by_screen_name("Ren_k107")

            elif act == "search":
                print("검색 행동...")
                await client.search_tweet("오늘", "Latest")

        except:
            pass

        await human_delay(40, 120)


async def main():

    print("쿠키 로그인 중...")

    client = Client()

    raw = json.loads(os.environ["TWITTER_COOKIES"])

    if isinstance(raw, list):
        cookies = {c["name"]: c["value"] for c in raw}
    else:
        cookies = raw

    client.set_cookies(cookies)

    print("로그인 성공")

    # 로그인 후 충분히 기다림
    await human_delay(60, 180)

    # 인간 행동 시뮬레이션
    await random_human_actions(client)

    # 트윗 전 대기
    await human_delay(90, 240)

    # 대사 로드
    with open("quotes.txt", "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    tweet = random.choice(lines)

    print("선택된 트윗:", tweet)

    # 트윗 재시도
    for i in range(3):

        try:
            print(f"트윗 시도 {i+1}/3")

            await client.create_tweet(text=tweet)

            print("트윗 성공")
            return

        except Exception as e:

            print("트윗 실패:", e)

            if i < 2:

                wait = random.uniform(300, 900)  # 5~15분
                print(f"{round(wait,1)}초 후 재시도")

                await asyncio.sleep(wait)

    print("트윗 최종 실패")


asyncio.run(main())
