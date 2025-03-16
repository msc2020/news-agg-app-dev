'''
app.py
'''
from flask import Flask, render_template, request, url_for, flash, redirect
#from flask_wtf.csrf import CSRFProtect

import os
from environs import Env
import random

from datetime import datetime
import pytz

from models import scrapy

import json

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func, text

import pymysql
pymysql.install_as_MySQLdb()

import pandas as pd

from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import components 

from bokeh.models import ColumnDataSource, Whisker, Label, LabelSet
from bokeh.plotting import figure, ColumnDataSource #, show
from bokeh.transform import dodge, factor_cmap, jitter
from bokeh.core.properties import value
from bokeh.transform import cumsum, factor_cmap

from bokeh.util.warnings import BokehUserWarning 
import warnings 
warnings.simplefilter(action='ignore', category=BokehUserWarning)


EXPORT_DUMP = False # True, False

TESTS_DEBUG = False # True, False


env = Env()
env.read_env()

# instance flask
app = Flask(__name__)
#app.secret_key = env.str('FLASK_SECRET_KEY_NEWS_AGG_APP') # dev

# configs db
# mysql://username:password@host:port/database_name

# prod
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('MYSQL_URL')

#dev
# app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{os.getenv("MYSQLUSER")}:{os.getenv("MYSQLPASSWORD")}@{os.getenv("MYSQLHOST")}:{os.getenv("MYSQLPORT")}/{os.getenv("MYSQLDATABASE")}'

# disables the tracking of modifications to SQLAlchemy session objects, avoid overhead
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class GlobalVars():
    # https://stackoverflow.com/questions/49664010/using-variables-across-flask-routes
    all_top_news = None
    tempo_gasto = None
    local_date = None

data = GlobalVars()

# instance database
db = SQLAlchemy(app)

class News(db.Model):
    '''
    Database model.
    '''
    id = db.Column(db.Integer, primary_key=True)
    site = db.Column(db.String(50), nullable=False)
    title_news = db.Column(db.String(200), nullable=False)
    url_news = db.Column(db.String(200), unique=True, nullable=False)
    tag = db.Column(db.String(50), nullable=False)
    img_src = db.Column(db.String(200))
    score_tb = db.Column(db.Float)
    sentiment_tb = db.Column(db.String(50))
    score_subjectivity = db.Column(db.Float)
    subjectivity_tb = db.Column(db.String(50))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f'>>> News:\n{self.site}'

    def insert(self):
        ''' Insere no dataset.
        '''
        db.session.add(self)
        db.session.commit()
        print('>>> Ok - registrado no banco de dados.')

with app.app_context():
    try:
        db.create_all()
        print('\n[create_schema] OK.')
    except Exception as e:
        print(f'\n[create_schema] Error:\n{e}')


def insert_to_dataset(news_list_dict: list) -> None:
    ''' Insere no dataset.
    '''
    print(f'\n[insert_to_dataset] Inserindo {len(news_list_dict)} novas news...')
    i = 0
    # print(f'[insert_to_dataset] news_list_dict.keys(): {news_list_dict[:3]}')
    for news_item in news_list_dict:
        # print(f'\n[insert_to_dataset] news_item: {news_item}')
        try:
            noticia_atual = News()
            noticia_atual.site = news_item['site']
            noticia_atual.title_news = news_item['title_news']
            noticia_atual.url_news = news_item['url_news']
            if TESTS_DEBUG:
                noticia_atual.tag = news_item['tag']
                noticia_atual.img_src = news_item['img_src']
                noticia_atual.score_tb = random.randrange(5, 11)
                noticia_atual.sentiment_tb = 'negativo'
                noticia_atual.score_subjectivity = random.randrange(70, 99)
                noticia_atual.subjectivity_tb = 'subjetivo'
            else:
                noticia_atual.tag = news_item['tag']
                noticia_atual.img_src = news_item['img_src']
                noticia_atual.score_tb = news_item['score_tb']
                noticia_atual.sentiment_tb = news_item['sentiment_tb']
                noticia_atual.score_subjectivity = news_item['score_subjectivity']
                noticia_atual.subjectivity_tb = news_item['subjectivity_tb']
            noticia_atual.insert()
            i += 1
        except Exception as e:
            db.session.rollback()
            if '1062' or 'Duplicate entry' in str(e):
                print('  >>> Erro ao inserir na base: já existe na base.')
            else:
                print('  >>> Erro ao inserir na base.')
            # print(f'  >>> [insert_to_dataset] Erro:\n{e}')

    print(f'\n[insert_to_dataset] Ok. Inserido {i} news na base.\n')


