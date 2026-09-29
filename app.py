import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="적성/지능 검사",
    page_icon="📝",
    layout="centered"
)

# 2. 문항 데이터 정의 (40개 문항 - 영역명 비공개)
QUESTIONS = [
    # 언어 (5문항)
    {"id": 2, "category": "언어", "text": "나는 읽고, 말하고, 쓰기 전에 이미 머릿속에는 어떤 낱말들이 들린다."},
    {"id": 3, "category": "언어", "text": "나는 TV나 영화보다는 라디오나 팟캐스트 같은 음성매체를 통해서 많은 정보를 얻는다."},
    {"id": 5, "category": "언어", "text": "나는 혼자서나 아니면 다른 사람과 함께 발음하기 어려운 어구(tongue twister), 무의미한 각운(nonsense rhymes), 혹은 동음이의어 등 언어게임을 즐긴다."},
    {"id": 6, "category": "언어", "text": "다른 사람들은 종종 내가 말하고 글을 쓸 때 사용하는 단어의 뜻을 설명해 달라고 요청한다."},
    {"id": 10, "category": "언어", "text": "나는 최근에 다른 사람들로부터 인정을 받거나 혹은 내가 자랑으로 여기고 있는 것들을 글로 써 왔다."},

    # 논리 수학 (5문항)
    {"id": 12, "category": "논리 수학", "text": "수학과 과학은 학교 다닐 때 내가 좋아하던 과목 중의 하나였다."},
    {"id": 13, "category": "논리 수학", "text": "나는 논리적 사고를 필요로 하는 게임과 수수께끼를 좋아한다."},
    {"id": 14, "category": "논리 수학", "text": "나는 과학의 새로운 진보에 관심이 있다."},
    {"id": 15, "category": "논리 수학", "text": "나는 어떤 조건 하에서 무슨 일이 발생할지에 관심이 있고 이를 밝히는 실험과 증명하기를 좋아한다."},
    {"id": 16, "category": "논리 수학", "text": "나는 사물 속에서 질서, 논리적 계열 및 유형(pattern)을 찾고자 한다."},

    # 공간 (5문항)
    {"id": 21, "category": "공간", "text": "나는 눈을 감았을 때 종종 생생한 시각적 영상을 본다."},
    {"id": 22, "category": "공간", "text": "나는 색깔에 민감하다."},
    {"id": 23, "category": "공간", "text": "나는 종종 내 주위에서 본 것을 기록하기 위해 카메라를 사용한다."},
    {"id": 25, "category": "공간", "text": "나는 생동감 있는 꿈을 꾼다."},
    {"id": 27, "category": "공간", "text": "나는 그림을 그리거나 낙서하는 것을 좋아한다."},

    # 신체 운동 (4문항)
    {"id": 31, "category": "신체 운동", "text": "나는 스포츠나 신체적 활동에 참여하는 것을 좋아한다."},
    {"id": 34, "category": "신체 운동", "text": "나는 걸으나, 조깅을 하든지 혹은 다른 종류의 신체적 활동을 할 때 가장 좋은 생각이 떠오르곤 한다."},
    {"id": 38, "category": "신체 운동", "text": "나는 몸을 격렬하게 움직이는 스포츠나, 그와 유사한 박진감 넘치는 신체적 체험을 좋아한다."},
    {"id": 39, "category": "신체 운동", "text": "나는 내 몸의 균형을 잘 맞출 수 있다고 생각한다."},

    # 음악 (5문항)
    {"id": 42, "category": "음악", "text": "나는 음정이 맞지 않을 때 그것을 쉽게 알아차릴 수 있다."},
    {"id": 47, "category": "음악", "text": "나는 간단한 타악기로 쉽게 박자를 맞출 수 있다."},
    {"id": 48, "category": "음악", "text": "나는 다양한 노래나 악곡의 선율을 알고 있다."},
    {"id": 49, "category": "음악", "text": "나는 음악을 한두 번 들으면 그것을 거의 정확하게 따라 부를 수 있다."},
    {"id": 50, "category": "음악", "text": "나는 공부할 때, 혹은 새로운 것을 학습하는 동안 장단을 맞추거나 멜로디에 맞추어 노래를 부른다."},

    # 대인 관계 (5문항)
    {"id": 54, "category": "대인 관계", "text": "나는 나의 일(직장/학교), 종교단체, 또는 지역사회와 연결된 사회적 활동에 참여하는 것을 좋아한다."},
    {"id": 55, "category": "대인 관계", "text": "나는 혼자 하는 놀이보다 여럿이서 함께하는 놀이를 더 좋아한다."},
    {"id": 57, "category": "대인 관계", "text": "나는 어떤 상황에서든 리더로서의 역할을 하고 있다는 것을 발견한다."},
    {"id": 58, "category": "대인 관계", "text": "나는 많은 사람들과 함께 있을 때 편안하다."},
    {"id": 59, "category": "대인 관계", "text": "나는 밤에 집에서 혼자 지내기보다는 생동감이 넘치는 파티에서 시간 보내기를 좋아한다."},

    # 개인 이해 (5문항)
    {"id": 63, "category": "개인 이해", "text": "나는 좌절하지 않고 실패에 대처할 수 있다."},
    {"id": 64, "category": "개인 이해", "text": "나는 나에게 알맞은 특별한 취미와 관심이 있다."},
    {"id": 65, "category": "개인 이해", "text": "나는 항상 잊지 않고 다짐하는 중요한 인생목표를 가지고 있다."},
    {"id": 66, "category": "개인 이해", "text": "나는 나의 장점과 단점을 잘 알고 있다."},
    {"id": 68, "category": "개인 이해", "text": "나는 나 자신을 의지가 강하고, 독립적으로 생활할 수 있는 사람이라고 생각한다."},

    # 자연 친화 (5문항)
    {"id": 72, "category": "자연 친화", "text": "나는 숲이나 산속을 걸어갈 때 동물의 발자국이나 새들의 둥지 등에 관심을 갖고, 또한 날씨 신호를 구분할 수 있다."},
    {"id": 73, "category": "자연 친화", "text": "나는 천문학, 우주의 탄생, 생명의 진화 등에 대해 관심이 많다."},
    {"id": 74, "category": "자연 친화", "text": "나는 여러 종류의 나무, 꽃, 식물 등을 구분할 수 있고 이름을 잘 기억한다."},
    {"id": 76, "category": "자연 친화", "text": "나는 식물에 직접 물을 주고 잘 가꾼다."},
    {"id": 77, "category": "자연 친화", "text": "나는 세계적인 주요 환경 문제에 대한 이해와 관심을 가지고 있다."},
]

