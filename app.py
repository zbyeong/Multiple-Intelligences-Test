import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="다중지능/적성 검사",
    page_icon="📝",
    layout="centered"
)

# 2. 문항 데이터 정의 (40개 문항)
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

    # 자연 친화 (6문항)
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

# 3. UI 구성 및 검사 진행
st.title("📊 영역별 적성/지능 검사")
st.write("각 문항을 읽고 자신과 가장 잘 부합하는 정도를 선택해 주세요.")
st.divider()

# 폼 생성
with st.form("survey_form"):
    answers = {}
    
    # 문항 출력
    for idx, q in enumerate(QUESTIONS, start=1):
        st.markdown(f"**Q{idx}. [{q['category']}]** {q['text']}")
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

    # 영역별 점수 계산 (평균 점수 계산)
    category_scores = {}
    category_counts = {}

    for q in QUESTIONS:
        cat = q["category"]
        score = answers[q["id"]]
        category_scores[cat] = category_scores.get(cat, 0) + score
        category_counts[cat] = category_counts.get(cat, 0) + 1

    # 영역별 평균 점수 데이터프레임 생성
    avg_scores = {cat: round(category_scores[cat] / category_counts[cat], 2) for cat in category_scores}
    df_results = pd.DataFrame(list(avg_scores.items()), columns=["영역", "평균점수 (5점 만점)"])

    # 강점 영역 확인
    max_score = df_results["평균점수 (5점 만점)"].max()
    top_categories = df_results[df_results["평균점수 (5점 만점)"] == max_score]["영역"].tolist()

    st.subheader(f"💡 나의 가장 우수한 영역: **{', '.join(top_categories)}**")
    st.write(f"해당 영역의 평균 점수는 **{max_score}점**입니다.")

    # 방사형 차트 (Radar Chart) 시각화
    fig = px.line_polar(
        df_results, 
        r="평균점수 (5점 만점)", 
        theta="영역", 
        line_close=True,
        range_r=[0, 5],
        title="영역별 점수 프로필"
    )
    fig.update_traces(fill='toself')
    st.plotly_chart(fig, use_container_width=True)

    # 막대 그래프 시각화
    fig_bar = px.bar(
        df_results,
        x="영역",
        y="평균점수 (5점 만점)",
        color="영역",
        text="평균점수 (5점 만점)",
        title="영역별 평균 점수 비교"
    )
    fig_bar.update_yaxes(range=[0, 5])
    st.plotly_chart(fig_bar, use_container_width=True)

    # 상세 데이터 표
    st.subheader("📋 영역별 상세 점수")
    st.dataframe(df_results, use_container_width=True)
