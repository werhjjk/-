import requests
import json

# 1. 설정
WEBHOOK_URL = "https://discord.com/api/webhooks/1482326991939309573/0qINgz4w9dKTuBvvEmDJYlxzksYuN5TqPkbM4bhlMk5FKIzmZyg0KnGUhwsWpQoXIVRS"
NEWS_API_KEY = "9609ec24112b4ff897c5d1bff362ca28" # 발급받은 키를 여기에 넣으세요!

def get_weather_info():
    url = "https://api.open-meteo.com/v1/forecast?latitude=35.1796&longitude=129.0756&current_weather=true&daily=precipitation_probability_max&timezone=Asia/Seoul"
    res = requests.get(url).json()
    return res['current_weather']['temperature'], res['daily']['precipitation_probability_max'][0]

def get_real_news():
    # 한국(country=kr)의 최신 뉴스 가져오기
    url = f"https://newsapi.org/v2/top-headlines?country=kr&apiKey={NEWS_API_KEY}"
    res = requests.get(url).json()
    
    articles = res.get('articles', [])
    news_list = []
    
    # 뉴스 중 상위 3개만 뽑기
    for i, art in enumerate(articles[:3]):
        title = art['title']
        news_list.append(f"{i+1}. {title}")
    
    return "\n".join(news_list) if news_list else "현재 가져올 뉴스 소식이 없습니다."

def get_outfit(temp):
    if temp < 5: return "❄️ 롱패딩, 목도리 필수!"
    elif 5 <= temp < 15: return "🧥 코트나 자켓을 추천해요."
    else: return "👕 가벼운 옷차림이 좋겠어요."

# 메인 실행
try:
    temp, rain = get_weather_info()
    news = get_real_news() # 진짜 뉴스 가져오기 실행!
    outfit = get_outfit(temp)
    
    data = {
        "username": "부산 종합 비서",
        "embeds": [{
            "title": "📅 실시간 정보 브리핑",
            "color": 3447003,
            "fields": [
                {"name": "🌡️ 날씨", "value": f"기온: **{temp}°C**\n비 확률: **{rain}%**", "inline": True},
                {"name": "👕 추천 옷차림", "value": outfit, "inline": False},
                {"name": "📰 실시간 주요 뉴스", "value": news, "inline": False}
            ]
        }]
    }
    requests.post(WEBHOOK_URL, data=json.dumps(data), headers={"Content-Type": "application/json"})
    print("전송 완료!")
except Exception as e:
    print(f"에러: {e}")
