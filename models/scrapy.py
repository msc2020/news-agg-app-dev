import time
import requests
from bs4 import BeautifulSoup

from models import sentiment_analysis


def take_news_by_tag(list_news, tag):
    res = []

    for news in list_news:
        if news['tag'] == tag:
            res.append(news)
    
    return res


def get_empty_item():
    item = {'site': None, 'title_news': None, 'url_news': None, 
            'tag': None, 'img_src': None, 'espectro': None,
            'img_src': None, 'url_site': None}
    
    return item


## continuar
class Scrapy():
    def __init__(self, 
                 verbose: bool, 
                 site: str, 
                 tag: str,
                 n_max: int,
                 espectro: str,
                 img_src: str,
                 url_site: str):
        
        self.verbose = verbose, 
        self.site = site,
        self.tag = tag
        self.n_max = n_max,
        self.espectro = espectro
        self.img_src = img_src
        self.url_site = (url_site)
        # print([i for i in self.__dict__.items()])
        # print(f'n_max: {n_max} - self.n_max: {self.n_max[0]}')
        
    def __add_sentiment_item(self, item: dict, title_news: str):
        news_sentiment = sentiment_analysis.sentence_analysis(title_news)            
        item = {**item, **news_sentiment}
        return item
    
    def __get_item(self, title_news: str, url_news: str):
        return {'site': self.site[0], 'title_news': title_news, 
                'url_news': url_news, 'tag': self.tag, 
                'img_src': self.img_src, 'espectro': self.espectro} 
    
    # scrapy
    def __scrapy_agencia_basil(self, soup):
        k = 0
        res = []
        
        for a in soup.find('div', class_='linha-noticia rowflex').find_all('a'):
            url_news = self.url_site + a['href']
            url_news = url_news.strip()
            if '-' not in url_news:
                url_news = self.url_site
            
            title_news = a.get_text().split('\n')[2].strip()
            
            item = self.__get_item(title_news, url_news)
            
            item = self.__add_sentiment_item(item, title_news)
            
            res.append(item)
            
            k += 1
            if k == self.n_max[0]:
                break
        
        return res
    
    def __scrapy_bdf(self, soup):
        k = 0
        res = []
        
        for a in soup.find('section', class_='most-read spacing').find_all('a'):
            url_news = self.url_site + a['href'].strip()
            if '-' not in url_news:
                url_news = self.url_site
            
            title_news = a.get_text().strip()
            
            item = self.__get_item(title_news, url_news)
            
            item = self.__add_sentiment_item(item, title_news)
            
            res.append(item)
            
            k += 1
            if k == self.n_max[0]:
                break
        
        return res
    
    def __scrapy_icl_noticias(self, soup):
        k = 0
        res = []
        
        for row in soup.find_all('div', class_='c-flex home-dest-block'):      
            for a in row.find_all('a')[1:]:                
                url_news = a['href'].strip()
                title_news = a.find('h2').get_text().strip()
                
                if '-' not in url_news:
                    url_news = self.url_site
                    
                item = self.__get_item(title_news, url_news)

                item = self.__add_sentiment_item(item, title_news)

                res.append(item)

                k += 1
                if k == self.n_max[0]:
                    break
            if k == self.n_max[0]:
                break
        return res

    def __scrapy_olhar_digital(self, soup):
            k = 0
            res = []
            
            for row in soup.find_all('div', class_='post-list margin-wrapper-lg columns2'):
                for a in row.find_all('a'):
                    title_news = a.find('h2').get_text().strip()
                    url_news = a['href'].strip()
                    
                    if '-' not in url_news:
                        url_news = self.url_site
                        
                    item = self.__get_item(title_news, url_news)

                    item = self.__add_sentiment_item(item, title_news)

                    res.append(item)

                    k += 1
                    if k == self.n_max[0]:
                        break
                if k == self.n_max[0]:
                    break
            
            return res
        
    def __scrapy_poder360(self, soup):
        k = 0
        res = []
        
        for a in soup.find('ol', class_='box-ordered-list__list').find_all('a'):
            url_news = a['href'].strip()
            title_news = a.get_text().strip()
            
            if '-' not in url_news:
                url_news = self.url_site
                
            item = self.__get_item(title_news, url_news)

            item = self.__add_sentiment_item(item, title_news)

            res.append(item)

            k += 1
            if k == self.n_max[0]:
                break
      
        return res
    
    def __scrapy_carta_capital(self, soup):
        k = 0
        res = []
        
        for row in soup.find_all('div', class_='h-news__list'):
            for a in row.find_all('a', href=True):
                url_news = a['href'].strip()
                title_news = soup.find('div', class_='h-news__list').find('a', href=True).get('title').strip()
                
                if '-' not in url_news:
                    url_news = self.url_site
                    
                item = self.__get_item(title_news, url_news)

                item = self.__add_sentiment_item(item, title_news)

                res.append(item)

                k += 1
                if k == self.n_max[0]:
                    break
            if k == self.n_max[0]:
                break
        
        return res
    
    def __scrapy_uol(self, soup):
        k = 0
        res = []
        
        for row in soup.find_all('li', class_='mostRead__item'):
            title_news = row.get_text().strip()
            for a in row.find_all('a', href=True):
                url_news = a['href'].strip()
                
                if '-' not in url_news:
                    url_news = self.url_site
                    
                item = self.__get_item(title_news, url_news)

                item = self.__add_sentiment_item(item, title_news)

                res.append(item)

                k += 1
                if k == self.n_max[0]:
                    break
            if k == self.n_max[0]:
                break
        
        return res
    
    def __scrapy_g1(self, soup):
        k = 0
        res = []
        
        for row in soup.find_all('div', class_='feed-post-body-title gui-color-primary gui-color-hover'):
            title_news = row.find('h2').get_text().strip()
            url_news = row.find_all('a')[0]['href'].strip()
            
            if '-' not in url_news:
                url_news = self.url_site
                
            item = self.__get_item(title_news, url_news)

            item = self.__add_sentiment_item(item, title_news)

            res.append(item)

            k += 1
            if k == self.n_max[0]:
                break    
        
        return res
    
        k = 0
        res = []
        
        for row in soup.find_all('div', class_='feed-post-body-title gui-color-primary gui-color-hover'):
            title_news = row.find('h2').get_text().strip()
            url_news = row.find_all('a')[0]['href'].strip()
            
            if '-' not in url_news:
                url_news = self.url_site
                
            item = self.__get_item(title_news, url_news)

            item = self.__add_sentiment_item(item, title_news)

            res.append(item)

            k += 1
            if k == self.n_max[0]:
                break    
        
        return res
    
    def __scrapy_canaltech(self, soup):
        k = 0
        res = []
        
        for row in soup.find_all('a', class_='jc'):
            title_news = row.find('h3').get_text().strip()
            url_news = self.url_site + row['href']
            
            if '-' not in url_news:
                url_news = self.url_site
                
            item = self.__get_item(title_news, url_news)

            item = self.__add_sentiment_item(item, title_news)

            res.append(item)

            k += 1
            if k == self.n_max[0]:
                break    
        
        return res
    
    def __run_scrapy(self, verbose=False):
        res = []
        try:
            html = requests.get(self.url_site).text
            soup = BeautifulSoup(html, 'html.parser')
                 
            print(f'>> Feito request [{self.site}].')
            
            if verbose: print(soup.prettify())
            
            if verbose: print(f'>>> self.site[0]: {self.site[0]}')
            if self.site[0] == 'ICL Notícias':
                res = self.__scrapy_icl_noticias(soup)
            elif self.site[0] == 'Agência Brasil':
                res = self.__scrapy_agencia_basil(soup)
            elif self.site[0] == 'Brasil de Fato':
                res = self.__scrapy_bdf(soup)
            elif self.site[0] == 'Poder 360':
                res = self.__scrapy_poder360(soup)
            elif self.site[0] == 'Carta Capital':
                res = self.__scrapy_carta_capital(soup)
            elif self.site[0] == 'UOL':
                res = self.__scrapy_uol(soup)
            elif self.site[0] == 'G1-Mundo':
                res = self.__scrapy_g1(soup)
            elif self.site[0] == 'Canaltech':
                res = self.__scrapy_canaltech(soup)
            elif self.site[0] == 'Olhar Digital':
                res = self.__scrapy_olhar_digital(soup)            
                
            print(f'>> Feito scrapy {self.site[0]}.')
               
        except Exception as e:
            print('>> Erro ao fazer request.')
            print(f'>> {e}')
            item = get_empty_item()
            res.append(item)
        print(f'>>> # Notícias: {len(res)}')
        return res
    
    
    def run_scrapy(self):
        return self.__run_scrapy()

