from textblob import TextBlob
from deep_translator import GoogleTranslator


## begin: sentiment analysis ##
#
# language translate
def language_translate(sentence, lang):
    try:
        translator = GoogleTranslator(source='auto', target=lang)
        translated = translator.translate(str(sentence))        
    except:
        translated = 'Error'
    
    return translated, lang.title()

# check subjectivity: very objective (0) or very subjective (1)
def check_subjectivity(score):
    if 0 <= score <= 0.4:
        sentiment = 'objetivo'
    elif 0.4 <= score < 0.6:
        sentiment = 'neutro'
    elif 0.6 <= score <= 1:
        sentiment = 'subjetivo'
    return sentiment

# check whether sentiment very positive (1), neutral(0) or very negative (-1)
def check_sentiment(score):
    if -0.5 <= score <= 0.5:
        sentiment = 'neutro'
    elif score > 0.5:
        sentiment = 'positivo'
    elif score < -0.5:
        sentiment = 'negativo'
    print(f'>> check_sentiment(): {(score, sentiment)}') 
    return sentiment


# sentence analysis
def sentence_analysis(sentence):
    # input: user sentence
    # output: score
    
    sentence_en, _ = language_translate(sentence, lang='en')
    
    score_tb = round(TextBlob(sentence_en).sentiment.polarity, 4)    
    sentiment_tb = check_sentiment(score_tb)
    score_subjectivity = round(TextBlob(sentence_en).sentiment.subjectivity, 4)
    subjectivity_tb = check_subjectivity(score_subjectivity)    

    res = {
        'score_tb': score_tb, 'score_subjectivity': score_subjectivity,
        'sentiment_tb': sentiment_tb, 'subjectivity_tb': subjectivity_tb        
    }
    return res
#
## end: sentiment analysis ##