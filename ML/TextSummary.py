import re
import nltk
import heapq
import bs4 as bs
import numpy as np
import urllib.request


def TxtSummary(sentence):
        
    Is_Link = sentence[0:5].lower()=="https"
    if(not Is_Link):
        print("Input-type: 'Text'")
        article_text=sentence

        
    else:    
        print("Input-type: 'Link':")
        scraped_data = urllib.request.urlopen(sentence)
        article = scraped_data.read()
        
        parsed_article = bs.BeautifulSoup(article,'lxml')
        paragraphs = parsed_article.find_all('p')
        
        article_text = ""
        for p in paragraphs:
            article_text += p.text  
            
    rows=int(len(article_text.split('.'))/4)+1
        
    
    # Removing Square Brackets and Extra Spaces
    article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
    article_text = re.sub(r'\s+', ' ', article_text)
    # Removing special characters and digits
    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)  
    sentence_list = nltk.sent_tokenize(article_text)

    stopwords = nltk.corpus.stopwords.words('english')

    word_frequencies = {}
    for word in nltk.word_tokenize(formatted_article_text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
                
    maximum_frequncy = max(word_frequencies.values())
    
    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)        

    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 40:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]
                else:
                    print("Two many characters for sentence:",sent)
                    print()
                    break
    print()
    #rows=int(len(sentence_scores)/4)+1 #25% of the text
    total=np.round(sum(sentence_scores.values()),rows)
    print('25% of text: '+str(rows)+'/'+str(rows) )
    print('Total score:', total, sentence_scores.values())
    
    summary_sentences = heapq.nlargest(rows, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)

    return summary ,  sentence_scores

def DataProcess(summry, scores):
    s=''
    for sc in scores:
        if(sc.lower() in  summry.lower()):
            s=s+' '+sc
    return s

