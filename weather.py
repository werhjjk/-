import requests
import json

# 1. 본인의 디스코드 웹훅 주소
WEBHOOK_URL = "https://discord.com/api/webhooks/1482326991939309573/0qINgz4w9dKTuBvvEmDJYlxzksYuN5TqPkbM4bhlMk5FKIzmZyg0KnGUhwsWpQoXIVRS"

# 2. 부산 날씨 가져오기 (비 올 확률을 알기 위해 daily 옵션 추가)
# latitude=35.17, longitude=129.07 (부산)
weather_url = "https://api.open-meteo.com/v1/forecast?latitude=35.1796&longitude=129.0756&current_weather=true&daily=precipitation_probability_max&timezone=Asia/Seoul"

response = requests.get(weather_url).json()

# 현재 기온과 오늘 비 올 확률(최대값) 추출
temp = response['current_weather']['temperature']
rain_chance = response['daily']['precipitation_probability_max'][0] # 오늘(0번째 날)의 비 확률

# 3. [핵심] 조건문으로 멘트 정하기
rain_comment = ""
if rain_chance > 50:
    rain_comment = "☔ 오늘 비 올 확률이 높아요! **우산 꼭 챙기세요!**"
elif rain_chance > 20:
    rain_comment = "☁️ 비가 올 수도 있으니 혹시 모르니 작은 우산 챙기세요."
else:
    rain_comment = "☀️ 오늘은 비 소식이 없네요. 가벼운 마음으로 외출하세요!"

# 4. 디스코드 메시지 전송
data = {
    "content": "📢 **부산 아침 날씨 알림**",
    "embeds": [{
        "title": "📍 오늘의 부산 날씨 요약",
        "description": f"🌡️ 현재 기온: **{temp}°C**\n💧 비 올 확률: **{rain_chance}%**\n\n💡 {rain_comment}",
        "color": 16776960 if rain_chance > 50 else 3447003 # 비오면 노란색, 아니면 푸른색
    }]
}

requests.post(WEBHOOK_URL, data=json.dumps(data), headers={"Content-Type": "application/json"})
print(f"전송 완료! (비 확률: {rain_chance}%)")
