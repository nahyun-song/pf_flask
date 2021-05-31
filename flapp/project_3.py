import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://www.chloeting.com/program/'

#프로그램 리스트 가져오기
page_p = requests.get(BASE_URL)
soup_p = BeautifulSoup(page_p.content, 'html.parser')

title_p = soup_p.find('div', class_='programs-list').find_all('a')

programs = []
for link in title_p:
  programs.append(link.get('href'))

breakpoint()

#프로그램별 스케줄 가져오기

url = BASE_URL + programs[0]
page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')

elm = soup.find_all('div', class_='info')

day_list = []

for e in elm:
  day_list.append(e.text.strip().split('\n'))

dict_list = []
for i in range(len(day_list)):
  dict_list.append({'day':day_list[i][0], 'time':day_list[i][3].strip()})

print(programs)