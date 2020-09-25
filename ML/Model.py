import sys
import argparse
import datetime
import numpy as np 
import pandas as pd  


import keras

from keras.models import Sequential
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from sklearn.feature_extraction.text import CountVectorizer
from keras.layers import Dense, Embedding, LSTM, SpatialDropout1D, GRU


from keras.callbacks import EarlyStopping
from keras.utils.np_utils import to_categorical
from sklearn.model_selection import train_test_split


from keras.models import load_model
from keras.callbacks import TensorBoard
from keras.utils.vis_utils import plot_model


def main():
    
    parser = argparse.ArgumentParser() 
    parser.add_argument('--path' , default='data/uci-news-aggregator.csv', help='Path to dataset')
    parser.add_argument('--layer' , default='lstm', help='lSTM or GRU training layer')
    parser.add_argument('--epochs' , type=int, default=8, help='lSTM or GRU training layer')
    
    args = parser.parse_args()
    
    print('model_'+args.layer+'_Ep'+str(args.epochs)+'.h5')
    print(args, args.layer, len(sys.argv)   )
    
    # Load Dataset
    data = pd.read_csv(args.path, usecols=['TITLE', 'CATEGORY'])
    print(data.CATEGORY.value_counts())
   
   
    #I do aspire here to have balanced classes
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
    print(concated['LABEL'][:10])
    labels = to_categorical(concated['LABEL'], num_classes=4)
    print(labels[:10])
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
    
    #Start training
    X_train, X_test, y_train, y_test = train_test_split(X , labels, test_size=0.25, random_state=42)
    epochs = args.epochs; emb_dim = 128; batch_size = 256
    print(labels[:2])
    
    log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    tensorboard_callback = keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)
    
    
    print((X_train.shape, y_train.shape, X_test.shape, y_test.shape))
    
    model = Sequential()
    model.add(Embedding(n_most_common_words, emb_dim, input_length=X.shape[1]))
    model.add(SpatialDropout1D(0.7))
    
    if(not args.layer.lower()=='lstm'):
        print('GRU MODEL')
        model.add(GRU(64, dropout=0.7, recurrent_dropout=0.7))
    else:
        print('LSTM MODEL')
        model.add(LSTM(64, dropout=0.7, recurrent_dropout=0.7))
    
    model.add(Dense(4, activation='softmax'))
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['acc'])
    
    print(model.summary()); print()
    #plot_model(model, to_file='model_plot_'+args.layer+'.png', show_shapes=True, show_layer_names=True)
    
    history = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, \
    validation_split=0.2,callbacks=[EarlyStopping(monitor='val_loss',patience=7, min_delta=0.0001), tensorboard_callback])
    
    model.save('model_'+args.layer+'_Ep'+str(args.epochs)+'.h5')  # creates a HDF5 file 'my_model.h5'

    
    
if __name__ == "__main__":
    main()
