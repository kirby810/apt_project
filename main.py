import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from streamlit_option_menu import option_menu
plt.rcParams['font.family'] ='Malgun Gothic'



df = pd.read_csv("전국아파트분양가격.csv", encoding="cp949")
df.rename(columns={"분양가격(제곱미터)": "분양가격"}, inplace=True)   # 열 이름 변경
df['분양가격'] = df['분양가격'].replace('', float('NaN')) #분양가격 비어있으면 NaN으로 대체
df = df.drop('규모구분', axis=1) # 규모구분행 삭제

#공백 문자열을 정규 표현식 r'^\s*$'으로 찾고 np.NaN으로 NaN값 삽입 regex=True는 Pandas의 데이터프레임에서 문자열을 처리할 때 정규 표현식을 사용할 것임을 나타냄
df['분양가격'] = df['분양가격'].replace(r'^\s*$', np.NaN, regex=True)


df.dropna(subset=['분양가격'], inplace=True)# NaN 값이 포함된 행 삭제
df['분양가격'] = pd.to_numeric(df['분양가격'])



def filter_by_region(df, region):     #지역별로 분류해주는 함수
    filtered_df = df[df['지역명'] == region]
    return filtered_df




regions = ['서울', '인천', '경기', '부산', '대구', '광주', '대전', '울산', '세종', '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주']
region_dfs = {region: filter_by_region(df, region) for region in regions}

# 각 지역별 분양가격 평균 계산
average_prices = {region: region_df['분양가격'].mean() for region, region_df in region_dfs.items()}

plt.figure(figsize=(10, 6))
plt.bar(average_prices.keys(), average_prices.values(), color='skyblue')
plt.xlabel('지역명')
plt.ylabel('평균 분양가격(제곱미터)')
plt.title('지역별 평균 분양가격')
plt.xticks(rotation=45)
plt.show()





























# def home_page():
#     st.write("Welcome to the Home Page!")

# def projects_page():
#     st.write("Here are our Projects!")

# def contact_page():
#     st.write("Contact us!")

# def main():
#     selected_page = st.sidebar.selectbox("MENU", ["Home", "Projects", "Contact"])
    
#     if selected_page == "Home":
#         home_page()
#     elif selected_page == "Projects":
#         projects_page()
#     elif selected_page == "Contact":
#         contact_page()

# if __name__ == "__main__":
#     main()