OPTIONS = {
    1: "전혀 그렇지 않다",
    2: "그렇지 않다",
    3: "보통이다",
    4: "그렇다",
    5: "매우 그렇다"
}

# 개별 영역 기본 추천
CATEGORY_INFO = {
    "언어": {"jobs": "작가, 기자, 번역가, 방송기획자", "majors": "국어국문학, 언론정보학, 문예창작학"},
    "논리 수학": {"jobs": "데이터 분석가, 회계사, 프로그래머", "majors": "통계학, 컴퓨터공학, 수학"},
    "공간": {"jobs": "디자이너, 건축가, 영상 편집자", "majors": "산업디자인, 건축학, 영상학"},
    "신체 운동": {"jobs": "운동선수, 물리치료사, 스포츠 트레이너", "majors": "체육학, 물리치료학, 무용학"},
    "음악": {"jobs": "작곡가, 연주가, 음향 엔지니어", "majors": "실용음악학, 작곡과, 음향공학"},
    "대인 관계": {"jobs": "상담사, 마케터, 교사, HR 전문가", "majors": "심리학, 경영학, 교육학"},
    "개인 이해": {"jobs": "라이프 코치, 인문학 연구원, 창업가", "majors": "철학, 자율전공, 심리학"},
    "자연 친화": {"jobs": "환경운동가, 수의사, 기상학자", "majors": "환경공학, 수의학, 생물학"}
}

