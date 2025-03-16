import time
import requests
from bs4 import BeautifulSoup
import random

from models import sentiment_analysis

import threading
import concurrent.futures

thread_local = threading.local()


def take_news_by_tag(list_news: list, tag: str) -> list:
    ''' Take news by tag.
    '''
    res = []

    for news in list_news:
        if news['tag'] == tag:
            res.append(news)

    return res

def get_empty_item() -> dict:
    ''' Get an empty item.
    '''
    item = {
        'site': None,
        'title_news': None,
        'url_news': None,
        'tag': None,
        'img_src': None,
        'raia': None,
        'url_site': None
    }

    return item

def get_random_n(
    min_n: int, 
    max_n: int
    ) -> int:
    '''Get a random int n.
    '''
    return int(random.randint(min_n, max_n))

def add_sentiment_item(item: dict, title_news: str):
    '''Add sentiment item with ml.
    '''
    print(f'\n[add_sentiment_item] title_news: {title_news}')
    news_sentiment = sentiment_analysis.sentence_analysis(title_news)
    res = {**item, **news_sentiment}
    return res

def get_item(param, title_news: str, url_news: str) -> dict:
    '''Get item.
    '''
    # print(f'\n[get_item] title_news: {title_news}')
    # print(f'\n[get_item] param.keys(): {param.keys()}')
    return {'site': param['site'], 
            'title_news': title_news, 
            'url_news': url_news, 
            'tag': param['tag'], 
            'img_src': param['img_src'], 
            'raia': param['raia'],
            'n_max': param['n_max']} 

# scrapy
def scrapy_agencia_brasil(param, soup):
    '''Scrapy Agência Brasil
    '''
    k = 0
    res = []
    # print(f"[scrapy_agencia_brasil] param['url_site']: {param['url_site']}")
    for a in soup.find('div', class_='linha-noticia rowflex').find_all('a'):
        url_news = param['url_site'] + a['href']
        url_news = url_news.strip()
        if '-' not in url_news:
            url_news = param['url_site']

        title_news = a.get_text().split('\n')[2].strip()
        # print(f"[scrapy_agencia_brasil] title_news: {title_news}")
        # print(f"[scrapy_agencia_brasil] url_news: {url_news}")
        # print(f"[scrapy_agencia_brasil] param['n_max']: {param['n_max']}")
        item = get_item(param=param, title_news=title_news, url_news=url_news)

        item = add_sentiment_item(item=item, title_news=title_news)

        res.append(item)

        k += 1
        if k == param['n_max']:
            break
    # print(f'[scrapy_agencia_brasil] res: {res}')
    return res

def scrapy_bdf(param: dict, soup: BeautifulSoup)-> list:
    '''Scrapy BDF (Brasil de Fato) site.
    '''
    k = 0

    res = []
    for a in soup.find('section', class_='most-read spacing').find_all('a'):
        url_news = param['url_site'] + a['href'].strip()
        if '-' not in url_news:
            url_news = param['url_site']

        title_news = a.get_text().strip()

        item = get_item(param=param, title_news=title_news, url_news=url_news)

        item = add_sentiment_item(item=item, title_news=title_news)

        res.append(item)

        k += 1
        if k == param['n_max']:
            break

    return res

def scrapy_carta_capital(param, soup):
    '''Scrapy BDF (Brasil de Fato) site.
    '''
    k = 0
    res = []
    for row in soup.find_all('div', class_='h-news__list'):
        for a in row.find_all('a', class_='h-news__item'):
            url_news = a['href'].strip()
            title_news = a['title'].strip()
            
            if '-' not in url_news:
                url_news = param['url_site']
                
            item = get_item(param=param, title_news=title_news, url_news=url_news)

            item = add_sentiment_item(item=item, title_news=title_news)

            res.append(item)

            k += 1
            if k == param['n_max']:
                break
        if k == param['n_max']:
            break
    
    return res

def scrapy_icl_noticias(param, soup):
    '''Scrapy ICL Notícias.
    '''
    k = 0
    res = []

    for row in soup.find_all('div', class_='c-flex home-dest-block'):      
        for a in row.find_all('a')[1:]:                
            url_news = a['href'].strip()
            title_news = a.find('h2').get_text().strip()

            if '-' not in url_news:
                url_news = param['url_site']

            item = get_item(param=param, title_news=title_news, url_news=url_news)

            item = add_sentiment_item(item=item, title_news=title_news)

            res.append(item)

            k += 1
            if k == param['n_max']:
                break
        if k == param['n_max']:
            break
    return res


def scrapy_g1(param, soup):
    ''' Scrapy G1.
    '''
    k = 0
    res = []
    
    for row in soup.find_all('div', class_='feed-post-body-title gui-color-primary gui-color-hover'):
        title_news = row.find('h2').get_text().strip()
        url_news = row.find_all('a')[0]['href'].strip()
        
        if '-' not in url_news:
            url_news = param['url_site']
            
        item = get_item(param=param, title_news=title_news, url_news=url_news)

        item = add_sentiment_item(item=item, title_news=title_news)

        res.append(item)

        k += 1
        if k == param['n_max']:
            break

    return res

