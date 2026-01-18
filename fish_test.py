import streamlit as st

# 1. 만점 및 결과 데이터 설정
fish_results = {
    "ISTJ": {"name": "코리도라스", "desc": "성실하고 책임감 있는 바닥의 청소부! 정해진 규칙을 지키는 것을 좋아해요."},
    "ISFJ": {"name": "팬더 가라루파", "desc": "주변을 배려하는 다정하고 온순한 평화주의자. 타인의 감정에 민감해요."},
    "INFJ": {"name": "디스커스", "desc": "생각이 깊고 신비로운 아우라를 지닌 존재. 혼자만의 시간이 중요해요."},
    "INTJ": {"name": "블랙 고스트", "desc": "독립적이고 분석적인 밤의 전략가. 효율성을 가장 중시합니다."},
    "ISTP": {"name": "글라스 캣피쉬", "desc": "과묵하지만 효율을 중시하는 실용주의자. 관찰력이 뛰어납니다."},
    "ISFP": {"name": "네온 테트라", "desc": "예술적 감각이 있고 조화로운 삶을 꿈꾸는 이. 온순하고 따뜻해요."},
    "INFP": {"name": "베타", "desc": "나만의 세계가 뚜렷한 낭만적인 몽상가. 감수성이 풍부합니다."},
    "INTP": {"name": "인디언 복어", "desc": "호기심 많고 엉뚱한 천재적인 탐구자. 논리적인 분석을 즐겨요."},
    "ESTP": {"name": "실버 아로와나", "desc": "자신감이 넘치고 모험을 즐기는 승부사. 행동파 스타일!"},
    "ESFP": {"name": "플래티", "desc": "어디서나 적응력 갑! 에너지가 넘치는 분위기 메이커입니다."},
    "ENFP": {"name": "구피", "desc": "호기심 천국, 사람을 좋아하는 러블리 인싸. 긍정 에너지가 넘쳐요."},
    "ENTP": {"name": "엔젤피쉬", "desc": "토론을 즐기고 아이디어가 샘솟는 재치꾼. 변화를 두려워하지 않아요."},
    "ESTJ": {"name": "프론토사", "desc": "질서를 중시하고 조직을 이끄는 카리스마 리더. 계획이 명확합니다."},
    "ESFJ": {"name": "몰리", "desc": "리액션 부자, 타인의 행복에서 기쁨을 찾는 다정한 성격이에요."},
    "ENFJ": {"name": "골든 엘리엇", "desc": "정의롭고 따뜻하며 모두를 포용하는 영향력 있는 멘토입니다."},
    "ENTJ": {"name": "레드 테일 샤크", "desc": "목표를 향해 거침없이 전진하는 추진력 대장. 결단력이 핵심!"}
}

questions = [
    {"q": "주말에 갑자기 친구가 나오라고 한다면?", "a": "좋아! 지금 나갈게! (E)", "b": "음.. 오늘은 집에서 쉬고 싶은데.. (I)", "type": "EI"},
    {"q": "여러 명이 모인 회식이나 파티에서 나는?", "a": "분위기를 주도하며 대화를 이끈다 (E)", "b": "주로 듣는 편이며 친한 사람과만 말한다 (I)", "type": "EI"},
    {"q": "에너지를 충전하는 방법은?", "a": "사람들을 만나고 활동하기 (E)", "b": "혼자 조용히 취미 생활 즐기기 (I)", "type": "EI"},
    {"q": "새로운 요리 레시피를 배울 때 나는?", "a": "정해진 용량과 순서를 정확히 지킨다 (S)", "b": "감으로 대충 넣으며 내 방식대로 만든다 (N)", "type": "SN"},
    {"q": "멍 때릴 때 나는 보통 무슨 생각을 할까?", "a": "정말 아무 생각도 안 한다 (S)", "b": "갑자기 좀비가 나타나는 등의 상상을 한다 (N)", "type": "SN"},
    {"q": "노래를 들을 때 내가 더 중요하게 생각하는 건?", "a": "귀에 착 감기는 멜로디와 박자 (S)", "b": "마음을 울리는 가사와 의미 (N)", "type": "SN"},
    {"q": "친구가 '나 너무 우울해서 쇼핑했어'라고 한다면?", "a": "뭐 샀어? 쇼핑하니까 좀 나아? (T)", "b": "무슨 일 있었어? 많이 힘들었구나.. (F)", "type": "TF"},
    {"q": "고민을 털어놓는 친구에게 나는?", "a": "현실적인 해결책을 제시해 준다 (T)", "b": "진심으로 공감하고 위로해 준다 (F)", "type": "TF"},
    {"q": "더 기분 좋은 칭찬은?", "a": "너 진짜 똑똑하다, 일 잘한다 (T)", "b": "너 진짜 따뜻한 사람이다, 고마워 (F)", "type": "TF"},
    {"q": "여행을 가기로 했을 때 나는?", "a": "시간 단위로 상세 계획을 짠다 (J)", "b": "목적지만 정하고 발길 닿는 대로 간다 (P)", "type": "JP"},
    {"q": "과제를 하거나 일을 할 때 스타일은?", "a": "미리 계획해서 여유 있게 끝낸다 (J)", "b": "마감 직전 벼락치기로 끝낸다 (P)", "type": "JP"},
    {"q": "책상이나 방 안의 상태는?", "a": "항상 정해진 위치에 물건이 있다 (J)", "b": "어질러진 것 같지만 나름의 규칙이 있다 (P)", "type": "JP"}
]