# 1~2순위 주요 지능 조합 추천 DB
COMBINATION_INFO = {
    frozenset(["언어", "대인 관계"]): {
        "jobs": "변호사, 아나운서/기자, PR/홍보 전문가, 외교관, 커뮤니케이션 디렉터, 세일즈 리더",
        "majors": "미디어커뮤니케이션학, 언론정보학, 법학, 정치외교학, 경영학(마케팅)"
    },
    frozenset(["언어", "논리 수학"]): {
        "jobs": "기술 전문 작가(Technical Writer), 데이터 분석 기자, 특허변리사, 학술 연구원, 경제 에디터",
        "majors": "문헌정보학, 경제학, 기술경영학, 과학커뮤니케이션"
    },
    frozenset(["언어", "공간"]): {
        "jobs": "웹툰 스토리작가, 영화 감독/시나리오 작가, 광고 카피라이터, 전시 기획자, 퍼블리싱 디자이너",
        "majors": "시각디자인학, 문예창작학과, 연극영화학과, 미디어콘텐츠학"
    },
    frozenset(["언어", "개인 이해"]): {
        "jobs": "소설가/시인, 자서전 에디터, 철학 칼럼니스트, 심리 에세이 작가, 독립출판 기획자",
        "majors": "국어국문학, 철학과, 심리학과, 문예창작학과"
    },
    frozenset(["언어", "자연 친화"]): {
        "jobs": "환경/생태 전문 기자, 다큐멘터리 작가, 자연과학 저술가, 환경 정책 대변인",
        "majors": "환경학, 언론정보학, 생물학, 커뮤니케이션학"
    },
    frozenset(["논리 수학", "공간"]): {
        "jobs": "데이터 사이언티스트, 건축가, 게임 시스템 개발자, AI/SW 엔지니어, UX/UI 디자이너, 로봇 공학자",
        "majors": "컴퓨터공학과, 건축학과, 데이터사이언스학과, 산업디자인학과, 로봇공학과"
    },
    frozenset(["논리 수학", "대인 관계"]): {
        "jobs": "경영 컨설턴트, 금융 분석가(Analyst), HR 데이터 분석가, 프로젝트 매니저(PM), 마케팅 전략가",
        "majors": "경영학과, 경제학과, 산업공학과, 통계학과"
    },
    frozenset(["논리 수학", "자연 친화"]): {
        "jobs": "환경과학자, 생명공학 연구원, 천문기상학자, 스마트농업 기술 연구원, 바이오 데이터 분석가",
        "majors": "생명공학과, 환경공학과, 천문기상학과, 바이오시스템공학"
    },
    frozenset(["공간", "신체 운동"]): {
        "jobs": "무대/스포츠 연출가, 외과의사, 재활치료사, 안무가, 정교한 제품 시공 전문가, 스턴트 감독",
        "majors": "무용학과, 물리치료학과, 의예과(외과/정형외과), 체육학과"
    },
    frozenset(["공간", "음악"]): {
        "jobs": "무대 디자이너, 뮤직비디오 감독, 미디어 아티스트, 게임 사운드/비주얼 디렉터, 공간 음향 디자이너",
        "majors": "미디어아트학과, 공간디자인학과, 예술경영학과, 실용음악학"
    },
    frozenset(["대인 관계", "개인 이해"]): {
        "jobs": "임상심리학자, 정신건강의학과 의사, 라이프/비즈니스 코치, 조직문화 컨설턴트, 사회복지 전문가",
        "majors": "심리학과, 사회복지학과, 의예과(정신건강의학), 교육학과"
    },
    frozenset(["대인 관계", "신체 운동"]): {
        "jobs": "스포츠 에이전트, 체육 교사, 레크리에이션 지도자, 팀 스포츠 감독, 그룹 피트니스 리더",
        "majors": "체육교육과, 스포츠비즈니스학과, 사회체육학과"
    },
    frozenset(["음악", "언어"]): {
        "jobs": "작사가, 싱어송라이터, 음향 PD, 음악 평론가, 뮤지컬 연출가",
        "majors": "실용음악과, 작곡과, 예술경영학과, 국문학/영문학"
    },
    frozenset(["음악", "대인 관계"]): {
        "jobs": "음악치료사, 합창단/오케스트라 지휘자, 음악 교육가, 공연 기획자, 예술 행정가",
        "majors": "음악치료학과, 음악교육과, 예술경영학과"
    },
    frozenset(["음악", "개인 이해"]): {
        "jobs": "독립 작곡가, 사운드 디자이너, 정서 치료 음악가, 음악 연구원",
        "majors": "작곡과, 음악치료학, 예술학"
    },
    frozenset(["신체 운동", "자연 친화"]): {
        "jobs": "야생동물 연구원, 산악 구조대원, 친환경 농업가, 생태 가이드, 원예치료사",
        "majors": "산림자원학, 농애생명과학, 체육학, 원예학과"
    }
}

# 3. UI 구성 및 검사 진행
st.title("📊 적성/지능 검사")
st.write("각 문항을 읽고 자신과 가장 잘 부합하는 정도를 선택해 주세요.")
st.divider()

# 폼 생성
with st.form("survey_form"):
    answers = {}
    
    # 문항 출력 (영역명 제외)
    for idx, q in enumerate(QUESTIONS, start=1):
        st.markdown(f"**Q{idx}. {q['text']}**")
        answers[q["id"]] = st.radio(
            label=f"Q{idx} 답변 선택",
            options=list(OPTIONS.keys()),
            format_func=lambda x: f"{x}점 - {OPTIONS[x]}",
            horizontal=True,
            key=f"q_{q['id']}",
            label_visibility="collapsed"
        )
        st.write("")
        
    submitted = st.form_submit_button("제출 및 결과 보기", use_container_width=True)

