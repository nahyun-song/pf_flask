from flask import Flask, render_template, redirect, url_for, request, session, flash
from flapp.routes.main_route import bp as main_bp
from flapp.models import db, migrate, User, Keyword
import requests
from bs4 import BeautifulSoup

app = Flask(__name__) 
app.register_blueprint(main_bp)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SECRET_KEY'] = '_5#y2L"F4Q8z\n\xec]/'

with app.app_context(): 
    db.init_app(app) 
    migrate.init_app(app, db)



@app.route('/') 
def signin():
   if session.get('logged_in'):
        resp_user = User.query.filter_by(userid=session.get('userid')).all()
        print('return user test')
        return render_template('signin.html', userid=resp_user, isLogin=True)

   print('Dummy Context!')
   return render_template('signin.html')

    
@app.route('/main') 
def main():
    BASE_URL = 'https://www.chloeting.com/program/'

    #프로그램 리스트 가져오기
    page_p = requests.get(BASE_URL)
    soup_p = BeautifulSoup(page_p.content, 'html.parser')

    title_p = soup_p.find('div', class_='programs-list').find_all('a')

    programs = []
    for link in title_p:
        programs.append(link.get('href'))

    return render_template('main.html', BASE_URL=BASE_URL, programs=programs)

@app.route('/signin_done', methods=['POST']) 
def signin_done():
    if request.form['userid']:
        userid = request.form['userid']
        email = request.form['email']
        pwd = request.form['pwd']

        user = User(userid=userid, email=email, pwd=pwd)
        db.session.add(user)
        db.session.commit()

    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
   return render_template('login.html')


@app.route('/login_done', methods=['POST']) 
def login_done():
   if request.method == 'POST':
       userid = request.form['userid']
       pwd = request.form['pwd']
       resp = User.query.filter_by(userid=userid, pwd=pwd).first()

       if resp is not None:
            session.clear()
            session['user_id'] = resp.userid
            session['logged_in'] = True
            print(session) #SecureCookieSession
            return redirect(url_for('keyword'))
       else:
           error = 'Incorrect ID or Password!'
           flash(error)

   return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('signin'))


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

    
@app.route('/keyword') 
def keyword():
    q_list = Keyword.query.filter(Keyword.index).all()

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



    if len(q_list) == 0 :
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
            if len(k_type[i])==3:
                keyword_t = Keyword(index=i+1, pro=pro[i], k_word1=k_type[i][0], k_word2=k_type[i][1], k_word3=k_type[i][2])
                db.session.add(keyword_t)
                db.session.commit()
            else:
                keyword_t = Keyword(index=i+1, pro=pro[i], k_word1=k_type[i][0], k_word2=k_type[i][1], k_word3=None)
                db.session.add(keyword_t)
                db.session.commit()
        return redirect(url_for('main'))
        
    else:
        return redirect(url_for('main'))



#어플리케이션 실행하기
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
