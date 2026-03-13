import os
import json
import random
import asyncio
import time
from twikit import Client

STATE_FILE = "state.json"


async def human_delay(a, b):
    t = random.uniform(a, b)
    print(f"{round(t,1)}초 대기...")
    await asyncio.sleep(t)


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)

    return {
        "last_quote": "",
        "next_tweet_time": 0
    }


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


async def random_human_actions(client):

    actions = ["timeline", "profile"]
    random.shuffle(actions)

    for act in actions:

        try:

            if act == "timeline":
                print("타임라인 확인...")
                await client.get_home_timeline()

            if act == "profile":
                print("프로필 방문...")
                await client.get_user_by_screen_name("Ren_k107")

        except:
            pass

        await human_delay(40, 120)


async def main():

    state = load_state()

    now = time.time()

    # 처음 실행 시 다음 트윗 시간 생성
    if state["next_tweet_time"] == 0:

        interval = random.uniform(36000, 50400)

        state["next_tweet_time"] = now + interval

        save_state(state)

        print("첫 실행. 다음 트윗 시간 생성.")
        return


    # 아직 트윗 시간이 아님
    if now < state["next_tweet_time"]:

        remaining = state["next_tweet_time"] - now

        print(f"다음 트윗까지 {round(remaining/3600,2)}시간 남음")

        return


    print("쿠키 로그인 중...")

    client = Client()

    raw = json.loads(os.environ["TWITTER_COOKIES"])

    if isinstance(raw, list):
        cookies = {c["name"]: c["value"] for c in raw}
    else:
        cookies = raw

    client.set_cookies(cookies)

    print("로그인 성공")

    await human_delay(60, 180)

    await random_human_actions(client)

    # 트윗 직전 긴 대기 (봇 탐지 회피)
    await human_delay(180, 420)

    with open("quotes.txt", "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    tweet = random.choice(lines)

    # 직전 트윗 중복 방지
    while tweet == state["last_quote"]:
        tweet = random.choice(lines)

    print("선택된 트윗:", tweet)

    try:

        await client.create_tweet(text=tweet)

        print("트윗 성공")

        state["last_quote"] = tweet

        # 다음 트윗 시간 새로 설정
        interval = random.uniform(36000, 50400)

        state["next_tweet_time"] = time.time() + interval

        save_state(state)

    except Exception as e:

        print("트윗 실패:", e)

        # 실패하면 다음 실행에서 다시 시도
        state["next_tweet_time"] = time.time() + random.uniform(3600, 7200)

        save_state(state)

        print("다음 실행에서 다시 시도")


asyncio.run(main())
