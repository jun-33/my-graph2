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
#    트리맵 — 장르 안에서 어떤 영화가 컸나
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
    "각 장르별 어떤 영화가 많은 관객을 모았는지 한눈에 비교할 수 있다."
)


# ============================================================
# 7. 세 번째 그래프
#    히스토그램 — 영화 대부분은 관객이 몇 명쯤인가
# ============================================================

st.header("📊 그래프 3. 영화별 총 관객 분포")

# 총 관객 데이터가 있는 영화만 사용
hist_df = df[
    ["movieNm", "total_audi"]
].dropna(subset=["movieNm", "total_audi"]).copy()

hist_df = hist_df[hist_df["total_audi"] >= 0]


# 히스토그램
fig3 = px.histogram(
    hist_df,
    x="total_audi",
    nbins=20,
    title="영화별 총 관객 분포",
    labels={
        "total_audi": "총 관객 수",
        "count": "영화 편수"
    }
)

fig3.update_traces(
    hovertemplate=(
        "총 관객 구간: %{x}<br>"
        "영화 편수: %{y}편"
        "<extra></extra>"
    )
)

fig3.update_layout(
    xaxis_title="총 관객 수",
    yaxis_title="영화 편수",
    margin=dict(t=60, b=20, l=20, r=20)
)

st.plotly_chart(fig3, use_container_width=True)


# ============================================================
# 8. 그래프 3 설명
# ============================================================

st.subheader("💡 이 그래프로 알 수 있는 것")

st.info(
    "이 그래프로 알 수 있는 것: "
    "영화별 총 관객 분표를 알 수 있다. 가장 많은 관객 수를 기록한 영화는 왕과 사는 남자이다."
)


# ============================================================
# 9. 네 번째 그래프
#    산점도 — 스크린을 많이 받은 영화가 관객도 많나
# ============================================================

st.header("📊 그래프 4. 개봉일 스크린 수와 총 관객의 관계")

scatter_df = df[
    ["movieNm", "genre", "first_scrn", "total_audi"]
].dropna(
    subset=["movieNm", "genre", "first_scrn", "total_audi"]
).copy()

# 의미 있는 양수 데이터만 사용
scatter_df = scatter_df[
    (scatter_df["first_scrn"] > 0) &
    (scatter_df["total_audi"] >= 0)
]


fig4 = px.scatter(
    scatter_df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    hover_data={
        "genre": True,
        "first_scrn": ":,.0f",
        "total_audi": ":,.0f"
    },
    title="개봉일 스크린 수와 총 관객의 관계",
    labels={
        "first_scrn": "개봉일 스크린 수",
        "total_audi": "총 관객 수",
        "genre": "장르"
    }
)

fig4.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "장르: %{customdata[0]}<br>"
        "개봉일 스크린 수: %{x:,.0f}개<br>"
        "총 관객: %{y:,.0f}명"
        "<extra></extra>"
    )
)
fig4.update_layout(
    xaxis_title="개봉일 스크린 수",
    yaxis_title="총 관객 수",
    margin=dict(t=60, b=20, l=20, r=20)
)

st.plotly_chart(fig4, use_container_width=True)


# ============================================================
# 10. 그래프 4 설명
# ============================================================

st.subheader("💡 이 그래프로 알 수 있는 것")

st.info(
    "이 그래프로 알 수 있는 것: "
    "영화의 개봉일 스크린 수와 총 관객의 관객 수가 어떤 관계를 보이는지 장르별로 비교 할 수 있따."
)


# ============================================================
# 11. 다섯 번째 그래프
#     박스플롯 — 장르별 관객 분포는 어떻게 다른가
# ============================================================

st.header("📊 그래프 5. 장르별 총 관객 분포")

box_df = df[
    ["genre", "movieNm", "total_audi"]
].dropna(
    subset=["genre", "movieNm", "total_audi"]
).copy()

# 총 관객이 0 이상인 데이터만 사용
box_df = box_df[box_df["total_audi"] >= 0]


# 장르별 영화 수 계산
genre_movie_count = box_df["genre"].value_counts()

# 영화가 10편 이상인 장르만 선택
valid_genres = genre_movie_count[
    genre_movie_count >= 10
].index

box_df = box_df[
    box_df["genre"].isin(valid_genres)
]


# 박스플롯
fig5 = px.box(
    box_df,
    x="genre",
    y="total_audi",
    color="genre",
    points="outliers",
    hover_name="movieNm",
    hover_data={
        "genre": False,
        "movieNm": True,
        "total_audi": ":,.0f"
    },
    title="영화가 10편 이상인 장르의 총 관객 분포",
    labels={
        "genre": "장르",
        "total_audi": "총 관객 수"
    }
)

fig5.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "총 관객: %{y:,.0f}명"
        "<extra></extra>"
    )
)

fig5.update_layout(
    xaxis_title="장르",
    yaxis_title="총 관객 수",
    showlegend=False,
    margin=dict(t=60, b=20, l=20, r=20)
)

st.plotly_chart(fig5, use_container_width=True)


# ============================================================
# 12. 그래프 5 설명
# ============================================================

st.subheader("💡 이 그래프로 알 수 있는 것")

