import sys
import pickle
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
    
    
    # ##################################     Arguments parser     ##################################
    parser = argparse.ArgumentParser() 
    parser.add_argument('--path' , default='data/uci-news-aggregator.csv', help='Path to dataset')
    parser.add_argument('--layer' , default='lstm', help='lSTM or GRU training layer')
    parser.add_argument('--epochs' , type=int, default=8, help='lSTM or GRU training layer')
    args = parser.parse_args()
    
    print('model_'+args.layer+'_Ep'+str(args.epochs)+'.h5')
    print(args, args.layer, len(sys.argv)   )
    

    # ##################################     1. Data Loading     ##################################
    
    # Load data from pickle file
    with open("data/pickle_Xtrain.pkl", 'rb') as file:
        pkl_X_train = pickle.load(file)
    with open("data/pickle_ytrain.pkl", 'rb') as file:
        pkl_y_train = pickle.load(file)
    with open("data/pickle_Xtest.pkl", 'rb') as file:
        pkl_X_test = pickle.load(file)
    with open("data/pickle_ytest.pkl", 'rb') as file:
        pkl_y_test = pickle.load(file)
     
    X_test=pkl_X_test; y_test=pkl_y_test;   
    X_train=pkl_X_train; y_train=pkl_y_train;
    
    # Load tokenizer from pickle file
    with open('data/tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
        
        
    print("Data:", (X_train.shape, y_train.shape, X_test.shape, y_test.shape))
    
    
 

    # ##################################     2. Training     ##################################
    emb_dim = 128; batch_size = 256; n_most_common_words = 8000; epochs=args.epochs
    
    # TensorBoard
    today = datetime.date.today()
    log_dir = "logs/fit/" + 'model_'+args.layer+'_Ep'+str(args.epochs)+'('+str(today)+')'
    tensorboard_callback = keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)
    print("Tensorboard:",log_dir); print()
    
    
    # Model defining
    model = Sequential()
    model.add(Embedding(n_most_common_words, emb_dim, input_length=X_train.shape[1]))
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
    plot_model(model, to_file='saved/model_plot_'+args.layer+'_Ep'+str(args.epochs)+'.png', show_shapes=True, show_layer_names=True)
    
    history = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, \
    validation_split=0.2,callbacks=[EarlyStopping(monitor='val_loss',patience=7, min_delta=0.0001), tensorboard_callback])
    
    
    
    # ##################################     3. Save Model     ##################################
    model.save('saved/model_'+args.layer+'_Ep'+str(args.epochs)+'.h5')  # creates a HDF5 file 'my_model.h5'

    
    
if __name__ == "__main__":
    main()
