from flask import Flask
import requests
from bs4 import BeautifulSoup
from flapp.models import db, migrate, Keyword


app = Flask(__name__) 

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SECRET_KEY'] = '_5#y2L"F4Q8z\n\xec]/'

with app.app_context(): 
    db.init_app(app) 
    migrate.init_app(app, db)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)


BASE_URL = 'https://www.chloeting.com/program/'

#프로그램 리스트 가져오기
page_p = requests.get(BASE_URL)
soup_p = BeautifulSoup(page_p.content, 'html.parser')

title_p = soup_p.find('div', class_='programs-list').find_all('a')

programs = []
for link in title_p:
    programs.append(link.get('href'))

pro = []
for i in range(len(programs)):
  p = programs[i].split('.')[0].split('/')[1].upper()
  pro.append(p)

type_k = soup_p.find_all('div', class_='detail')
type_k[0].find('p', class_='more-details')

k_type = []
for div in type_k:
  text = div.find('p', class_='more-details').text
  t = text.split(':')[1].split(',')
  k_type.append(t)


q_list = Keyword.query.filter(Keyword.index).all()
if len(q_list) == 0 :
    index = 1
else :
    index = len(q_list) + 1


for i in range(21):
  keyword_t = Keyword(index=i, pro=pro[i], k_word1=k_type[i][0], k_word2=k_type[i][1], k_word3=k_type[i][2])
  db.session.add(keyword_t)
  db.session.commit()