def insert_db_top_news(list_all_top_news: list, verbose: bool=False) -> list:
    ''' Insere top N news no DB.
    '''
    res = []
    for news_item in list_all_top_news:
        for news_subitem in news_item:
            res.append(news_subitem)
    if verbose:
        print(f'\n[insert_db_top_news] res:\n{res}')
    insert_to_dataset(res)
    print(f'\n[insert_db_top_news] Ok. Filtrado {len(res)} top news.')
    return res


if TESTS_DEBUG == False:
    print('\n[modo debug = False]') # will run scrapy
else:
    print('\n[modo debug = True]')

# home
@app.route('/')
def root():
    ''' Home page - Scrapy all sites in the queue.
    '''
    if TESTS_DEBUG == False:
        try:
            data.local_date = datetime.now(pytz.timezone('Brazil/East'))
            all_news, tempo_gasto = scrapy.run_all_scrapy()
            print(f'\n[root] len(all_news): {len(all_news)}')
            print(f'[root] tempo_gasto: {tempo_gasto}')
            print('[root] scrapy_each_site() Feito.')
            # print(f'[root] all_news[0]: {all_news[0]}')

            # define variáveis globais
            data.all_top_news = insert_db_top_news(all_news)
            data.tempo_gasto = tempo_gasto
            # print(f'\n[root] data.all_top_news[0].keys():\n{data.all_top_news[0].keys()}')

            #export a dump
            if EXPORT_DUMP:
                with open('data.json', 'w') as f:
                    json.dump(data.all_top_news, f)
        except Exception as e:
            print('[root] Erro:\n{e}')

        return render_template('all_news.html',
                               list_news=data.all_top_news,
                               date=data.local_date,
                               tempo_gasto=data.tempo_gasto)

    else:
        # TESTS_DEBUG != False

        # define variáveis globais
        f = open('data.json')
        f_content = f.read()
        data.local_date = datetime.now(pytz.timezone('Brazil/East'))
        data.all_top_news = json.loads(f_content)
        print('\n[root] JSON carregado.')

        # descomente para novo dump do db
        # data.all_top_news = insert_db_top_news(data.all_top_news)
        
        # seta tempo igual zero p/ testes
        data.tempo_gasto = 0

        # print(f'data.all_top_news[0]: {data.all_top_news[0]}')
        return render_template('all_news.html',
                               list_news=data.all_top_news,
                               date=data.local_date,
                               tempo_gasto=data.tempo_gasto)


@app.route('/all_news')
def all_news():
    ''' Render all news.
    '''
    if TESTS_DEBUG == False:
        return render_template(
            'all_news.html',
            list_news=data.all_top_news,
            date=data.local_date,
            tempo_gasto=data.tempo_gasto
        )
    else:
        # print(f'\n[root] data.all_top_news[0].keys():\n{data.all_top_news[0].keys()}')
        return render_template(
            'all_news.html', 
            list_news=data.all_top_news, 
            date=data.local_date,
            tempo_gasto=data.tempo_gasto
        )

@app.route('/geral')
def geral():
    ''' Render notícias gerais.
    '''
    if TESTS_DEBUG == False:
        general_news = scrapy.take_news_by_tag(data.all_top_news, 'Gerais')
        return render_template('general.html', list_news=general_news,
                               date=data.local_date, tempo_gasto=data.tempo_gasto)
    else:
        general_news = scrapy.take_news_by_tag(data.all_top_news, 'Gerais')
        return render_template('general.html', list_news=general_news,
                               date=data.local_date, tempo_gasto=data.tempo_gasto)