# 2. 페이지 스타일 설정
st.set_page_config(page_title="열대어 MBTI 테스트", page_icon="🐠")

# 연한 노랑 배경색 적용 (CSS)
st.markdown("""
    <style>
    .stApp {
        background-color: #FFFDE7;
    }
    .main-title {
        font-size: 3rem;
        font-weight: bold;
        color: #FFA000;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 세션 상태 초기화
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'answers' not in st.session_state:
    st.session_state.answers = []
if 'q_idx' not in st.session_state:
    st.session_state.q_idx = 0
if 'scores' not in st.session_state:
    st.session_state.scores = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}

# 4. 앱 로직
# --- 메인 화면 ---
if st.session_state.page == 'home':
    st.markdown('<p class="main-title">🐠 열대어 MBTI 테스트</p>', unsafe_allow_html=True)
    st.write("<div style='text-align: center;'>나의 성격은 어떤 열대어와 닮았을까요?</div>", unsafe_allow_html=True)
    st.write("")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("테스트 시작하기", use_container_width=True):
            st.session_state.page = 'test'
            st.rerun()

# --- 테스트 화면 ---
elif st.session_state.page == 'test':
    progress = (st.session_state.q_idx) / len(questions)
    st.progress(progress)
    st.write(f"질문 {st.session_state.q_idx + 1} / {len(questions)}")
    
    current_q = questions[st.session_state.q_idx]
    st.subheader(current_q['q'])
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button(current_q['a'], use_container_width=True, key=f"btn_a_{st.session_state.q_idx}"):
            type_char = current_q['type'][0] # E, S, T, J
            st.session_state.scores[type_char] += 1
            st.session_state.q_idx += 1
            if st.session_state.q_idx >= len(questions):
                st.session_state.page = 'result'
            st.rerun()
            
    with col2:
        if st.button(current_q['b'], use_container_width=True, key=f"btn_b_{st.session_state.q_idx}"):
            type_char = current_q['type'][1] # I, N, F, P
            st.session_state.scores[type_char] += 1
            st.session_state.q_idx += 1
            if st.session_state.q_idx >= len(questions):
                st.session_state.page = 'result'
            st.rerun()

# --- 결과 화면 ---
elif st.session_state.page == 'result':
    st.markdown('<p class="main-title">결과 확인 중...</p>', unsafe_allow_html=True)
    
    # 결과 계산
    res = ""
    res += "E" if st.session_state.scores["E"] >= st.session_state.scores["I"] else "I"
    res += "S" if st.session_state.scores["S"] >= st.session_state.scores["N"] else "N"
    res += "T" if st.session_state.scores["T"] >= st.session_state.scores["F"] else "F"
    res += "J" if st.session_state.scores["J"] >= st.session_state.scores["P"] else "P"
    
    final_fish = fish_results[res]
    
    st.balloons()
    st.success("테스트 완료!")
    st.markdown(f"<h2 style='text-align: center;'>당신은 '{final_fish['name']}' 타입!</h2>", unsafe_allow_html=True)
    st.write(f"<p style='text-align: center; font-size: 1.2rem;'>{final_fish['desc']}</p>", unsafe_allow_html=True)
    
    if st.button("다시 하기"):
        st.session_state.page = 'home'
        st.session_state.q_idx = 0
        st.session_state.scores = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
        st.rerun()