def scrapy_g1_tech(param, soup):
    '''Scrapy G1 Tech.
    '''
    k = 0
    res = []

    for row in soup.find('div', class_='_evt').find_all('a'):
        title_news = row.get_text().replace('\n', '').strip()
        url_news = row['href'].strip()
        if len(title_news) > 0:
            if '-' not in url_news:
                url_news = param['url_site']

            item = get_item(param=param, title_news=title_news, url_news=url_news)

            item = add_sentiment_item(item=item, title_news=title_news)

            res.append(item)

            k += 1

        if k == param['n_max']:
            break

    return res


def scrapy_olhar_digital(param, soup):
    ''' Scrapy Olhar Digital.
    '''
    k = 0
    res = []

    for row in soup.find_all('div', class_='post-list margin-wrapper-lg columns2'):
        for a in row.find_all('a'):
            title_news = a.find('h2').get_text().strip()
            url_news = a['href'].strip()

            if '-' not in url_news:
                url_news = param['url_site']

            item = get_item(param=param, title_news=title_news, url_news=url_news)

            item = add_sentiment_item(item=item, title_news=title_news)

            res.append(item)

            k += 1
            if k == param['n_max']:
                break
        if k == param['n_max']:
            break

    return res


def scrapy_poder360(param, soup):
    '''Scrapy Poder 360.
    '''
    k = 0
    res = []

    for a in soup.find('ol', class_='box-ordered-list__list').find_all('a'):
        url_news = a['href'].strip()
        title_news = a.get_text().strip()

        if '-' not in url_news:
            url_news = param['url_site']

        item = get_item(param=param, title_news=title_news, url_news=url_news)

        item = add_sentiment_item(item=item, title_news=title_news)

        res.append(item)

        k += 1
        if k == param['n_max']:
            break

    return res


def scrapy_uol(param, soup):
    '''Scrapy UOL.
    '''
    k = 0
    res = []

    for row in soup.find_all('li', class_='mostRead__item'):
        title_news = row.get_text().strip()
        for a in row.find_all('a', href=True):
            url_news = a['href'].strip()

            if '-' not in url_news:
                url_news = param['url_site']

            item = get_item(param=param, title_news=title_news, url_news=url_news)

            item = add_sentiment_item(item=item, title_news=title_news)

            res.append(item)

            k += 1
            if k == param['n_max']:
                break
        if k == param['n_max']:
            break
    
    return res

def scrapy_canaltech(param, soup):
    '''Scrapy Canaltech.
    '''
    k = 0
    res = []

    for row in soup.find_all('a', class_='jc'):
        title_news = row.find('h3').get_text().strip()
        url_news = param['url_site'] + row['href']

        if '-' not in url_news:
            url_news = param['url_site']

        item = get_item(param=param, title_news=title_news, url_news=url_news)

        item = add_sentiment_item(item=item, title_news=title_news)

        res.append(item)

        k += 1
        if k == param['n_max']:
            break 

    return res

def run_scrapy(params, verbose=False):
    ''' Run scrapy.
    '''
    # print(f'[run_scrapy] params.keys(): {params.keys()}')
    res = []
    try:
        html = params['response_text']#await response.text() # ok ?
        # print(f"[run_scrapy] >>> Read {html[:5]} bytes from {params['url_site']}")
        soup = BeautifulSoup(html, 'html.parser')  # ok ?

        print(f"\n[run_scrapy] Feito request [{params['site']}].")

        if params['site'] == 'ICL Notícias':
            res = scrapy_icl_noticias(params, soup)
        elif params['site'] == 'Agência Brasil':
            res = scrapy_agencia_brasil(params, soup)
        elif params['site'] == 'Brasil de Fato':
            res = scrapy_bdf(params, soup)
        elif params['site'] == 'Poder 360':
            res = scrapy_poder360(params, soup)
        elif params['site'] == 'Carta Capital':
            res = scrapy_carta_capital(params, soup)
        elif params['site'] == 'UOL':
            res = scrapy_uol(params, soup)
        elif params['site'] == 'G1-Mundo':
            res = scrapy_g1(params, soup)
        elif params['site'] == 'Canaltech':
            res = scrapy_canaltech(params, soup)
        elif params['site'] == 'Olhar Digital':
            res = scrapy_olhar_digital(params, soup)
        elif params['site'] == 'G1-Tecnologia':
            res = scrapy_g1_tech(params, soup)        

        print(f"[run_scrapy] Feito scrapy {params['site']}.")

    except Exception as e:
        print(f'[run_scrapy] Erro ao fazer request.\n{e}')
        item = get_empty_item()
        res.append(item)
    print(f'[run_scrapy] # Notícias: {len(res)}')
    # print(f'[run_scrapy] res: {res}')
    return res


# parâmetros para scrapy
params = []

