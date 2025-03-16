# News Aggregator App

Collect news from some sources.

- Github repository: "https://github.com/msc2020/news-agg-app-dev"

- [https://news-agg-app.up.railway.app](https://news-agg-app.up.railway.app)


## About

- Make the scraping of some sites of news.

- Apply a machine learning sentiment analysis over each news.

- Link to access the original source.


```python
[[{'site': 'Brasil de Fato', 'title_news': 'Daniel Cara: redação do Enem está ultraexigente e servindo de propaganda para pré-vestibulares', 'url_news': 'https://www.brasildefato.com.br//2025/01/17/daniel-cara-redacao-do-enem-esta-ultraexigente-e-servindo-como-propaganda-para-cursos-pre-vestibulares', 'tag': 'Gerais', 'img_src': 'images/bdf_logo.png', 'raia': 'left', 'n_max': (1,), 'score_tb': 45, 'score_subjectivity': 10, 'sentiment_tb': 'neutro', 'subjectivity_tb': 'objetivo'}], [{'site': 'ICL Notícias', 'title_news': 'Vídeos mostram presos em presídio de MG sendo torturados por policiais penais', 'url_news': 'https://iclnoticias.com.br/videos-presos-em-presidio-de-mg-torturados/', 'tag': 'Gerais', 'img_src': 'images/icl_logo.png', 'raia': 'left', 'n_max': (1,), 'score_tb': 50, 'score_subjectivity': 0, 'sentiment_tb': 'neutro', 'subjectivity_tb': 'objetivo'}], [{'site': 'Agência Brasil', 'title_news': 'Apresentador Léo Batista morre no Rio de Janeiro, aos 92 anos', 'url_news': 'https://agenciabrasil.ebc.com.br//esportes/noticia/2025-01/apresentador-leo-batista-morre-no-rio-de-janeiro-aos-92-anos', 'tag': 'Gerais', 'img_src': 'images/agencia_brasil_logo.png', 'raia': 'center', 'n_max': (3,), 'score_tb': 45, 'score_subjectivity': 40, 'sentiment_tb': 'neutro', 'subjectivity_tb': 'objetivo'}, {'site': 'Agência Brasil', 'title_news': 'Pessoas desconhecem riscos ao escanear a íris, alertam especialistas', 'url_news': 'https://agenciabrasil.ebc.com.br//geral/noticia/2025-01/pessoas-desconhecem-riscos-ao-escanear-iris-alertam-especialistas', 'tag': 'Gerais', 'img_src': 'images/agencia_brasil_logo.png', 'raia': 'center', 'n_max': (3,), 'score_tb': 50, 'score_subjectivity': 50, 'sentiment_tb': 'neutro', 'subjectivity_tb': 'neutro'}, {'site': 'Agência Brasil', 'title_news': 'Caso Samarco: novo acordo não atrai e municípios focam em ação inglesa', 'url_news': 'https://agenciabrasil.ebc.com.br//geral/noticia/2025-01/caso-samarco-novo-acordo-nao-atrai-e-municipios-focam-em-acao-inglesa', 'tag': 'Gerais', 'img_src': 'images/agencia_brasil_logo.png', 'raia': 'center', 'n_max': (3,), 'score_tb': 53, 'score_subjectivity': 18, 'sentiment_tb': 'neutro', 'subjectivity_tb': 'objetivo'}], [{'site': 'Poder 360', 'title_news': 'Zambelli sofre acidente ao tentar pegar absorvente em avião', 'url_news': 'https://www.poder360.com.br/poder-brasil/zambelli-sofre-acidente-ao-tentar-pegar-absorvente-em-aviao/', 'tag': 'Gerais', 'img_src': 'images/poder_360_logo.png', 'raia': 'center', 'n_max': (1,), 'score_tb': 20, 'score_subjectivity': 70, 'sentiment_tb': 'negativo', 'subjectivity_tb': 'subjetivo'}], [{'site': 'Carta Capital', 'title_news': 'EUA se retirarão do Acordo de Paris e aumentarão a produção de\xa0hidrocarbonetos', 'url_news': 'https://www.cartacapital.com.br/mundo/governo-trump-afirma-que-eua-vao-se-retirar-do-acordo-de-paris/', 'tag': 'Gerais', 'img_src': 'images/carta_capital_logo.png', 'raia': 'left', 'n_max': (2,), 'score_tb': 50, 'score_subjectivity': 0, 'sentiment_tb': 'neutro', 'subjectivity_tb': 'objetivo'}, {'site': 'Carta Capital', 'title_news': 'Justiça isenta Pablo Marçal de pagar promessa de 1 milhão de dólares', 'url_news': 'https://www.cartacapital.com.br/cartaexpressa/justica-isenta-pablo-marcal-de-pagar-promessa-de-1-milhao-de-dolares/', 'tag': 'Gerais', 'img_src': 'images/carta_capital_logo.png', 'raia': 'left', 'n_max': (2,), 'score_tb': 50, 'score_subjectivity': 0, 'sentiment_tb': 'neutro', 'subjectivity_tb': 'objetivo'}], [{'site': 'UOL', 'title_news': 'Loja de carros de luxo em MG fecha e causa prejuízo milionário aos clientes', 'url_news': 'https://www.uol.com.br/carros/noticias/redacao/2025/01/20/loja-de-carros-de-luxo-fecha-e-causa-prejuizo-milionario-aos-clientes.htm', 'tag': 'Gerais', 'img_src': 'images/uol_logo.png', 'raia': 'right', 'n_max': (2,), 'score_tb': 50, 'score_subjectivity': 0, 'sentiment_tb': 'neutro', 'subjectivity_tb': 'objetivo'}, {'site': 'UOL', 'title_news': 'Trump não coloca a mão na Bíblia durante o juramento de posse; siga', 'url_news': 'https://noticias.uol.com.br/ao-vivo/2025/01/20/posse-trump-ao-vivo-presidente-eua.htm', 'tag': 'Gerais', 'img_src': 'images/uol_logo.png', 'raia': 'right', 'n_max': (2,), 'score_tb': 50, 'score_subjectivity': 0, 'sentiment_tb': 'neutro', 'subjectivity_tb': 'objetivo'}], [{'site': 'G1-Mundo', 'title_news': 'Gesto de Musk gera polêmica durante fala do bilionário em evento da posse de Trump', 'url_news': 'https://g1.globo.com/mundo/video/gesto-de-musk-gera-polemica-durante-fala-do-bilionario-em-evento-da-posse-de-trump-13274016.ghtml', 'tag': 'Gerais', 'img_src': 'images/g1_logo.png', 'raia': 'right', 'n_max': (1,), 'score_tb': 50, 'score_subjectivity': 0, 'sentiment_tb': 'neutro', 'subjectivity_tb': 'objetivo'}], [{'site': 'Canaltech', 'title_news': 'Review Echo Spot 2 | Um relógio de cabeceira com Alexa', 'url_news': 'https://canaltech.com.br/mais-lidas/assistente-virtual/analise/review-echo-spot-um-relogio-de-cabeceira-com-alexa/', 'tag': 'Tecnologia', 'img_src': 'images/canaltech_logo.png', 'raia': 'right', 'n_max': (3,), 'score_tb': 50, 'score_subjectivity': 0, 'sentiment_tb': 'neutro', 'subjectivity_tb': 'objetivo'}, {'site': 'Canaltech', 'title_news': 'Review Realme GT 7 Pro | Chegou a hora de dar uma chance aos flagships da marca?', 'url_news': 'https://canaltech.com.br/mais-lidas/produto/realme/gt-7-pro/analise/', 'tag': 'Tecnologia', 'img_src': 'images/canaltech_logo.png', 'raia': 'right', 'n_max': (3,), 'score_tb': 50, 'score_subjectivity': 0, 'sentiment_tb': 'neutro', 'subjectivity_tb': 'objetivo'}, {'site': 'Canaltech', 'title_news': 'Review Mi Band 9 | Será que vale a pena comprar a smartband da Xiaomi?', 'url_news': 'https://canaltech.com.br/mais-lidas/produto/xiaomi/smart-band-9/analise/', 'tag': 'Tecnologia', 'img_src': 'images/canaltech_logo.png', 'raia': 'right', 'n_max': (3,), 'score_tb': 65, 'score_subjectivity': 10, 'sentiment_tb': 'neutro', 'subjectivity_tb': 'objetivo'}], [{'site': 'G1-Tecnologia', 'title_news': 'A trajetória de Elon Musk', 'url_news': 'https://g1.globo.com/tecnologia/noticia/2025/01/20/a-trajetoria-de-elon-musk.ghtml', 'tag': 'Tecnologia', 'img_src': 'images/g1_logo.png', 'raia': 'left', 'n_max': (3,), 'score_tb': 50, 'score_subjectivity': 0, 'sentiment_tb': 'neutro', 'subjectivity_tb': 'objetivo'}, {'site': 'G1-Tecnologia', 'title_news': 'Gesto de Musk gera polêmica durante fala do bilionário em evento da posse de Trump', 'url_news': 'https://g1.globo.com/tecnologia/noticia/2025/01/20/musk-cita-marte-em-evento-de-trump-e-diz-que-futuro-da-civilizacao-esta-garantido.ghtml', 'tag': 'Tecnologia', 'img_src': 'images/g1_logo.png', 'raia': 'left', 'n_max': (3,), 'score_tb': 50, 'score_subjectivity': 0, 'sentiment_tb': 'neutro', 'subjectivity_tb': 'objetivo'}, {'site': 'G1-Tecnologia', 'title_news': "'America is back': site da Casa Branca muda e passa a exaltar Trump", 'url_news': 'https://g1.globo.com/mundo/noticia/2025/01/20/america-is-back-site-da-casa-branca-muda-e-passa-a-exaltar-trump.ghtml', 'tag': 'Tecnologia', 'img_src': 'images/g1_logo.png', 'raia': 'left', 'n_max': (3,), 'score_tb': 50, 'score_subjectivity': 0, 'sentiment_tb': 'neutro', 'subjectivity_tb': 'objetivo'}]]
```