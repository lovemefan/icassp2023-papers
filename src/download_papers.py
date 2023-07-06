# -*- coding:utf-8 -*-
# @FileName  :download_papers.py
# @Time      :2023/7/6 09:55
# @Author    :lovemefan
# @Email     :lovemefan@outlook.com
import os.path
import re

import requests
import json
from tqdm import tqdm
TOC_URL = 'https://ieeexplore.ieee.org/rest/search/pub/10094559/issue/10094560/toc'


def generate_paper_list(page_nun):
    meta_data = []
    papers_data = []
    for i in tqdm(range(page_nun)):
        meta, papers = get_papers_cite(i)

        meta_data.extend(meta)
        papers_data.extend(papers)

    with open('../metadata/meta_info.json', 'w', encoding='utf-8') as file:
        json.dump(meta_data, file, indent=4)

    with open('../metadata/papers.json', 'w', encoding='utf-8') as file:
        json.dump(papers_data, file, indent=4)


def download_paper(id: str, title):
    if os.path.exists(f'../papers/{title}.pdf'):
        print(f"../papers/{title}.pdf is exist")
    else:

        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0'}
        pdf_url = f"https://ieeexplore.ieee.org/ielx7/10094559/10094560/{id}.pdf"
        print(f"pfd download url: {pdf_url}")
        response = requests.get(pdf_url, timeout=80, headers=headers)
        if response.status_code != 200:
            raise ValueError(response.text)
        with open(f'../papers/{title}.pdf', 'wb') as pdf:
            pdf.write(response.content)
        print(f"Download: {title}")


def get_papers_cite(page: int):
    data = {
        "isnumber": "10094560",
        "sortType": "vol-only-seq",
        "rowsPerPage": "100",
        "pageNumber": f"{page}",
        "punumber": "10094559"
    }
    headers = {
        "Origin": "https://ieeexplore.ieee.org"
    }
    response = requests.post(TOC_URL, headers=headers, json=data)
    result = json.loads(response.text)
    papers_list = []
    for item in tqdm(result['records']):
        paper_info = dict()
        paper_info['title'] = item['articleTitle'].replace('/', ' or ')
        paper_info['doi'] = item['doi']
        paper_info['pdfLink'] = f"https://ieeexplore.ieee.org{item['pdfLink']}"
        print(paper_info)
        papers_list.append(paper_info)
        download_paper(paper_info['doi'][-8:], paper_info['title'])

    return result['records'], papers_list


if __name__ == '__main__':
    generate_paper_list(28)