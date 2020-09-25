import sys
import pickle
import argparse
import datetime
import numpy as np 
import pandas as pd 

from os import path
from PIL import Image
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

import keras
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from sklearn.feature_extraction.text import CountVectorizer

from keras.callbacks import TensorBoard
from keras.utils.vis_utils import plot_model
from keras.utils.np_utils import to_categorical


def main():
    
    # ##################################     Arguments parser     ##################################
    parser = argparse.ArgumentParser() 
    parser.add_argument('--path' , default='data/uci-news-aggregator.csv', help='Path to dataset')
    args = parser.parse_args()
    
    print(args )
    
    # Load Dataset {1. data-analysis, 2. data-preprocessing}
    data = pd.read_csv(args.path, usecols=['TITLE', 'CATEGORY'])
    
    
    # ##################################     1. Data-Analysis     ##################################
    df = pd.read_csv('data/uci-news-aggregator.csv', usecols=['TITLE', 'CATEGORY'], encoding="utf-8")
    df['Categ']=df['CATEGORY'].apply(lambda x: 'Business' if x=='b' else 'Health' \
                               if x=='m' else 'Science/Tech' if x=='t' else 'Entertainment')
    print(df.head())
    print("There are {} observations and {} features in the dataset. \n".format(df.shape[0],df.shape[1]))
    print("There are {} News types in the dataset: {}  \n".format(len(df.CATEGORY.unique()),
                                                                               ", ".join(df.CATEGORY.unique() )))
    
    # Summary statistic of all countries
    country = df.groupby("Categ")
    print(country.describe().head())
    
    plt.figure(figsize=(10,7))
    country.size().sort_values(ascending=False).plot.bar()
    plt.xticks(rotation=50)
    plt.xlabel("news type")
    plt.ylabel("Number of articles")
    plt.savefig('saved/WCloud_Img/statistics.png', edgecolor='black')
    plt.show()
    
    # Remove stopwords
    stopwords = set(STOPWORDS)
    print('Stopwords', stopwords)

    # WordCloud
    print()
    print('WordClouds:')
    print('All categories')
    CLoudImage(df, '', 'white');print()
    print('Health')
    CLoudImage(df, 'm', 'pink');print()
    print('Science/Tech')
    CLoudImage(df, 't', 'coral');print()
    print('Business')
    CLoudImage(df , 'b', 'dimgray');print()
    print('Entertainment')
    CLoudImage(df, 'e','skyblue');print()
   
   
    # ##################################     2. Data-Preprocessing     ##################################
    num_of_categories = 50000
    shuffled = data.reindex(np.random.permutation(data.index))
    e = shuffled[shuffled['CATEGORY'] == 'e'][:num_of_categories]
    b = shuffled[shuffled['CATEGORY'] == 'b'][:num_of_categories]
    t = shuffled[shuffled['CATEGORY'] == 't'][:num_of_categories]
    m = shuffled[shuffled['CATEGORY'] == 'm'][:num_of_categories]
    concated = pd.concat([e,b,t,m], ignore_index=True)
    #Shuffle the dataset
    concated = concated.reindex(np.random.permutation(concated.index))
    concated['LABEL'] = 0
    #One-hot encode the lab
    concated.loc[concated['CATEGORY'] == 'e', 'LABEL'] = 0
    concated.loc[concated['CATEGORY'] == 'b', 'LABEL'] = 1
    concated.loc[concated['CATEGORY'] == 't', 'LABEL'] = 2
    concated.loc[concated['CATEGORY'] == 'm', 'LABEL'] = 3
    labels = to_categorical(concated['LABEL'], num_classes=4)

    if 'CATEGORY' in concated.keys():
        concated.drop(['CATEGORY'], axis=1)
      
    n_most_common_words = 8000
    max_len = 150
    tokenizer = Tokenizer(num_words=n_most_common_words, filters='!"#$%&()*+,-./:;<=>?@[\]^_`{|}~', lower=True)
    tokenizer.fit_on_texts(concated['TITLE'].values)
    sequences = tokenizer.texts_to_sequences(concated['TITLE'].values)
    word_index = tokenizer.word_index
    print('Found %s unique tokens.' % len(word_index))
    
    X = pad_sequences(sequences, maxlen=max_len)
    X_train, X_test, y_train, y_test = train_test_split(X , labels, test_size=0.25, random_state=42)

    # Save Data and Tokenizer as pickles
    #1. data
    with open('data/pickle_Xtest.pkl', 'wb') as file:
        pickle.dump(X_test, file)
    with open('data/pickle_ytest.pkl', 'wb') as file:
        pickle.dump(y_test, file)
    with open('data/pickle_Xtrain.pkl', 'wb') as file:
        pickle.dump(X_train, file)
    with open('data/pickle_ytrain.pkl', 'wb') as file:
        pickle.dump(y_train, file)
    print("Data has saved as pickle")

    #2. tokeninzer
    with open('data/tokenizer.pickle', 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
        
        
# ##################################     3. WordCloud-Method (print/save)     ##################################      
def CLoudImage(df, catg='', BckgrColor = 'white', Path='saved/WCloud_Img/' ):
    if (catg==''):
      text = df.TITLE.values
    else:
      text = df[df['CATEGORY']==catg ].TITLE.values
    wordcloud = WordCloud( width = 3000, height = 2000, background_color = BckgrColor, stopwords = STOPWORDS).generate(str(text))
    fig = plt.figure( figsize = (30, 20), facecolor = 'k', edgecolor = 'k')
 
    plt.imshow(wordcloud, interpolation = 'bilinear')
    plt.axis('off')
    plt.tight_layout(pad=4)
    plt.show()
    wordcloud.to_file(Path+"WordCloud_"+catg+'.png' )
        
        
        
# Main Method
if __name__ == "__main__":
    main()
