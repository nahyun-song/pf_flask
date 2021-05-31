from flask import Flask, render_template, redirect, url_for, request
from flapp.routes.main_route import bp as main_bp
from flapp.models import db, migrate
import requests
from bs4 import BeautifulSoup

app = Flask(__name__) 
app.register_blueprint(main_bp)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

with app.app_context(): 
    db.init_app(app) 
    migrate.init_app(app, db)



@app.route('/') 
def signin():
    return render_template('signin.html')

@app.route('/main') 
def main():
    return render_template('main.html')

@app.route('/signin_done', methods=['POST']) 
def signin_done():
    userid = request.form['userid']
    email = request.form['email']
    pwd = request.form['pwd']

    return redirect(url_for('main'))

@app.route('/login') 
def login():
    return render_template('login.html')

@app.route('/login_done') 
def login_done():
    pass


@app.route('/list') 
def index():

    BASE_URL = 'https://www.chloeting.com/program/'

    #프로그램 리스트 가져오기
    page_p = requests.get(BASE_URL)
    soup_p = BeautifulSoup(page_p.content, 'html.parser')

    title_p = soup_p.find('div', class_='programs-list').find_all('a')

    programs = []
    for link in title_p:
        programs.append(link.get('href'))

    return render_template('list.html', programs=programs, BASE_URL=BASE_URL)



@app.route('/schedule') 
def schedule():
    BASE_URL = 'https://www.chloeting.com/program/'

    #프로그램 리스트 가져오기
    page_p = requests.get(BASE_URL)
    soup_p = BeautifulSoup(page_p.content, 'html.parser')

    title_p = soup_p.find('div', class_='programs-list').find_all('a')

    programs = []
    for link in title_p:
        programs.append(link.get('href'))

    return render_template('schedule.html', programs=programs)

@app.route('/food') 
def food():
    return render_template('food.html')


#어플리케이션 실행하기
if __name__ == '__main__':
    app.run(debug=True)