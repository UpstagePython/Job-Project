import json
import os

def merge_json_files(file_paths, output_path):
    # 합친 데이터를 저장할 빈 리스트
    merged_data = []

    # 각 파일 경로에 대해
    for file_path in file_paths:
        # JSON 파일을 열고 읽기
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            # 불러온 데이터를 합친 데이터에 추가
            merged_data.append(data)
    
    # 합친 데이터를 하나의 JSON 파일로 저장
    with open(output_path, 'w', encoding='utf-8') as output_file:
        json.dump(merged_data, output_file, ensure_ascii=False, indent=4)

# 직무 유형 목록
job_types = ['app', 'dba', 'front', 'hard', 'machine', 'publisher', 'server', 'web']

# 각 직무 유형에 대해
for job_type in job_types:
    # 각 직무 유형에 따른 파일 경로 설정
    file_paths = [
        f'CrawlingData/wanted/json/{job_type}_wanted.json',
        f'CrawlingData/saramin/json/{job_type}_saramin.json',
        f'CrawlingData/jobkorea/json/{job_type}_job.json'
    ]
    
    # 합친 JSON 파일을 저장할 경로 설정
    output_path = f'{job_type}_merge.json'
    
    # 해당 직무 유형의 JSON 파일을 합치고 저장
    merge_json_files(file_paths, output_path)