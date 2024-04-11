import streamlit as st
import pandas as pd
import json
import requests

# Geocoding API를 통해 주소를 위도, 경도로 변환하는 함수
def geocode(address):
    api_key = 'API_KEYS'  # Google Maps API 키
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

# JSON 파일 이름
json_filename = 'Crawling/job_data.json'

# JSON 파일에서 채용 정보 데이터를 읽어오기
jobs = load_jobs_from_json(json_filename)

# 데이터프레임을 위한 리스트
map_data_list = []

# 각 채용 정보의 지역을 위도, 경도로 변환
for job in jobs:
    lat, lon = geocode(job['region'])
    if lat is not None and lon is not None:
        map_data_list.append({'lat': lat, 'lon': lon, 'title': job['title'], 'company': job['company']})

# 데이터프레임 생성
map_data = pd.DataFrame(map_data_list)

# 스트림릿을 사용하여 지도를 표시
st.subheader('Map of Data')
st.map(map_data)