params_agencia_brasil = {
    'verbose': False, 
    'site': 'Agência Brasil',
    'tag': 'Gerais', 
    'n_max': get_random_n(2, 3),
    'raia': 'center',
    'img_src': 'images/agencia_brasil_logo.png',
    'url_site': 'https://agenciabrasil.ebc.com.br/'
    }

params_bdf_scrapy = {
    'verbose': False, 
    'site': 'Brasil de Fato',
    'tag': 'Gerais', 
    'n_max': get_random_n(1, 2),
    'raia': 'left',
    'img_src': 'images/bdf_logo.png',
    'url_site': 'https://www.brasildefato.com.br/',
    }

params_canaltech = {
    'verbose': False, 
    'site': 'Canaltech',
    'tag': 'Tecnologia', 
    'n_max': get_random_n(1, 3),
    'raia': 'right',
    'img_src': 'images/canaltech_logo.png',
    'url_site': 'https://canaltech.com.br/mais-lidas',
    }

params_carta_capital = {
    'verbose': False,
    'site':'Carta Capital',
    'tag':'Gerais', 
    'n_max':get_random_n(2, 3),
    'raia':'left',
    'img_src':'images/carta_capital_logo.png',
    'url_site':'https://www.cartacapital.com.br/'
    }

params_g1_mundo = {
    'verbose': False, 
    'site': 'G1-Mundo',
    'tag': 'Gerais', 
    'n_max': get_random_n(1, 2),
    'raia': 'right',
    'img_src': 'images/g1_logo.png',
    'url_site': 'https://g1.globo.com/mundo',
    }

params_g1_tech = {
    'verbose': False, 
    'site': 'G1-Tecnologia',
    'tag': 'Tecnologia', 
    'n_max': get_random_n(2, 3),
    'raia': 'left',
    'img_src': 'images/g1_logo.png',
    'url_site': 'https://g1.globo.com/tecnologia', 
    }

params_icl_noticias = {
    'verbose': False, 
    'site': 'ICL Notícias',
    'tag': 'Gerais',
    'n_max': get_random_n(1, 2),
    'raia': 'left',
    'img_src': 'images/icl_logo.png',
    'url_site': 'https://iclnoticias.com.br/'
    }

params_olhar_digital = {
    'verbose': False, 
    'site': 'Olhar Digital',
    'tag': 'Tecnologia', 
    'n_max': get_random_n(1, 3),
    'raia': 'center',
    'img_src': 'images/olhar_digital_logo.png',
    'url_site': 'https://olhardigital.com.br/editorias/noticias/',
    }

params_poder360 = {
    'verbose': False, 
    'site': 'Poder 360',
    'tag': 'Gerais', 
    'n_max': get_random_n(1, 2),
    'raia': 'center',
    'img_src': 'images/poder_360_logo.png',
    'url_site': 'https://www.poder360.com.br/',
    }

params_uol_scrapy = {
    'verbose': False, 
    'site': 'UOL',
    'tag': 'Gerais', 
    'n_max': get_random_n(1, 2),
    'raia': 'right',
    'img_src': 'images/uol_logo.png',
    'url_site': 'https://www.uol.com.br/',
    }


params.append(params_agencia_brasil)
params.append(params_bdf_scrapy)
params.append(params_canaltech)
params.append(params_carta_capital)
params.append(params_g1_mundo)
params.append(params_g1_tech)
params.append(params_icl_noticias)
params.append(params_olhar_digital)
params.append(params_poder360)
params.append(params_uol_scrapy)

# print('\n[checks]')
# print(f'>>> params: {params}')

def add_downloaded_site(_param):
    '''Add downloaded site.
    '''
    param = _param
    # print(f'\n[add_downloaded_site] {param}')
    param['response_text'] = requests.get(param['url_site'], timeout=9).text
    print(f"\n[add_downloaded_site] param['site']: {param['site']}")
    res = run_scrapy(param)
    # print(f'[add_downloaded_site] res: {res}')
    return res

res_scrapy = []
def scrapy_all_sites():
    ''' Run scrapy for each site.
    '''
    print('\n[scrapy_all_sites]')
    t0 = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        global res_scrapy
        res_scrapy = []
        print(f'[scrapy_all_sites][ThreadPoolExecutor]')
        # print(f'params: {params}')
        res_scrapy = list(executor.map(add_downloaded_site, params))
        executor.shutdown(wait=True)
        # print(f' [ThreadPoolExecutor] res_scrapy: {res_scrapy}')

        print(' [ThreadPoolExecutor] Loop executado.')
        print('\n', 30*'-')

    tempo_gasto = round(time.time() - t0, 2)
    print(f'\n\n[scrapy_all_sites] Tempo gasto: {tempo_gasto:.2f} s\n\n')
    print('\n', 30*'-')
    return res_scrapy, tempo_gasto


def run_all_scrapy():
    ''' Run all scrapies.
    '''
    res_scrapy, tempo_gasto = scrapy_all_sites()
    print('\n[run_all_scrapy ...]\n')
    # print(f'[run_all_scrapy] res_scrapy[0]:\n{res_scrapy[0]}')
    return res_scrapy, tempo_gasto
    