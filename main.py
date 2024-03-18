import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
from streamlit_folium import folium_static
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




def plot_average_prices(df, graph_type):
    regions = ['서울', '인천', '경기', '부산', '대구', '광주', '대전', '울산', '세종', '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주']
    region_dfs = {region: filter_by_region(df, region) for region in regions}
    average_prices = {region: region_df['분양가격'].mean() for region, region_df in region_dfs.items()}

    plt.figure(figsize=(10, 6))
    
    if graph_type == "막대그래프":
        plt.bar(average_prices.keys(), average_prices.values(), color='red')
        plt.title('지역별 평균 분양가격')
    elif graph_type == "선그래프":
        plt.plot(average_prices.keys(), average_prices.values(), marker='o', color='blue', linestyle='-')
        plt.title('지역별 평균 분양가격')
    
    plt.xlabel('지역명')
    plt.ylabel('평균 분양가격(제곱미터)')
    plt.xticks(rotation=45)
    return plt

def plot_average_prices_by_year(df, graph_type):
    years = df['연도'].unique()  
    average_prices_by_year = {}  

    for year in years:
        year_df = df[df['연도'] == year]
        average_prices_by_year[year] = year_df['분양가격'].mean()

    plt.figure(figsize=(10, 6))
    
    if graph_type == "막대그래프":
        plt.bar(list(average_prices_by_year.keys()), list(average_prices_by_year.values()), color='red')
        plt.title('연도별 평균 분양가격')
    elif graph_type == "선그래프":
        plt.plot(list(average_prices_by_year.keys()), list(average_prices_by_year.values()), marker='o', color='blue', linestyle='-')
        plt.title('연도별 평균 분양가격')
    
    plt.xlabel('연도')
    plt.ylabel('평균 분양가격(제곱미터)')
    plt.xticks(rotation=45)
    return plt


#지도
def plot_map(df):
    # 지역별 평균 분양가격 
    average_prices = df.groupby('지역명')['분양가격'].mean().to_dict()

    # 지역별 위도와 경도 
    locations = {
        '서울': [37.5665, 126.9780],
        '인천': [37.4563, 126.7052],
        '경기': [37.4138, 127.5183],
        '부산': [35.1796, 129.0756],
        '대구': [35.8714, 128.6014],
        '광주': [35.1595, 126.8526],
        '대전': [36.3504, 127.3845],
        '울산': [35.5384, 129.3114],
        '세종': [36.4803, 127.2892],
        '강원': [37.8228, 128.1555],
        '충북': [36.8001, 127.6645],
        '충남': [36.5184, 126.8000],
        '전북': [35.7175, 127.1530],
        '전남': [34.8679, 126.9910],
        '경북': [36.5760, 128.5055],
        '경남': [35.4606, 128.2132],
        '제주': [33.4996, 126.5312]
    }
    m = folium.Map(location=[36.5, 127.5], zoom_start=7)

    # 각 지역에 마커 추가
    for region, location in locations.items():
        avg_price = average_prices.get(region, '정보 없음')
        popup_text = f"{region}: {avg_price:.2f}원/㎡" 
        folium.Marker(location=location, popup=popup_text).add_to(m)

    return m



#streamlit 페이지

with st.sidebar:
    selected = option_menu(
        menu_title="Menu",
        options=["지역별 아파트 가격", "연도별 아파트 가격", "지도"],
        icons=["house", "envelope", "map"],
        menu_icon="kr",
        default_index=0,
    )
    if selected in ["지역별 아파트 가격", "연도별 아파트 가격"]:
        graph_type = st.radio("그래프 종류", ["막대그래프", "선그래프"])

st.title("한국 아파트 가격 현황")

if selected == "지역별 아파트 가격":
    plt = plot_average_prices(df, graph_type)
    st.pyplot(plt)
elif selected == "연도별 아파트 가격":
    plt = plot_average_prices_by_year(df, graph_type)
    st.pyplot(plt)
elif selected == "지도":
    folium_map = plot_map(df)
    folium_static(folium_map)











