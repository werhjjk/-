import requests
import json

# 1. 아까 복사한 디스코드 웹훅 주소를 여기에 붙여넣으세요
WEBHOOK_URL = "https://discord.com/api/webhooks/1482326991939309573/0qINgz4w9dKTuBvvEmDJYlxzksYuN5TqPkbM4bhlMk5FKIzmZyg0KnGUhwsWpQoXIVRS"

# 2. 서울의 위도와 경도를 이용해 날씨 정보를 가져옵니다
weather_url = "https://api.open-meteo.com/v1/forecast?latitude=35.1796&longitude=129.0756&current_weather=true"
response = requests.get(weather_url).json()

# 날씨 데이터 추출
temp = response['current_weather']['temperature']
wind = response['current_weather']['windspeed']

# 3. 디스코드로 보낼 예쁜 메시지 만들기
data = {
    "content": "📢 **아침 날씨 알림**",
    "embeds": [{
        "title": "오늘의 부산 날씨",
        "description": f"🌡️ 현재 기온: **{temp}°C**\n💨 풍속: **{wind}km/h**",
        "color": 5814783 # 파란색 계열
    }]
}

# 4. 전송!
requests.post(WEBHOOK_URL, data=json.dumps(data), headers={"Content-Type": "application/json"})
print("디스코드로 날씨를 보냈습니다!")