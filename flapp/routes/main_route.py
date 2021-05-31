#Blueprint

from sys import dont_write_bytecode
from flask import Flask, Blueprint, redirect, render_template, url_for
import requests
from bs4 import BeautifulSoup
from werkzeug.utils import redirect

bp = Blueprint('schedule', __name__, url_prefix='/schedule') 


#n333 ----------------------------------------------
from flask import request

@bp.route('/<num>')
def active(num):
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

    return render_template('detail-sche.html', dict_list=dict_list, num=num)

@bp.route('/check', methods=['GET', 'POST'])
def check():
    done = request.args.get('done')
    date = request.args.get('date')

    if done in None:
        done == 'undone'

    object = Check(done=done, date=date)
    db.session.add(object)
    db.session.commit()

    return redirect(url_for('schedule'))