st.info(
    "이 그래프로 알 수 있는 것: "
    "어떤 장르의 영화 관객 수가 많은 지 비교할 수 있다."
)
# ============================================================
# 그래프 6. 버블 — 첫 주 관객까지 넣으면 무엇이 더 보이나
# ============================================================

st.header("📊 그래프 6. 개봉일 스크린 수와 총 관객의 관계 - 버블 그래프")

bubble_df = df[
    ["movieNm", "genre", "first_scrn", "first_week_audi", "total_audi"]
].dropna(
    subset=["movieNm", "genre", "first_scrn", "first_week_audi", "total_audi"]
).copy()

bubble_df = bubble_df[
    (bubble_df["first_scrn"] > 0) &
    (bubble_df["first_week_audi"] > 0) &
    (bubble_df["total_audi"] >= 0)
]

fig6 = px.scatter(
    bubble_df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    size="first_week_audi",
    size_max=45,
    hover_name="movieNm",
    custom_data=["genre", "first_week_audi"],
    title="개봉일 스크린 수와 총 관객의 관계 - 첫 주 관객을 버블 크기로 표시",
    labels={
        "first_scrn": "개봉일 스크린 수",
        "total_audi": "총 관객 수",
        "first_week_audi": "첫 주 관객 수",
        "genre": "장르"
    }
)

fig6.update_traces(
    marker=dict(
        opacity=0.7,
        line=dict(width=1)
    ),
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "장르: %{customdata[0]}<br>"
        "개봉일 스크린 수: %{x:,.0f}개<br>"
        "첫 주 관객 수: %{customdata[1]:,.0f}명<br>"
        "총 관객 수: %{y:,.0f}명"
        "<extra></extra>"
    )
)

fig6.update_layout(
    xaxis_title="개봉일 스크린 수",
    yaxis_title="총 관객 수",
    margin=dict(t=60, b=20, l=20, r=20)
)

st.plotly_chart(fig6, use_container_width=True)

st.subheader("💡 이 그래프로 알 수 있는 것")
st.info(
    "이 그래프로 알 수 있는 것: "
    "개봉일 스크린 수와 총 관계 수의 관계를 알 수 있다."
)
# ============================================================
# 그래프 7. 선버스트 — 국가에서 장르로 내려가면
# ============================================================

st.header("📊 그래프 7. 제작 국가와 장르별 영화 분포")

sunburst_df = df[
    ["nation", "genre", "movieNm"]
].dropna(
    subset=["nation", "genre", "movieNm"]
).copy()

# 제작 국가가 여러 개 적혀 있는 경우 첫 번째 국가만 사용
sunburst_df["nation"] = (
    sunburst_df["nation"]
    .astype(str)
    .str.split("|")
    .str[0]
    .str.strip()
)

# 장르가 여러 개 적혀 있는 경우 첫 번째 장르만 사용
sunburst_df["genre"] = (
    sunburst_df["genre"]
    .astype(str)
    .str.split("|")
    .str[0]
    .str.strip()
)

# 빈 값 제거
sunburst_df = sunburst_df[
    (sunburst_df["nation"] != "") &
    (sunburst_df["genre"] != "")
]

# 국가 → 장르별 영화 편수 계산
sunburst_count = (
    sunburst_df
    .groupby(["nation", "genre"])
    .size()
    .reset_index(name="영화 편수")
)

fig7 = px.sunburst(
    sunburst_count,
    path=["nation", "genre"],
    values="영화 편수",
    title="제작 국가 → 장르별 영화 편수",
)

fig7.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "영화 편수: %{value}편"
        "<extra></extra>"
    )
)

fig7.update_layout(
    margin=dict(t=60, b=20, l=20, r=20)
)

st.plotly_chart(fig7, use_container_width=True)

st.subheader("💡 이 그래프로 알 수 있는 것")
st.info(
    "이 그래프로 알 수 있는 것: "
    "어떤 나라에서 어떤 장르의 영화를 많이 제작했는가를 알 수 있다."
)
# ============================================================
# 그래프 8. 박스오피스 TOP 10에 머문 일수 분포
# ============================================================

st.header("📊 그래프 8. 박스오피스 TOP 10에 머문 일수 분포")

top10_df = df[
    ["movieNm", "days_in_top10"]
].dropna(
    subset=["movieNm", "days_in_top10"]
).copy()

top10_df = top10_df[
    top10_df["days_in_top10"] >= 0
]

fig8 = px.histogram(
    top10_df,
    x="days_in_top10",
    nbins=20,
    title="영화별 박스오피스 TOP 10 유지 일수 분포",
    labels={
        "days_in_top10": "TOP 10에 머문 일수",
        "count": "영화 편수"
    }
)

fig8.update_traces(
    hovertemplate=(
        "TOP 10 유지 일수: %{x}일<br>"
        "영화 편수: %{y}편"
        "<extra></extra>"
    )
)

fig8.update_layout(
    xaxis_title="TOP 10에 머문 일수",
    yaxis_title="영화 편수",
    margin=dict(t=60, b=20, l=20, r=20)
)

st.plotly_chart(fig8, use_container_width=True)

st.subheader("💡 이 그래프로 알 수 있는 것")
st.info(
    "이 그래프로 알 수 있는 것: "
    "영화들이 얼마나 Top 10을 유지했는가를 알 수 있다"
)
