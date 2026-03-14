import requests
import json

# ==========================================
# 1. 설정 (이 부분만 본인 정보로 수정하세요)
# ==========================================
WEBHOOK_URL = "https://discord.com/api/webhooks/1482326991939309573/0qINgz4w9dKTuBvvEmDJYlxzksYuN5TqPkbM4bhlMk5FKIzmZyg0KnGUhwsWpQoXIVRS"
NEWS_API_KEY = "9609ec24112b4ff897c5d1bff362ca28"

def get_weather_info():
    """부산 날씨와 비 확률을 가져옵니다."""
    url = "https://api.open-meteo.com/v1/forecast?latitude=35.1796&longitude=129.0756&current_weather=true&daily=precipitation_probability_max&timezone=Asia/Seoul"
    res = requests.get(url).json()
    temp = res['current_weather']['temperature']
    rain_chance = res['daily']['precipitation_probability_max'][0]
    return temp, rain_chance

def get_sports_news():
    """실시간 스포츠 뉴스 상위 3개를 링크와 함께 가져옵니다."""
    url = f"https://newsapi.org/v2/top-headlines?country=kr&category=sports&apiKey={NEWS_API_KEY}"
    res = requests.get(url).json()
    articles = res.get('articles', [])
    
    # 헤드라인이 없을 경우 검색 모드
    if not articles:
        search_url = f"https://newsapi.org/v2/everything?q=스포츠&sortBy=publishedAt&language=ko&apiKey={NEWS_API_KEY}"
        res = requests.get(search_url).json()
        articles = res.get('articles', [])

    news_list = []
    for art in articles:
        title = art.get('title')
        url = art.get('url')
        if title and title != '[Removed]' and url:
            # 제목에서 언론사 이름 제거하고 깔끔하게 정리
            clean_title = title.split(' - ')[0]
            news_list.append(f"🏆 [{clean_title}]({url})")
        if len(news_list) >= 3:
            break
    return "\n".join(news_list) if news_list else "현재 스포츠 뉴스 소식이 없습니다."

def get_outfit(temp):
    """기온에 맞는 옷차림을 추천합니다."""
    if temp < 5: return "❄️ **롱패딩, 목도리, 장갑** 필수! 단단히 입으세요."
    elif 5 <= temp < 10: return "🧥 **코트나 경량패딩**, 히트텍을 추천해요."
    elif 10 <= temp < 17: return "🧥 **자켓, 가디건, 기모 맨투맨**이 적당해요."
    elif 17 <= temp < 23: return "👕 **니트, 맨투맨, 긴팔 티셔츠**를 입으세요."
    else: return "☀️ **반팔 티셔츠와 얇은 셔츠**가 좋겠어요."

# ==========================================
# 2. 실행 및 전송 부분
# ==========================================
try:
    # 데이터 수집
    temp, rain = get_weather_info()
    news = get_sports_news()
    outfit = get_outfit(temp)
    
    # 비 소식 조건문
    rain_msg = "☔ 비 소식이 있어요. **우산 꼭 챙기세요!**" if rain > 50 else "☀️ 오늘은 우산 없이 가벼운 발걸음으로!"

    # 디스코드 메시지 구성 (Embed 형식)
    data = {
        "username": "부산 브리핑 비서",
        "avatar_url": "https://cdn-icons-png.flaticon.com/512/4343/4343003.png", # 귀여운 로봇 아이콘
        "embeds": [{
            "title": "📅 오늘 아침 종합 브리핑",
            "description": f"좋은 아침입니다! 오늘 부산의 주요 정보를 정리해 드립니다.",
            "color": 3447003, # 푸른색
            "fields": [
                {
                    "name": "🌡️ 날씨 및 강수",
                    "value": f"현재 기온: **{temp}°C**\n비 올 확률: **{rain}%**\n{rain_msg}",
                    "inline": False
                },
                {
                    "name": "👕 추천 옷차림",
                    "value": outfit,
                    "inline": False
                },
                {
                    "name": "📰 실시간 스포츠 뉴스",
                    "value": news,
                    "inline": False
                }
            ],
            "footer": {
                "text": "오늘도 멋진 하루 보내세요! 💪"
            },
            "timestamp": None # 현재 시간 표시 원할 시 설정 가능
        }]
    }

    # 전송
    response = requests.post(WEBHOOK_URL, data=json.dumps(data), headers={"Content-Type": "application/json"})
    
    if response.status_code == 204:
        print("전송 성공!")
    else:
        print(f"전송 실패: {response.status_code}")

except Exception as e:
    print(f"오류 발생: {e}")