## continuar
def icl_noticias_scrapy():
    res = Scrapy(verbose=False, 
                 site='ICL Notícias',
                 tag='Gerais', 
                 n_max=2,
                 espectro='left',
                 img_src='images/icl_logo.png',
                 url_site='https://iclnoticias.com.br/',
          ).run_scrapy()
    return res  
     
def agencia_basil_scrapy():
    res = Scrapy(verbose=False, 
                 site='Agência Brasil',
                 tag='Gerais', 
                 n_max=2,
                 espectro='center',
                 img_src='images/agencia_brasil_logo.png',
                 url_site='https://agenciabrasil.ebc.com.br/',
          ).run_scrapy()
    return res  

def bdf_scrapy():
    res = Scrapy(verbose=False, 
                 site='Brasil de Fato',
                 tag='Gerais', 
                 n_max=2,
                 espectro='left',
                 img_src='images/bdf_logo.png',
                 url_site='https://www.brasildefato.com.br/',
          ).run_scrapy()
    return res  

def carta_capital_scrapy():
    res = Scrapy(verbose=False, 
                 site='Carta Capital',
                 tag='Gerais', 
                 n_max=2,
                 espectro='left',
                 img_src='images/carta_capital_logo.png',
                 url_site='https://www.cartacapital.com.br/',
          ).run_scrapy()
    return res

