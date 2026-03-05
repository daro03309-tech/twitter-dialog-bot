import os
import json
import random
from twikit import Client

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

with open("quotes.txt", "r", encoding="utf-8") as f:
    lines = f.read().splitlines()

tweet = random.choice(lines)

print("트윗:", tweet)

client.create_tweet(text=tweet)

print("트윗 완료")
