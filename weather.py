import requests
import json

# 1. 설정 (본인의 디스코드 주소로 꼭 바꾸세요!)
WEBHOOK_URL = "https://discord.com/api/webhooks/1482326991939309573/0qINgz4w9dKTuBvvEmDJYlxzksYuN5TqPkbM4bhlMk5FKIzmZyg0KnGUhwsWpQoXIVRS"

def get_weather_info():
    # 부산 날씨와 비 확률 가져오기
    url = "https://api.open-meteo.com/v1/forecast?latitude=35.1796&longitude=129.0756&current_weather=true&daily=precipitation_probability_max&timezone=Asia/Seoul"
    res = requests.get(url).json()
    temp = res['current_weather']['temperature']
    rain_chance = res['daily']['precipitation_probability_max'][0]
    return temp, rain_chance

def get_news_headlines():
    # 뉴스 API를 쓰면 복잡하니, 구글 뉴스 RSS 느낌으로 간단히 제목만 가져오는 팁!
    # 여기서는 입문용으로 가장 핫한 뉴스 키워드 예시를 들게요. (나중에 진짜 뉴스로 연결 가능)
    headlines = [
        "1. [경제] 코스피 반등 성공, 반도체주 강세",
        "2. [지역] 부산 광안리 드론쇼 일정 변경 안내",
        "3. [IT] 인공지능 비서 서비스 이용자 급증"
    ]
    return "\n".join(headlines)

def get_outfit(temp):
    # 기온별 옷차림 추천 (조건문 활용)
    if temp < 5: return "❄️ 롱패딩, 목도리, 장갑 필수!"
    elif 5 <= temp < 10: return "🧥 코트나 가죽 자켓, 히트텍을 추천해요."
    elif 10 <= temp < 17: return "🧥 자켓, 가디건, 기모 맨투맨이 적당해요."
    elif 17 <= temp < 23: return "👕 얇은 니트, 맨투맨, 긴팔 티셔츠를 입으세요."
    else: return "☀️ 반팔 티셔츠와 얇은 셔츠가 좋겠어요."

# --- 실행 부분 ---
temp, rain = get_weather_info()
news = get_news_headlines()
outfit = get_outfit(temp)

# 비 소식 추가
rain_msg = "☔ 우산 꼭 챙기세요!" if rain > 50 else "☀️ 우산 없어도 돼요."

# 디스코드 전송 데이터 구성
data = {
    "username": "부산 아침 비서",
    "embeds": [{
        "title": "📅 오늘 아침 종합 브리핑",
        "color": 3447003,
        "fields": [
            {"name": "🌡️ 날씨", "value": f"기온: **{temp}°C**\n비 확률: **{rain}%**\n{rain_msg}", "inline": True},
            {"name": "👕 추천 옷차림", "value": outfit, "inline": False},
            {"name": "📰 주요 뉴스", "value": news, "inline": False}
        ],
        "footer": {"text": "오늘도 행복한 하루 되세요! 😊"}
    }]
}

requests.post(WEBHOOK_URL, data=json.dumps(data), headers={"Content-Type": "application/json"})