def olhar_digital_scrapy():
    res = Scrapy(verbose=False, 
                 site='Olhar Digital',
                 tag='Tecnologia', 
                 n_max=2,
                 espectro='center',
                 img_src='images/olhar_digital_logo.png',
                 url_site='https://olhardigital.com.br/editorias/noticias/',
          ).run_scrapy()
    return res  

def poder360_scrapy():
    res = Scrapy(verbose=False, 
                 site='Poder 360',
                 tag='Gerais', 
                 n_max=2,
                 espectro='center',
                 img_src='images/poder_360_logo.png',
                 url_site='https://www.poder360.com.br/',
          ).run_scrapy()
    return res  

def uol_scrapy():
    res = Scrapy(verbose=False, 
                 site='UOL',
                 tag='Gerais', 
                 n_max=2,
                 espectro='right',
                 img_src='images/uol_logo.png',
                 url_site='https://www.uol.com.br/',
          ).run_scrapy()
    return res 

def g1_mundo_scrapy():
    res = Scrapy(verbose=False, 
                 site='G1-Mundo',
                 tag='Gerais', 
                 n_max=2,
                 espectro='right',
                 img_src='images/g1_logo.png',
                 url_site='https://g1.globo.com/mundo',
          ).run_scrapy()
    return res 

def canaltech_scrapy():
    res = Scrapy(verbose=False, 
                 site='Canaltech',
                 tag='Tecnologia', 
                 n_max=2,
                 espectro='right',
                 img_src='images/canaltech_logo.png',
                 url_site='https://canaltech.com.br/mais-lidas',
          ).run_scrapy()
    return res

def scrapy_each_site():
    t0 = time.time()
    print('\n>>> Carta Capital')
    try:    
        news_carta_capital = carta_capital_scrapy()
        print('>>> Carta Capital: done.')
    except:
        print('>>> Carta Capital: error.')
    
    jornal = 'ICL Notícias'
    print(f'\n>>> {jornal}')
    try:    
        news_icl = icl_noticias_scrapy()
        print(f'>>> {jornal}: done.')
    except:
        print(f'>>> {jornal}: error.')
    
    print('\n>>> Brasil de Fato')
    try:
        news_bdf = bdf_scrapy()
        print('>>> Brasil de Fato: done.')
    except:
        print('>>> Brasil de Fato: error.')
    print('\n>>> Agência Brasil')
    try:
        news_agencia_brasil = agencia_basil_scrapy()
        print('>>> Agência Brasil: done.')
    except:
        print('>>> Agência Brasil: error.')
        
    print('\n>>> Olhar Digital')
    try:
        news_olhar_digital = olhar_digital_scrapy()
        print('>>> Olhar Digital: done.')
    except:
        print('>>> Olhar Digital: error.')
    
    print('\n>>> Poder 360')
    try:
        news_poder360 = poder360_scrapy()
        print('>>> Poder 360: done.')
    except:
        print('>>> Poder 360: error.')
    
    print('\n>>> UOL ...')
    try:
        news_uol = uol_scrapy()
        print('>>> UOL: done.')
    except:
        print('>>> UOL: error.')
    
    print('\n>>> G1 ...')
    try:
        news_g1 = g1_mundo_scrapy()
        print('>>> G1: done.')
    except:
        print('>>> G1: error.')
    
    print('\n>>> Canaltech ...')
    try:
        news_canaltech = canaltech_scrapy()
        print('>>> CanalTech: done.')
    except:
        print('>>> CanalTech: error.')
    
    tempo_gasto = round(time.time() - t0, 2)
    print(f'\n>>> Tempo gasto: {tempo_gasto:.2f} s')
    return news_bdf, news_icl, news_agencia_brasil, news_poder360,\
            news_carta_capital, news_uol, news_g1, news_canaltech, news_olhar_digital,\
            tempo_gasto