@app.route('/tech')
def tech():
    ''' Render tech news.
    '''
    if TESTS_DEBUG == False:
        tech_news = scrapy.take_news_by_tag(data.all_top_news, 'Tecnologia')
        return render_template('tech.html', list_news=tech_news, 
                               date=data.local_date, tempo_gasto=data.tempo_gasto)
    else:
        tech_news = scrapy.take_news_by_tag(data.all_top_news, 'Tecnologia')
        return render_template('tech.html', list_news=tech_news,
                               date=data.local_date, tempo_gasto=data.tempo_gasto)


# print(CDN.js_files)
@app.route('/visual')
def visual():
    ''' Gráficos.
    '''
    with db.session.connection() as connection:

        # generate graphic with bokeh
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekdays_pt = ['2a-feira', '3a-feira', '4a-feira',
                       '5a-feira', '6a-feira', 'Sábado', 'Domingo']
        background_fill_color = '#eff7f4'
        list_sentiments = ['positivo', 'neutro', 'negativo']

        qtde_neutros = len(weekdays)*[0]
        qtde_positivos = len(weekdays)*[0]
        qtde_negativos = len(weekdays)*[0]

        # dataset
        query = '''
        SELECT * FROM news
        LIMIT 1000;
        '''
        n_samples_db_query = connection.execute(text('SELECT COUNT(1) FROM news;')).fetchall()[0][0]
        print(f'\n[visual] n_samples_db_query: {n_samples_db_query}')
        result = connection.execute(text(query))
        df_news = pd.DataFrame(result.fetchall())
        df_news.columns = result.keys()
        df_news.created_at = pd.to_datetime(df_news.created_at)
        df_news = df_news[~df_news.site.str.contains('http')]
        n_samples_db = df_news.shape[0]

        print(f'[visual] n_samples_db: {n_samples_db}')

        df_news['day_name'] = df_news['created_at'].dt.day_name()
        # print(f'\n[overview] result:\n{df_news.head()}')

        df_news.rename(
            columns={'id': 'Quantidade',
            'sentiment_tb': 'Nível Positividade',
            'score_tb':'Score Positividade',
            'subjectivity_tb':'Nível Subjetividade',
            'score_subjectivity':'Score Subjetividade',
            'day_name': 'Dia da Semana',
            'site': 'Site'
            }, 
            inplace=True
        )

        # positividade por semana
        cols = ['Nível Positividade', 'Quantidade', 'Dia da Semana']
        df_week_sentiment = df_news[cols].groupby(
            by=['Dia da Semana',
                'Nível Positividade']
            ).count()

        # subjetividade por semana
        cols = ['Nível Subjetividade', 'Quantidade', 'Dia da Semana']
        df_week_subjectivity = df_news[cols].groupby(by=['Dia da Semana',
                                                         'Nível Subjetividade']).count()

        # últimas notícias - df.tail(20)
        cols = ['Data', 'Site', 'title_news', 'Score Positividade',
                'Nível Positividade', 'Score Subjetividade', 'Nível Subjetividade']
        df_news['Data'] = df_news['created_at'].dt.date

        df_tail = df_news[cols].tail(30)
        n_samples_table = df_tail.shape[0]
        df_tail.reset_index(inplace=True, drop=True)
        df_tail.rename(columns={'title_news': 'Notícia'}, inplace=True)
        print(f'[visual] n_samples_table: {n_samples_table}')

        df_value_counts = pd.DataFrame(df_news.Site.value_counts(dropna=False))
        df_value_counts.rename(columns={'count': 'Total'}, inplace=True)

        #############
        # gráfico 1 #
        #############
        for _, row in df_week_sentiment.reset_index().iterrows():
            weekday = row['Dia da Semana']
            positivity = row['Nível Positividade']
            qtde = row['Quantidade']
            idx_week = weekdays.index(weekday)
            # print(f'[{weekday}][{idx_week}]')
            if positivity == 'neutro':
                qtde_neutros[idx_week] = qtde
            elif positivity == 'positivo':
                qtde_positivos[idx_week] = qtde
            elif positivity == 'negativo':
                qtde_negativos[idx_week] = qtde
        
        data_graphic = {
            'Weekdays' : weekdays_pt, # weekdays,
            'Neutro'   : qtde_neutros,
            'Positivo'   : qtde_positivos,
            'Negativo'   : qtde_negativos
        }
        # print(f'\n[visual] data_graphic: {data_graphic}')
        source = ColumnDataSource(data=data_graphic)

        # y_max = max(qtde_neeutros + qtde_positivos + qtde_negativos)
        p = figure(
                x_range=weekdays_pt,
                tools='hover, box_select, zoom_in, zoom_out, box_zoom, reset, save',
                title='Positividade por dia da semana',
                width=550, 
                height=300,
                background_fill_color=background_fill_color,
                output_backend='webgl', 
                y_range=(0.0, 100.0)
            )

        p.vbar(x=dodge('Weekdays', 0.25, range=p.x_range), top='Negativo', source=source,
               width=0.23, color='#65AB65', legend_label='Negativo')

        p.vbar(x=dodge('Weekdays', -0.25, range=p.x_range), top='Neutro', source=source,
               width=0.23, color='#EBBB8B', legend_label='Neutro')

        p.vbar(x=dodge('Weekdays', 0, range=p.x_range), top='Positivo', source=source,
               width=0.23, color='#1F8DE1', legend_label='Positivo')

        p.x_range.range_padding = 0.1
        p.xgrid.grid_line_color = None
        p.legend.location = 'top_right'
        p.legend.orientation = 'horizontal'
        p.legend.click_policy='hide'
        p.legend.background_fill_alpha = 0.3

        p.hover.tooltips = [
            ('Dia da semana', '@Weekdays'),
            ('#Neutro', '@Neutro'),
            ('#Positivo', '@Positivo'),
            ('#Negativo', '@Negativo')
        ]
        p.title.text_font_size = '13pt'
        # show(p)
        script1, div1 = components(p, CDN)
        del p


        #############
        # gráfico 2 #
        #############
        col_class = 'Nível Positividade'#'sentiment_tb'
        col_score = 'Score Positividade'#'score_tb'
        classes = list(sorted(df_news[col_class].unique(), reverse=True))
        # classes = list(df_news[col_class].unique())
        # classes = list(sorted(classes))

        background_fill_color = '#eff7f4'
        p = figure(x_range=classes, 
                tools='hover, box_select, zoom_in, zoom_out, box_zoom, reset, save',
                #    tools='',
                title='Distribuição de Positividade',
                width=320,
                height=300,
                background_fill_color=background_fill_color,
                output_backend='webgl'
                )

        p.xgrid.grid_line_color = None

        g = df_news.groupby(col_class)
        upper = g[col_score].quantile(0.90).sort_index(ascending=False)
        lower = g[col_score].quantile(0.10).sort_index(ascending=False)

        if upper.equals(lower):
            upper = g[col_score].max().sort_index(ascending=False)
            lower = g[col_score].min().sort_index(ascending=False)

        # upper = []
        # lower = []
        # print(f'\n[visual][gráfico 2] lower: {lower}')
        # print(f'[visual][gráfico 2] upper: {upper}')
        source = ColumnDataSource(data=dict(base=classes, upper=upper, lower=lower))

        error = Whisker(base='base', upper='upper', lower='lower', source=source,
                        level='annotation', line_width=2)
        error.upper_head.size=20
        error.lower_head.size=20
        p.add_layout(error)

        p.scatter(jitter(col_class, width=0.3, range=p.x_range), col_score, source=df_news,
                  size=13, line_color='white', alpha=0.6,
                  color=factor_cmap(col_class, 'Category10_3', classes))

        p.hover.tooltips = [('Score de Positividade', '$y') ]
        p.title.text_font_size = '13pt'
        # p.legend.click_policy='hide'

        script2, div2 = components(p, CDN)
        del p


        #############
        # gráfico 3 #
        #############
        qtde_objetivos = len(weekdays)*[0]
        qtde_subjetivos = len(weekdays)*[0]
        qtde_neutros = len(weekdays)*[0]

        for _, row in df_week_subjectivity.reset_index().iterrows():
            weekday = row['Dia da Semana']
            subjetivity = row['Nível Subjetividade']
            qtde = row['Quantidade']
            idx_week = weekdays.index(weekday)
            # print(f'[{weekday}][{idx_week}]')
            if subjetivity == 'neutro':
                qtde_neutros[idx_week] = qtde
            elif subjetivity == 'objetivo':
                qtde_objetivos[idx_week] = qtde
            elif subjetivity == 'subjetivo':
                qtde_subjetivos[idx_week] = qtde

        data_graphic = {'Weekdays' : weekdays_pt,#weekdays,
                        'Neutro'   : qtde_neutros,
                        'Objetivo'   : qtde_objetivos,
                        'Subjetivo'   : qtde_subjetivos}
        # print(f'\n[visual] data_graphic: {data_graphic}')
        source = ColumnDataSource(data=data_graphic)

        # y_max = max(qtde_neutros + qtde_objetivos + qtde_subjetivos)
        p = figure(x_range=weekdays_pt,
                    tools='hover, box_select, zoom_in, zoom_out, box_zoom, reset, save',
                    title='Subjetividade por dia da semana',
                    width=550, height=300,
                    background_fill_color=background_fill_color,
                    output_backend='webgl', y_range=(0.0, 100.0))

        p.vbar(x=dodge('Weekdays', -0.275, range=p.x_range), top='Neutro', source=source,
               width=0.25, color="#EBBB8B", legend_label='Neutro')

        p.vbar(x=dodge('Weekdays', 0, range=p.x_range), top='Objetivo', source=source,
               width=0.25, color='#B5A2CE', legend_label='Objetivo')

        p.vbar(x=dodge('Weekdays', 0.275, range=p.x_range), top='Subjetivo', source=source,
               width=0.25, color='#85DE85', legend_label='Subjetivo')

        p.legend.click_policy='hide'

        p.x_range.range_padding = 0.1
        p.xgrid.grid_line_color = None
        p.legend.location = 'top_left'
        p.legend.orientation = 'horizontal'
        p.hover.tooltips = [
            ('Dia da semana', '@Weekdays'),
            ('#Neutro', '@Neutro'),
            ('#Objetivo', '@Objetivo'),
            ('#Subjetivo', '@Subjetivo')
        ]
        p.title.text_font_size = '13pt'
        p.legend.background_fill_alpha = 0.3
        # show(p)
        script3, div3 = components(p, CDN)
        del p


        # ###########
        # gráfico 4 #
        # ###########
        col_class = 'Nível Subjetividade'#'sentiment_tb'
        col_score = 'Score Subjetividade'#'score_tb'
        classes = list(sorted(df_news[col_class].unique(), reverse=True))
        # classes = list(sorted(classes))

        background_fill_color = '#eff7f4'
        p = figure(x_range=classes,
                tools='hover, box_select, zoom_in, zoom_out, box_zoom, reset, save',
                #    tools='',
                title='Distribuição de Subjetividade',
                width=320, height=300,
                background_fill_color=background_fill_color,
                output_backend='webgl'
                )

        p.xgrid.grid_line_color = None

        g = df_news.groupby(col_class)
        upper = g[col_score].quantile(0.90).sort_index(ascending=False)
        lower = g[col_score].quantile(0.10).sort_index(ascending=False)

        if upper.equals(lower):
            upper = g[col_score].max().sort_index(ascending=False)
            lower = g[col_score].min().sort_index(ascending=False)

        # print(f'[visual][gráfico 4] lower: {lower}')
        # print(f'[visual][gráfico 4] upper: {upper}')
        source = ColumnDataSource(data=dict(base=classes,
                                            upper=upper,
                                            lower=lower))

        # colors=['#EBBB8B', '#B5A2CE', '#85DE85']
        error = Whisker(base='base', upper='upper', lower='lower', source=source,
                        level='annotation', line_width=2)
        error.upper_head.size=20
        error.lower_head.size=20
        p.add_layout(error)

        p.scatter(jitter(col_class, width=0.3, range=p.x_range), 
                  col_score, source=df_news,
                  size=13, line_color='white', alpha=0.9,
                  color=factor_cmap(col_class, 'Accent5', classes))

        p.hover.tooltips = [('Score de Subjetividade', '$y') ]
        p.title.text_font_size = '13pt'
        
        script4, div4 = components(p, CDN)
        del p
        
        
        ############
        # gráfico 5
        ############
        rows = pd.crosstab(
            df_news['Site'], 
            df_news['Nível Positividade'],
            values=df_news['Score Positividade'],
            aggfunc='sum',
            normalize='index'
        )

        source = ColumnDataSource(rows.T)
        source.data['labels'] = list_sentiments

        categories =  list(df_news['Site'].unique())
        positivity = source.data['Nível Positividade']

        p = figure(y_range=categories, x_range=(-0.5, 1.3), height=400, width=780,
                    title='Positividade por Site',
                    tools= ''' zoom_in, zoom_out, 
                    box_zoom, reset, save
                    ''',
                    # tooltips="$name @x: @$name",

                    x_axis_location=None, toolbar_location='below', outline_line_color=None)
        p.grid.grid_line_color = None
        p.yaxis.fixed_location = 0
        p.axis.major_tick_line_color = None
        p.axis.major_label_text_color = None
        p.axis.axis_line_color = '#000001'
        p.axis.axis_line_width = 5
        p.title.text_font_size = '13pt'
        
        source.data['color'] = ['#ffffff','#010101', '#000000']
        source.data['color_sentiment'] = ['#EBBB8B', '#B5A2CE', '#85DE85']

        for i, y in enumerate(categories):
            left = cumsum(y, include_zero=True)
            right = cumsum(y)
            if i==0:
                p.hbar(y=value(y),
                       color='color_sentiment',
                       left=left, right=right,
                       source=source, height=0.9,
                       legend_field = 'labels'
                )
            else:
                p.hbar(y=value(y), color='color_sentiment',
                       left=left, right=right,
                       source=source, height=0.9
                )
                #    color=factor_cmap('Nível Positividade', 'Viridis4', positivity))
                # https://docs.bokeh.org/en/latest/docs/reference/palettes.html

            pcts = source.data[y]
            source.data[f'{y} texto'] = [
                f' {x*100:0.1f} %'
                .replace(' 0.0 %', '')
                .replace('.0 %', ' %') for r, x in zip(positivity, pcts)
            ]
            p.text(y=value(y),
                x=left,
                text=f'{y} texto',
                source=source,
                x_offset=17,
                y_offset=3,
                text_align='center',
                angle=3.14/5,
                text_color='color',
                text_baseline='middle',
                text_font_size='9px')


        totals = pd.crosstab(df_news['Site'],
                             df_news['Nível Positividade'],
                             values=df_news['Score Positividade'],
                             margins=True, aggfunc='sum',
                             normalize='columns').All

        p.hbar(right=0, left=-totals, y=totals.index, height=0.9, color='#dadada')

        texto = [f'{name} ({totals.loc[name]*100:0.1f}%)' for name in categories]
        p.text(y=categories, x=0, 
               text=texto, text_baseline='middle', text_align='right',
               x_offset=-15, text_color='#4a4a4a', text_font_size='13px',
               text_font_style='bold')

        p.yaxis.major_label_orientation = 'vertical'
        # p.hover.tooltips = [('Score Positividade', '$values') ]
        # p.legend.click_policy='hide'

        script5, div5 = components(p, CDN)
        del p

        return render_template('visual.html',
                            n_samples_db_query=n_samples_db_query,
                            cdn_link=CDN.js_files[0],
                            scripts=[script1, script2, script3, script4, script5],
                            divs=[div1, div2, div3, div4, div5],
                            date=data.local_date,
                            tempo_gasto=0)


