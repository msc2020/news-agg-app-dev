from flask import Flask, render_template, request, url_for, flash, redirect
#from flask_wtf.csrf import CSRFProtect

import random

import os
from environs import Env

from datetime import datetime
import pytz


from models import scrapy
from tests import *

import json

# set debug to input data
# TESTS_DEBUG = True
TESTS_DEBUG = False
N_MAX = 2

env = Env()
env.read_env()

# instance flask
app = Flask(__name__)
#app.secret_key = env.str('FLASK_SECRET_KEY_NEWS_AGG_APP') # dev
app.secret_key = os.getenv('FLASK_SECRET_KEY_NEWS_AGG_APP')

# local date
date = datetime.now(pytz.timezone('Brazil/East'))


if TESTS_DEBUG == False:
    # run scrapy
    print('\n[scrapy_each_site()] Making scraping ...')
    
    news_bdf, news_icl, news_agencia_brasil, news_poder360,\
        news_carta_capital, news_uol, news_g1, news_canaltech, news_olhar_digital,\
        tempo_gasto = scrapy.scrapy_each_site()
    print('\n[scrapy_each_site()] Done.')

    # top N news
    def top_news(verbose=False):
<<<<<<< HEAD
        all_news = [news_bdf, news_carta_capital, news_g1, news_icl, \
=======
        all_news = [news_bdf, news_carta_capital, news_g1, news_icl,\
>>>>>>> 23b867d (-)
            news_agencia_brasil, news_poder360,\
            news_uol, news_canaltech, news_olhar_digital]
        
        res = []
        for news_list in all_news:
            if len(news_list) > 1:
                if news_list[0]['site'] in ['ICL Notícias', 
                                            'Agência Brasil',
                                            'Carta Capital', 
                                            'Poder 360',
                                            'UOL',
                                            'G1-Mundo']:
                    res += news_list[:N_MAX + 1]
                else:
                    res += news_list[:1]                       
        return res, tempo_gasto
else:
    pass


# home
@app.route('/')
def root():
    
    if TESTS_DEBUG == False:
        all_top_news, tempo_gasto = top_news()
        return render_template('all_news.html',
                               list_news=all_top_news, date=date, tempo_gasto=tempo_gasto)
    else:
        global t0
        return render_template('all_news.html', list_news=tests_news, date=date, tempo_gasto=0)

# geral
@app.route('/geral')
def geral():
    if TESTS_DEBUG == False:
        general_news = news_carta_capital + news_agencia_brasil + news_uol
        general_news = scrapy.take_news_by_tag(general_news, 'Gerais')
        return render_template('general.html', list_news=general_news, date=date, tempo_gasto=tempo_gasto)
    else:
        general_news = scrapy.stake_news_by_tag(tests_news, 'Gerais')
        return render_template('general.html', list_news=general_news, date=date, tempo_gasto=0)


# tech
@app.route('/tech')
def tech():
    if TESTS_DEBUG == False:
        tech_news = news_canaltech + news_olhar_digital
        tech_news = scrapy.take_news_by_tag(tech_news, 'Tecnologia')
        return render_template('tech.html', list_news=tech_news, date=date, tempo_gasto=tempo_gasto)
    else:
        tech_news = scrapy.take_news_by_tag(tests_news, 'Tecnologia')
        return render_template('tech.html', list_news=tech_news, date=date, tempo_gasto=0)
