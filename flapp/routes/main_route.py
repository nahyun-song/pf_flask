from flask import Flask, Blueprint, session, request, redirect, render_template, url_for
import requests
from bs4 import BeautifulSoup
from werkzeug.utils import redirect
from flapp.models import db, User, Check


bp = Blueprint('schedule', __name__, url_prefix='/schedule') 

@bp.route('/') 
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


@bp.route('/<num>', methods=['GET', 'POST'])
def detail(num):
    BASE_URL = 'https://www.chloeting.com/program/'

    #프로그램 리스트 가져오기
    page_p = requests.get(BASE_URL)
    soup_p = BeautifulSoup(page_p.content, 'html.parser')

    title_p = soup_p.find('div', class_='programs-list').find_all('a')

    programs = []
    for link in title_p:
        programs.append(link.get('href'))

    #프로그램별 스케줄 가져오기

    url = BASE_URL + programs[int(num)]
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    elm = soup.find_all('div', class_='info')

    day_list = []

    for e in elm:
        day_list.append(e.text.strip().split('\n'))

    dict_list = []
    for i in range(len(day_list)):
        dict_list.append({'day':day_list[i][0], 'time':day_list[i][3].strip()})

    dict_len = len(dict_list)


    return render_template('modi-sche.html', programs=programs, dict_list=dict_list, num=int(num), dict_len=dict_len)

@bp.route('/<num>/check', methods=['POST'])
def check(num):
    q_list = Check.query.filter(Check.index).all()
    if len(q_list) == 0 :
        index = 1
    else :
        index = len(q_list) + 1

    userid = session['user_id']
    comm = request.form['comm']
    date = request.form['date']
    day_num = request.form['day']

    BASE_URL = 'https://www.chloeting.com/program/'

    #프로그램 리스트 가져오기
    page_p = requests.get(BASE_URL)
    soup_p = BeautifulSoup(page_p.content, 'html.parser')

    title_p = soup_p.find('div', class_='programs-list').find_all('a')

    programs = []
    for link in title_p:
        programs.append(link.get('href'))

    pro = programs[int(num)].split('.')[0].split('/')[1].upper()

    #프로그램별 스케줄 가져오기

    url = BASE_URL + programs[int(num)]
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    elm = soup.find_all('div', class_='info')

    day_list = []

    for e in elm:
        day_list.append(e.text.strip().split('\n'))

    dict_list = []
    for i in range(len(day_list)):
        dict_list.append({'day':day_list[i][0], 'time':day_list[i][3].strip()})

    datime = f"{dict_list[int(day_num)-1]['day']} | {dict_list[int(day_num)-1]['time']}"

    check = Check(index=index, userid=userid, comm=comm, date=date, datime=datime, pro=pro)
    db.session.add(check)
    db.session.commit()

    return redirect(url_for('schedule.board'))

@bp.route('/board', methods=['GET', 'POST'])
def board():
    user_row = Check.query.filter_by(userid=session['user_id']).all()
    user_len=len(user_row)

    comm = []
    date = []
    datime = []
    pro = []
    index = []

    for i in range(user_len) :
        comm.append(user_row[i].comm)
        date.append(user_row[i].date)
        datime.append(user_row[i].datime)
        pro.append(user_row[i].pro)
        index.append(user_row[i].index)

    BASE_URL = 'https://www.chloeting.com/program/'

    #프로그램 리스트 가져오기
    page_p = requests.get(BASE_URL)
    soup_p = BeautifulSoup(page_p.content, 'html.parser')

    title_p = soup_p.find('div', class_='programs-list').find_all('a')

    programs = []
    for link in title_p:
        programs.append(link.get('href'))

    return render_template('board.html', date=date, comm=comm, user_len=user_len, programs=programs, datime=datime, pro=pro, index=index)

@bp.route('/edit/<index>', methods=['GET', 'POST'])
def edit(index):
    return render_template('edit.html', index=index)

@bp.route('/edit/<index>/done', methods=['GET', 'POST'])
def edit_done(index):
    q_list = Check.query.filter(Check.index==index).first()

    userid = session['user_id']
    comm = request.form['comm']
    date = request.form['date']
    pro = q_list.pro
    datime = q_list.datime

    db.session.delete(q_list)
    db.session.commit()

    check = Check(index=index, userid=userid, pro=pro, datime=datime, comm=comm, date=date)
    db.session.add(check)
    db.session.commit()

    return redirect(url_for('schedule.board'))


@bp.route('/delete/<index>', methods=['GET', 'POST'])
def delete(index):
    q_list = Check.query.filter(Check.index==index).first()

    db.session.delete(q_list)
    db.session.commit()

    return redirect(url_for('schedule.board'))