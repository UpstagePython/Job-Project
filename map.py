import streamlit as st
import pandas as pd
import json
import requests
import pydeck as pdk
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Geocoding API를 통해 주소를 위도, 경도로 변환하는 함수
def geocode(address):
    api_key = 'AIzaSyBCXE0NK4nVfUMjqmHmpb2LjegoviWznR4'  # Google Maps API 키
    base_url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}'
    response = requests.get(base_url)
    data = response.json()
    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        return location['lat'], location['lng']
    else:
        return None, None

# JSON 파일에서 채용 정보 데이터를 읽어오는 함수
def load_jobs_from_json(json_filename):
    with open(json_filename, 'r', encoding='utf-8') as file:
        jobs = json.load(file)
    return jobs

# 분석할 데이터의 키워드 및 스트림릿 셀렉트 박스로 제작
keyword = st.selectbox('키워드를 선택하세요', ['app', 'web', 'dba', 'server', 'machine', 'front', 'hard', 'publisher'])

# JSON 파일 이름
json_filename = f'CrawlingData/data/json/{keyword}_merge.json'

# JSON 파일에서 채용 정보 데이터를 읽어오기
jobs = load_jobs_from_json(json_filename)

# 데이터프레임을 위한 리스트
map_data_list = []

# 각 채용 정보의 지역을 위도, 경도로 변환
for job in jobs:
    lat, lon = geocode(job['address'])
    if lat is not None and lon is not None:
        map_data_list.append({
            'lat': lat,
            'lon': lon,
            'title': job['title'],
            'company': job['company'],
            'tooltip': job['company']
        })

# 데이터프레임 생성
map_data = pd.DataFrame(map_data_list)

# pydeck 레이어 설정
layer = pdk.Layer(
    'ScatterplotLayer',
    data=map_data,
    get_position=['lon', 'lat'],
    get_color=[255, 0, 0],  # 마커 색상은 빨간색으로 설정
    get_radius=150,  # 마커의 반경
    pickable=True,
    tooltip=True
)

# pydeck 뷰포트 설정
view_state = pdk.ViewState(
    latitude=map_data['lat'].mean(),
    longitude=map_data['lon'].mean(),
    zoom=10
)

# pydeck 맵 생성
r = pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v10',
    initial_view_state=view_state,
    layers=[layer],
    tooltip={"text": "{tooltip}"}
)

# 스트림릿을 통해 pydeck 맵 표시
st.pydeck_chart(r)

# 워드 클라우드 생성을 위한 채용 제목 문자열 결합
title_text = ' '.join(job['title'] for job in jobs)

# 한글 폰트 경로를 지정하여 워드 클라우드 생성
font_path = '/Library/Fonts/AppleGothic.ttf'
wordcloud = WordCloud(
    font_path=font_path,  # 한글 폰트 경로 지정
    width=800,
    height=400,
    background_color='white'
).generate(title_text)

# 워드 클라우드 시각화
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
st.pyplot(plt)