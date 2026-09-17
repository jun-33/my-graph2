import streamlit as st
import pandas as pd
import plotly.express as px

# ============================================================
# 1. 페이지 설정
# ============================================================

st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.write("1년간 박스오피스 10위권에 든 영화들의 분포와 관계를 살펴봅니다.")


# ============================================================
# 2. 데이터 불러오기
# ============================================================

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 개봉일: 여덟 자리 숫자를 날짜 형식으로 변환
    df["openDt"] = pd.to_datetime(
        df["openDt"].astype(str),
        format="%Y%m%d",
        errors="coerce"
    )

    # 장르: 여러 장르가 | 로 구분되어 있다면 첫 번째 장르만 사용
    df["genre"] = (
        df["genre"]
        .fillna("미상")
        .astype(str)
        .str.split("|")
        .str[0]
        .str.strip()
    )

    # 숫자형 데이터 변환
    numeric_columns = [
        "first_scrn",
        "first_show",
        "first_week_audi",
        "total_audi",
        "days_in_top10"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    return df


df = load_data()


# ============================================================
# 3. 첫 번째 그래프
#    장르별 영화 편수 - 도넛 그래프
# ============================================================

st.header("📊 그래프 1. 장르별 영화 편수")

# 장르별 영화 수 계산
genre_count = (
    df["genre"]
    .value_counts()
    .reset_index()
)

genre_count.columns = ["장르", "영화 편수"]


# 도넛 그래프
fig = px.pie(
    genre_count,
    names="장르",
    values="영화 편수",
    hole=0.45,
    title="장르별 영화 편수"
)

# 마우스를 올렸을 때 편수와 비율 표시
fig.update_traces(
    textinfo="percent",
    hovertemplate=(
        "<b>%{label}</b><br>"
        "영화 편수: %{value}편<br>"
        "비율: %{percent}<extra></extra>"
    )
)

fig.update_layout(
    legend_title="장르",
    margin=dict(t=60, b=20, l=20, r=20)
)

st.plotly_chart(fig, use_container_width=True)


# ============================================================
# 4. 그래프 설명
# ============================================================

st.subheader("💡 이 그래프로 알 수 있는 것")

st.info(
    "이 그래프로 알 수 있는 것: "
    "어떤 영화의 장르의 편수가 많은 지 알 수 있다."
)




# ============================================================
# 5. 두 번째 그래프
#    장르 안의 영화 - 트리맵
# ============================================================

st.header("📊 그래프 2. 장르별 영화의 총 관객 분포")

# 트리맵에 사용할 데이터
treemap_df = df[
    ["genre", "movieNm", "total_audi"]
].dropna(subset=["genre", "movieNm", "total_audi"]).copy()

# 총 관객이 0 이하인 데이터 제외
treemap_df = treemap_df[treemap_df["total_audi"] > 0]


fig2 = px.treemap(
    treemap_df,
    path=["genre", "movieNm"],
    values="total_audi",
    title="장르별 영화와 총 관객"
)

# 마우스를 올렸을 때 영화명과 총 관객 표시
fig2.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "총 관객: %{value:,.0f}명"
        "<extra></extra>"
    )
)

fig2.update_layout(
    margin=dict(t=60, b=20, l=20, r=20)
)

st.plotly_chart(fig2, use_container_width=True)


# ============================================================
# 6. 그래프 2 설명
# ============================================================

st.subheader("💡 이 그래프로 알 수 있는 것")

st.info(
    "이 그래프로 알 수 있는 것: "
    "각 장르 안에서 어떤 영화가 많은 관객을 모았는지 총 관객 규모를 비교할 수 있습니다."
)


# ============================================================
# 앞으로 추가할 그래프
# ============================================================

# 그래프 3
# st.header("📊 그래프 3. ...")


# 그래프 4
# st.header("📊 그래프 4. ...")


# 그래프 5
# st.header("📊 그래프 5. ...")
