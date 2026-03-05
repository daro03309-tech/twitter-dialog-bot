import time
from twikit import Client

client = Client()

print("쿠키 로그인 중...")

client.load_cookies("cookies.txt")

print("로그인 성공")

# 대사 불러오기
with open("quotes.txt", "r", encoding="utf-8") as f:
    quotes = [q.strip() for q in f.readlines() if q.strip()]

# 인덱스 불러오기
try:
    with open("index.txt", "r") as f:
        index = int(f.read().strip())
except:
    index = 0

# 대사 선택
tweet = quotes[index][:280]

print("트윗 내용:", tweet)

# 트윗 시도
for i in range(3):
    try:
        client.create_tweet(text=tweet)
        print("트윗 성공")
        break
    except Exception as e:
        print("트윗 실패 재시도", i+1)
        time.sleep(5)

# 다음 인덱스 계산
index += 1
if index >= len(quotes):
    index = 0

# 저장
with open("index.txt", "w") as f:
    f.write(str(index))

print("다음 대사 번호:", index)
