
import pandas as pd
import random
import streamlit as st

st.title("로또 번호 전략 분석기")
st.markdown("✅ 고정수 / 제외수 기반 조합 추천기")

# 데이터 업로드
uploaded_file = st.file_uploader("CSV 파일 업로드", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # 최근 회차 선택
    recent_n = st.slider("최근 분석할 회차 수", min_value=10, max_value=100, value=50)
    recent_df = df.tail(recent_n)

    # 빈도 기반 고정수 추천
    freq_numbers = recent_df.iloc[:, 1:7].values.flatten()
    freq_series = pd.Series(freq_numbers).value_counts().sort_index()
    top_fixed = freq_series.head(4).index.tolist()

    st.write(f"🎯 최근 {recent_n}회 기준 고정수 추천: {top_fixed}")

    # 사용자 고정수/제외수 선택
    fixed = st.multiselect("고정수", list(range(1, 46)), default=top_fixed)
    exclude = st.multiselect("제외수", list(range(1, 46)), default=[])

    # 조합 수 설정
    combo_count = st.number_input("조합 개수", min_value=1, max_value=30, value=10)

    # 조합 생성
    def generate_lotto(fixed_numbers=[], exclude_numbers=[], count=6):
        nums = set(fixed_numbers)
        pool = set(range(1, 46)) - set(fixed_numbers) - set(exclude_numbers)
        while len(nums) < count:
            nums.add(random.choice(list(pool)))
        return sorted(nums)

    def generate_multiple(n, fixed, exclude):
        return [generate_lotto(fixed, exclude) for _ in range(n)]

    if st.button("조합 생성"):
        results = generate_multiple(combo_count, fixed, exclude)
        for i, combo in enumerate(results, 1):
            st.write(f"#{i}: {combo}")