# 4. 제출 시 결과 산출
if submitted:
    st.divider()
    st.header("🎯 검사 결과 분석")

    # 영역별 단순 합계 점수 계산
    raw_scores = {}
    for q in QUESTIONS:
        cat = q["category"]
        score = answers[q["id"]]
        raw_scores[cat] = raw_scores.get(cat, 0) + score

    # 25점 만점으로 점수 환산
    converted_scores = {}
    for cat, score in raw_scores.items():
        if cat == "신체 운동":
            converted_scores[cat] = round(score * 1.25, 1)  # 20점 만점 -> 25점 만점
        else:
            converted_scores[cat] = round(score * 1.0, 1)   # 25점 만점 유지

    # 점수 기준 정렬
    sorted_scores = sorted(converted_scores.items(), key=lambda x: x[1], reverse=True)
    
    # 1순위, 2순위 지능 추출
    rank1_score = sorted_scores[0][1]
    rank1_cats = [item[0] for item in sorted_scores if item[1] == rank1_score]
    
    # 2순위 산출
    remaining_scores = [item for item in sorted_scores if item[1] < rank1_score]
    if remaining_scores:
        rank2_score = remaining_scores[0][1]
        rank2_cats = [item[0] for item in remaining_scores if item[1] == rank2_score]
    else:
        rank2_score = None
        rank2_cats = []

    # 데이터프레임 생성
    df_results = pd.DataFrame(list(converted_scores.items()), columns=["영역", "환산 점수 (25점 만점)"])

    # 🏆 1~2순위 주요 결과 요약 안내
    st.subheader("💡 주요 강점 지능 분석")
    st.write(f"- **1순위 강점 지능:** **{', '.join(rank1_cats)}** ({rank1_score}점)")
    if rank2_cats:
        st.write(f"- **2순위 강점 지능:** **{', '.join(rank2_cats)}** ({rank2_score}점)")

    # 🚀 추천 진로 / 전공 제안 세션
    st.markdown("---")
    st.subheader("🚀 1~2순위 조합 기반 추천 직업 및 전공")

    # 1, 2순위 조합 키 생성
    combo_key = None
    if len(rank1_cats) >= 2:
        combo_key = frozenset([rank1_cats[0], rank1_cats[1]])
        cat1_name, cat2_name = rank1_cats[0], rank1_cats[1]
    elif len(rank1_cats) == 1 and rank2_cats:
        combo_key = frozenset([rank1_cats[0], rank2_cats[0]])
        cat1_name, cat2_name = rank1_cats[0], rank2_cats[0]

    # 1) 미리 정의된 융합 조합 정보가 존재하는 경우
    if combo_key and combo_key in COMBINATION_INFO:
        rec_data = COMBINATION_INFO[combo_key]
        st.success(f"✨ **[{cat1_name} + {cat2_name}]** 강점 시너지 맞춤 추천")
        st.markdown(f"- **💼 조합 추천 직업:** {rec_data['jobs']}")
        st.markdown(f"- **🎓 조합 추천 전공:** {rec_data['majors']}")

    # 2) DB에 없는 기타 조합일 경우 각 영역의 개별 직업/전공을 조합하여 표시
    elif combo_key:
        job1 = CATEGORY_INFO[cat1_name]['jobs']
        job2 = CATEGORY_INFO[cat2_name]['jobs']
        major1 = CATEGORY_INFO[cat1_name]['majors']
        major2 = CATEGORY_INFO[cat2_name]['majors']
        
        st.success(f"✨ **[{cat1_name} + {cat2_name}]** 강점 융합 추천")
        st.markdown(f"- **💼 조합 추천 직업:** {job1}, {job2} 분야의 융합/전문 분야")
        st.markdown(f"- **🎓 조합 추천 전공:** {major1}, {major2} 관련 학과 및 융합 전공")

    st.markdown("---")

    # 시각화 그래프 영역
    col1, col2 = st.columns(2)
    
    with col1:
        # 방사형 차트 (Radar Chart)
        fig_radar = px.line_polar(
            df_results, 
            r="환산 점수 (25점 만점)", 
            theta="영역", 
            line_close=True,
            range_r=[0, 25],
            title="영역별 점수 프로필"
        )
        fig_radar.update_traces(fill='toself')
        st.plotly_chart(fig_radar, use_container_width=True)

    with col2:
        # 막대 그래프
        fig_bar = px.bar(
            df_results,
            x="영역",
            y="환산 점수 (25점 만점)",
            color="영역",
            text="환산 점수 (25점 만점)",
            title="영역별 환산 점수 비교"
        )
        fig_bar.update_yaxes(range=[0, 25])
        st.plotly_chart(fig_bar, use_container_width=True)

    # 상세 데이터 표
    st.subheader("📋 영역별 상세 점수")
    st.dataframe(df_results, use_container_width=True)
