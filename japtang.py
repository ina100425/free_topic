import streamlit as st
import random
import requests
import time
import base64
import feedparser  # 📰 뉴스 기능을 위해 추가
from streamlit_lottie import st_lottie

# ==========================================
# 🔑 API 키
OPENWEATHER_API_KEY = "a3852a06671ff4ad36b2b4e6269418b9" 
# ==========================================

# 1. 페이지 설정
st.set_page_config(page_title="AX마스터 짬뽕 대시보드", layout="wide", page_icon="🌟")

# 2. 로컬 파일을 바이너리로 읽어오는 함수
def get_local_file_as_base64(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
            return base64.b64encode(data).decode()
    except FileNotFoundError:
        return None

# 파일 경로 정의
JAMPONG_IMAGE_PATH = "jampong.png"
PATRICK_GIF_PATH = "patrick.gif"
ROBOT_IMAGE_PATH = "robot.png"
BODY_FONT_PATH = "kkukkkuk.ttf"
DAHYUN_FONT_PATH = "dahyun.ttf"

# 데이터 로드
body_font_base64 = get_local_file_as_base64(BODY_FONT_PATH)
dahyun_font_base64 = get_local_file_as_base64(DAHYUN_FONT_PATH)
robot_base64 = get_local_file_as_base64(ROBOT_IMAGE_PATH)
robot_img_html = f'<img src="data:image/png;base64,{robot_base64}" width="65" style="border-radius:10px;">' if robot_base64 else "🤖"

# 3. 커스텀 CSS
font_face_style = ""
if body_font_base64:
    font_face_style += f"""
    @font-face {{
        font-family: 'kkukkkuk';
        src: url(data:font/ttf;charset=utf-8;base64,{body_font_base64}) format('truetype');
        font-weight: normal;
        font-style: normal;
    }}
    """
if dahyun_font_base64:
    font_face_style += f"""
    @font-face {{
        font-family: 'dahyun';
        src: url(data:font/ttf;charset=utf-8;base64,{dahyun_font_base64}) format('truetype');
        font-weight: normal;
        font-style: normal;
    }}
    """

st.markdown(
    f"""
    <style>
    {font_face_style}

    html, body, [class*="st-"], .stMarkdown, p, h1, h2, h3, span, label, input, button, textarea, .stMetric, .stSubheader, div {{
        font-family: 'kkukkkuk', sans-serif !important;
        color: #4E342E !important;
        font-weight: 400 !important;
    }}

    .custom-title {{
        font-family: 'kkukkkuk' !important;
        color: #4E342E !important;
        font-size: 3.5rem !important;
        font-weight: normal !important;
        margin: 0;
        line-height: 1.2;
    }}

    /* 🤖 로봇 옆 다짐 말풍선 스타일 */
    .hand-drawn-goal {{
        font-family: 'kkukkkuk' !important;
        font-weight: normal !important;
        position: relative; 
        background: #FFFFFF; 
        border: 3px solid #4E342E;
        padding: 15px 25px; 
        font-size: 1.2rem; 
        color: #4E342E !important;
        border-radius: 255px 15px 225px 15px/15px 225px 15px 255px;
        box-shadow: 3px 3px 0px #4E342E;
        margin-left: 20px;
    }}

    .hand-drawn-goal::before {{
        content: '';
        position: absolute;
        left: -18px;
        top: 50%;
        transform: translateY(-50%);
        border-width: 10px 18px 10px 0;
        border-style: solid;
        border-color: transparent #4E342E transparent transparent;
    }}

    .hand-drawn-goal::after {{
        content: '';
        position: absolute;
        left: -14px;
        top: 50%;
        transform: translateY(-50%);
        border-width: 8px 15px 8px 0;
        border-style: solid;
        border-color: transparent #FFFFFF transparent transparent;
    }}

    .stApp {{ background-color: #FFFDE7; }}
    [data-testid="stSidebar"] {{ background-color: #FFEBEE; }}
    
    /* ⚪ 입력 박스 설정 */
    div[data-baseweb="select"] > div,
    div[data-baseweb="textarea"] > div,
    div[data-baseweb="input"] > div,
    input, textarea {{
        background-color: #FFFFFF !important;
        border: 1.5px solid #D2B48C !important; /* 얇은 실선 테두리 적용 */
        border-radius: 8px !important;
    }}

    hr {{
        border: none !important;
        border-top: 3px dashed #F8BBD0 !important; 
        background-color: transparent !important;
        height: 0px !important;
        margin: 25px 0 !important;
    }}

    div.stButton > button {{
        background-color: #F8BBD0 !important;
        color: #4E342E !important;
        border: 2px solid #F48FB1 !important;
        border-radius: 10px !important;
        font-family: 'kkukkkuk' !important;
        font-weight: 400 !important;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
    }}

    div.stButton > button:hover {{
        background-color: #DB7093 !important;
        color: #FFFFFF !important;
        transform: scale(1.1) rotate(5deg) !important;
        border-color: #C71585 !important;
    }}
    
    div.stButton > button:hover * {{
        color: #FFFFFF !important;
    }}

    .title-container {{ 
        display: flex; 
        align-items: center; 
        justify-content: center; 
        gap: 0px; 
    }}
    
    .goal-section {{ display: flex; align-items: center; justify-content: center; gap: 10px; margin: 20px 0; }}
    
    .hand-drawn-bubble {{
        position: relative; padding: 30px; margin-top: 30px; 
        font-size: 1.35rem !important;
        text-align: center; border: 3px solid; border-radius: 255px 15px 225px 15px/15px 225px 15px 255px;
        display: block; width: 100%; box-shadow: 3px 3px 0px rgba(0,0,0,0.1);
        font-family: 'kkukkkuk' !important;
    }}
    .hand-drawn-bubble::before {{
        content: ''; position: absolute; top: -20px; left: 50%; transform: translateX(-50%);
        border-width: 0 15px 20px 15px; border-style: solid; border-color: inherit;
        border-left-color: transparent; border-right-color: transparent;
    }}
    .hand-drawn-bubble::after {{
        content: ''; position: absolute; top: -14px; left: 50%; transform: translateX(-50%);
        border-width: 0 12px 17px 12px; border-style: solid;
        border-left-color: transparent; border-right-color: transparent;
    }}

    .mood-high {{ background-color: #FFEBEE; color: #4E342E !important; border-color: #FFCDD2; }}
    .mood-high::after {{ border-bottom-color: #FFEBEE !important; }}
    .mood-mid {{ background-color: #FFF3E0; color: #4E342E !important; border-color: #FFE0B2; }}
    .mood-mid::after {{ border-bottom-color: #FFF3E0 !important; }}
    .mood-low {{ background-color: #ECEFF1; color: #4E342E !important; border-color: #CFD8DC; }}
    .mood-low::after {{ border-bottom-color: #ECEFF1 !important; }}

    /* ✨ 뉴스 카드 Soft Mint Teal 스타일 */
    .news-card {{
        background-color: #CADEDF !important;
        border: 2px solid #A8C4C5 !important;
        border-radius: 15px;
        padding: 15px;
        height: 100%;
        transition: transform 0.2s, background-color 0.2s;
        text-decoration: none !important;
        display: block;
    }}
    .news-card:hover {{
        transform: translateY(-5px);
        background-color: #B8D3D4 !important;
        box-shadow: 0 4px 15px rgba(168, 196, 197, 0.5);
        border-color: #8EB2B3 !important;
    }}
    .news-title {{
        font-size: 1.1rem;
        font-weight: bold;
        margin-bottom: 8px;
        color: #2D4344 !important;
    }}
    .news-source {{
        font-size: 0.85rem;
        color: #537172 !important;
    }}

    .font-label-large {{
        font-size: 1.3rem !important;
        margin-bottom: 10px;
    }}
    
    /* 💛 폰트 체험 존 결과창 스타일 수정 */
    .font-test-area-dahyun {{
        background-color: #FFF9C4 !important; 
        border: 3px dashed #FBC02D !important; /* ✨ 점선 테두리 적용 */
        border-radius: 15px;
        padding: 20px;
        font-size: 2.2rem;
        text-align: center;
        min-height: 100px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-top: 10px;
        font-family: 'dahyun' !important;
    }}

    [data-testid="stMetricValue"] {{
        text-align: center !important;
        display: flex;
        justify-content: center;
    }}
    [data-testid="stMetricLabel"] {{
        display: flex;
        justify-content: center;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

def load_lottieurl(url):
    try: r = requests.get(url); return r.json() if r.status_code == 200 else None
    except: return None

def get_weather(city_name, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric&lang=kr"
    try:
        response = requests.get(url).json()
        if response.get("cod") == 200:
            return {"temp": response["main"]["temp"], "desc": response["weather"][0]["description"], "icon": response["weather"][0]["icon"], "humidity": response["main"]["humidity"]}
        return None
    except: return None

# 📰 뉴스 가져오기 함수 (키워드: AI, AX, 인공지능)
def get_ai_news():
    rss_url = "https://news.google.com/rss/search?q=AI+OR+AX+OR+인공지능&hl=ko&gl=KR&ceid=KR:ko"
    feed = feedparser.parse(rss_url)
    return feed.entries[:2]

with st.sidebar:
    st.subheader("📍 오늘의 날씨")
    city = st.selectbox("도시 선택", ["Seoul", "Busan", "Incheon", "Daegu", "Daejeon", "Gwangju", "Jeju"])
    if OPENWEATHER_API_KEY:
        weather_data = get_weather(city, OPENWEATHER_API_KEY)
        if weather_data:
            w_code = weather_data['icon'][:2]
            emoji_map = {"01": "☀️", "02": "⛅", "03": "☁️", "04": "☁️", "09": "🌧️", "10": "🌦️", "11": "🌩️", "13": "❄️", "50": "🌫️"}
            st.markdown(f"<div style='font-size: 60px; text-align: center; padding: 10px 10px 0px 10px;'>{emoji_map.get(w_code, '✨')}</div>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align:center; font-size: 1.2rem; margin-top: -10px;'>현재 날씨: {weather_data['desc']}</p>", unsafe_allow_html=True)
            col_w1, col_w2 = st.columns(2)
            col_w1.metric("기온", f"{weather_data['temp']}°C")
            col_w2.metric("습도", f"{weather_data['humidity']}%")
    st.markdown("---")
    st.subheader("✏️ 오늘의 다짐")
    today_goal_input = st.text_area("", placeholder="오늘의 다짐을 입력하세요! 🔥", label_visibility="collapsed")   
    if st.button("다짐 저장"): st.toast("다짐이 저장되었습니다! ✨")

jampong_data = get_local_file_as_base64(JAMPONG_IMAGE_PATH)
jampong_html = f'<img src="data:image/png;base64,{jampong_data}" width="100">' if jampong_data else ""

st.markdown(
    f"""
    <div class="title-container">
        <div>{jampong_html}</div>
        <h1 class="custom-title"> AX 마스터 짬뽕 대시보드</h1>
        <div style="margin-left: -20px;">{jampong_html}</div>
    </div>
    """, 
    unsafe_allow_html=True
)

if today_goal_input:
    st.markdown(f'<div class="goal-section"><div>{robot_img_html}</div><div class="hand-drawn-goal">“{today_goal_input}”</div></div>', unsafe_allow_html=True)

st.markdown("---")

patrick_data = get_local_file_as_base64(PATRICK_GIF_PATH)
patrick_html = f'<img src="data:image/gif;base64,{patrick_data}" style="position: absolute; top: 20px; right: 0px; width: 120px; z-index: 10;">' if patrick_data else ""

st.markdown(f'<div style="position: relative;">{patrick_html}', unsafe_allow_html=True)
st.header("🍴 점심 뭐 먹지?")
col1, col2 = st.columns(2)
cheap_menu = ["맥도날드", "치킨랩", "가득드림", "컵라면", "샌드위치", "노브랜드", "쿠차라"]
expensive_menu = ["아오내순대국", "북창동순두부", "김치찜", "부대찌개", "라멘", "초밥", "돈까스", "마라탕", "쌀국수"]
with col1:
    st.subheader("💸 만 원 이하 점메추")
    p1 = st.empty(); p1.markdown('<div class="menu-box sky-blue-box" style="padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 10px; background-color: #E3F2FD; color: #4E342E !important; border: 2px dashed #BBDEFB; font-size: 1.5rem;">메뉴를 뽑아보세요!</div>', unsafe_allow_html=True)
    if st.button("가성비 메뉴 뽑기 🎰"):
        for _ in range(8):
            p1.markdown(f'<div class="menu-box sky-blue-box" style="padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 10px; background-color: #E3F2FD; color: #4E342E !important; border: 2px dashed #BBDEFB; font-size: 1.5rem;">{random.choice(cheap_menu)}</div>', unsafe_allow_html=True)
            time.sleep(0.1)
        p1.markdown(f'<div class="menu-box sky-blue-box" style="padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 10px; background-color: #E3F2FD; color: #4E342E !important; border: 2px dashed #BBDEFB; font-size: 1.5rem;">✨ {random.choice(cheap_menu)} ✨</div>', unsafe_allow_html=True)
        st.balloons()
with col2:
    st.subheader("🤑 만 원 이상 점메추")
    p2 = st.empty(); p2.markdown('<div class="menu-box light-green-box" style="padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 10px; background-color: #E8F5E9; color: #4E342E !important; border: 2px dashed #C8E6C9; font-size: 1.5rem;">메뉴를 뽑아보세요!</div>', unsafe_allow_html=True)
    if st.button("메뉴 뽑기 🎰"):
        for _ in range(8):
            p2.markdown(f'<div class="menu-box light-green-box" style="padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 10px; background-color: #E8F5E9; color: #4E342E !important; border: 2px dashed #C8E6C9; font-size: 1.5rem;">{random.choice(expensive_menu)}</div>', unsafe_allow_html=True)
            time.sleep(0.1)
        p2.markdown(f'<div class="menu-box light-green-box" style="padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 10px; background-color: #E8F5E9; color: #4E342E !important; border: 2px dashed #C8E6C9; font-size: 1.5rem;">✨ {random.choice(expensive_menu)} ✨</div>', unsafe_allow_html=True)
        st.balloons()
st.markdown('</div>', unsafe_allow_html=True) 

st.markdown("---")

st.header("🤔 현재 기분 점수")
st.markdown('<p style="font-size: 1.25rem; margin-bottom: 30px;">지금 기분이 어떠신가요?</p>', unsafe_allow_html=True)
score = st.slider("", 0, 100, 50, key="mood_slider", label_visibility="collapsed")

if score >= 80: lottie_url, status_msg, mood_class = "https://assets9.lottiefiles.com/packages/lf20_u4j3tAz98v.json", "최고예요! 이 기세를 몰아 오늘을 즐기세요! 🕺💃", "mood-high"
elif score >= 40: lottie_url, status_msg, mood_class = "https://assets5.lottiefiles.com/packages/lf20_tivunBeS8t.json", "평온한 하루네요. 무난한 게 가장 좋은 법이죠. 🙂‍↕️", "mood-mid"
else: lottie_url, status_msg, mood_class = "https://assets1.lottiefiles.com/packages/lf20_0y69z6.json", "조금 지치셨나요? 맛있는 거 먹고 일찍 쉬는 걸 추천해요. 🛌", "mood-low"

lottie_json = load_lottieurl(lottie_url)
if lottie_json: st_lottie(lottie_json, height=250, key="mood_ani")
st.markdown(f'<div class="hand-drawn-bubble {mood_class}">{status_msg}</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# ✨ 실시간 AI 관련 뉴스 섹션
# ---------------------------------------------------------
st.markdown("---")
st.header("📰 실시간 AI 관련 핫이슈")
news_list = get_ai_news()
col_n1, col_n2 = st.columns(2)

for i, news in enumerate(news_list):
    with [col_n1, col_n2][i]:
        st.markdown(f"""
            <a href="{news.link}" target="_blank" class="news-card">
                <div class="news-title">{news.title}</div>
                <div class="news-source">출처: {news.source.get('title', 'Google News')}</div>
            </a>
        """, unsafe_allow_html=True)

st.markdown("---")
st.header("✍️ 눈누에서 찾은 귀여운 고양이 폰트... 써보실래요?")
st.markdown('<p class="font-label-large">¢, £, †, ♤ 를 입력하면 귀여운 고양이를 만날 수 있어요! 🐈‍⬛</p>', unsafe_allow_html=True)
test_text = st.text_input("체험 텍스트 입력", placeholder="여기에 입력해보세요.", key="font_tester", label_visibility="collapsed")

if test_text:
    st.markdown(f'<div class="font-test-area-dahyun">{test_text}</div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="font-test-area-dahyun">글자를 입력하면 이곳에 나타납니다!</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("© 2026 AX Master | 퍼스널 대시보드")