@app.route('/overview')
def overview():
    '''Overview infos.
    '''

    with db.session.connection() as connection:
        query = '''
        SELECT * FROM news
        LIMIT 1000;
        '''
        n_samples_db_query = connection.execute(text('SELECT COUNT(1) FROM news;')).fetchall()[0][0]
        print(f'[overview()] n_samples_db_query: {n_samples_db_query}')
        result = connection.execute(text(query))
        df_news = pd.DataFrame(result.fetchall())
        df_news.columns = result.keys()
        df_news = df_news[~df_news.site.str.contains('http')]
        df_news.created_at = pd.to_datetime(df_news.created_at)
        n_samples_db = df_news.shape[0]
        print(f'[overview()] n_samples_db: {n_samples_db}')
        try:
            weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
                        'Friday', 'Saturday', 'Sunday']
            weekdays_pt = ['2a-feira', '3a-feira','4a-feira','5a-feira',
                           '6a-feira', 'Sábado', 'Domingo']
            df_news['day_name'] = df_news['created_at'].dt.day_name().apply(lambda x: weekdays_pt[weekdays.index(x)])
            print('\n[overview] weekdays_pt')
            # df_news['day_name'] = df_news['created_at'].dt.day_name()
        except:
            try:
                df_news['day_name'] = df_news['created_at'].dt.day_name(locale='pt_BR.utf8')              
            except:
                df_news['day_name'] = df_news['created_at'].dt.day_name()
        print(f'\n[overview] result:\n{df_news.head()}')

        df_news.rename(
            columns={'id': 'Quantidade',
            'sentiment_tb': 'Nível Positividade',
            'score_tb':'Score Positividade',
            'subjectivity_tb':'Nível Subjetividade',
            'score_subjectivity':'Score Subjetividade',
            'day_name': 'Dia da Semana',
            'site': 'Site'
            }, 
            inplace=True
        )

        # positividade por semana
        cols = ['Nível Positividade', 'Quantidade', 'Dia da Semana']
        df_week_sentiment = df_news[cols].groupby(by=['Dia da Semana', 
                                                      'Nível Positividade']).count()
        weekdays_pt_order = {'Domingo': 0, '2a-feira': 1,
                             '3a-feira': 2, '4a-feira': 3,
                             '5a-feira':4, '6a-feira':5, 
                             'Sábado':6
        }
        df_week_sentiment = df_week_sentiment.sort_index(key=lambda x: x.map(weekdays_pt_order))

        # subjetividade por semana
        cols = ['Nível Subjetividade', 'Quantidade', 'Dia da Semana']
        df_week_subjectivity = df_news[cols].groupby(by=['Dia da Semana', 
                                                            'Nível Subjetividade']).count()
        # count subjetividade
        cols = ['Quantidade', 'Nível Subjetividade']
        df_count_subjectivity = df_news[cols].groupby(by=['Nível Subjetividade']).count()

        # count positividade
        cols = ['Quantidade', 'Nível Positividade']
        df_count_sentiment = df_news[cols].groupby(by=['Nível Positividade']).count()

        # últimas notícias - df.tail(20)
        cols = ['Data', 'Site', 'title_news', 'Score Positividade', 
                'Nível Positividade', 'Score Subjetividade', 'Nível Subjetividade']
        df_news['Data'] = df_news['created_at'].dt.date

        df_tail = df_news[cols].tail(30)
        n_samples_table = df_tail.shape[0]
        df_tail.reset_index(inplace=True, drop=True)
        df_tail.rename(columns={'title_news': 'Notícia'}, inplace=True)
        print(f'n_samples_table: {n_samples_table}')

        df_value_counts = pd.DataFrame(df_news.Site.value_counts(dropna=False))
        df_value_counts.rename(columns={'count': 'Total'}, inplace=True)

        # print(df_week_sentiment.to_html())
        return render_template(
            'overview.html',
            total_db=n_samples_db,
            n_samples_df=n_samples_table,
            
            titles_tables_week=['_', 'Positividade por semana', 'Subjetividade por semana'],
            tables_week=[df_week_sentiment.to_html(), df_week_subjectivity.to_html()],

            titles_tables_count=['_', 'Subjetividade - quantidade', 'Positividade - quantidade'],
            tables_count=[df_count_subjectivity.to_html(), df_count_sentiment.to_html()],

            titles_tables_value_counts=['_', 'Total de Notícias por Site'],
            tables_value_counts=[df_value_counts.to_html()],

            titles_tables_tail=['_', 'Últimas Notícias'],
            tables_tail=[df_tail.to_html(table_id='last_news')],

            date=data.local_date,
            tempo_gasto=0
        )
