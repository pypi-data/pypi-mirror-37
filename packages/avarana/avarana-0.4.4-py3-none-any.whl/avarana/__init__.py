# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 13:06:35 2018

@author: hrajiv
"""
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Embedding
from keras.layers import LSTM
import pandas as pd
import sys
import numpy as np
import xgboost
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.metrics import explained_variance_score
from eli5.permutation_importance import get_score_importances
from sklearn.model_selection import GridSearchCV

name='avarana'

def parser(x):
	return pd.datetime.strptime(x, '%Y%m%d')

def lag(array, start_index, end_index, lag):
    lag_start_index = start_index-lag
    lag_end_index = end_index-lag
    return array[lag_start_index:lag_end_index]

def mean_absolute_percentage_error(y_true, y_pred): 
    y_true[y_true==0] = y_true[y_true>0].min() 
    h1 = np.abs(y_true - y_pred)
    h2 = np.divide(h1, y_true)
    return np.mean(h2)

def tf_mape(y_true, y_pred):
    y_true[y_true==0] = y_true[y_true>0].min() 
    h1 = np.abs(y_true - y_pred)
    h2 = np.divide(h1, y_true)
    return np.mean(h2)

def weighted_absolute_percentage_error(y_true, y_pred): 
    return np.abs(y_true - y_pred).sum()/y_true.sum()

def nnet_regressor(X, y, X_test=[], y_test=[], hidden_layers=[],
                   activation='relu', loss='mape', verbose=0):
    if type(hidden_layers) is not list:
        print("Hidden layers must be a list")
        sys.exit(0)
        
    model = Sequential()
    
    if len(hidden_layers) > 0 and np.sum(hidden_layers) > 0:
        first_layer = 0
        for layer_size in hidden_layers:
            if layer_size > 0 and first_layer == 0:
                model.add(Dense(layer_size, input_dim=X.shape[1], activation='linear'))
                first_layer = 1
            elif layer_size > 0:
                model.add(Dense(layer_size, activation='relu'))
        model.add(Dense(1, activation='linear')) #hard coded to 1 output layer
    else:
        model.add(Dense(1, input_dim=X.shape[1], activation='linear')) #hard coded to 1 output layer

    model.compile(loss=loss, optimizer='rmsprop')

    def scorer(X, y):
        y_pred = model.predict(X)
        return 1-mean_absolute_percentage_error(y, y_pred)    
    
#    gsc = GridSearchCV(
#        estimator=model,
#        param_grid={
#            #'neurons': range(18,31,4),
#            'noise': [x/20.0 for x in range(3, 7)],
#        },
#        scoring='neg_absolute_error',
#        cv=5
#    )   
    
    
    
#    last_min_mape = 100
#    last_min_layer = []
#    
#    hidden_layers = []
#    for h in range(0,X.shape[1]):
#        hidden_layers.append(0)
#        for i in range(0,len(X)+1): 
#            hidden_layers[h] = i
#            model, predictions, mape = manthan_nnet(X,Y,X_test,test,hidden_layers)
#            if mape < last_min_mape:
#                last_min_layer = hidden_layers
#                last_min_mape = mape
#    
#    print('Min layer size = ',last_min_layer, ' last min MAPE= ', last_min_mape)
    
    model.fit(X.values, y.values, batch_size=round(len(y)/2), epochs=500, verbose=verbose)
    
    if verbose > 0:
        base_score, score_decreases = get_score_importances(scorer, X_test.values, y_test.values)
        feature_importances = np.mean(score_decreases, axis=0)
        abs_feature_importances = np.abs(feature_importances )
        feature_importances_table = pd.DataFrame(np.transpose([X.columns, feature_importances, abs_feature_importances]), 
                                                 columns=['Feature','Score', 'Abs Score'])
        print(feature_importances_table.sort_values('Abs Score', ascending=False)) 
    
#    Set defaults if there is no test period in the inputs
    predictions = []
    mape = 0
    
    if len(X_test) > 0:
        predictions = model.predict(X_test).ravel()
        
        error = mean_squared_error(y_test.values, predictions)
        mape = mean_absolute_percentage_error(y_test.values, predictions)
        wape = weighted_absolute_percentage_error(y_test.values, predictions)
        r2 = r2_score(y_test.values, predictions)
        if verbose > 0:
            print('Hidden layers: ',hidden_layers,' R2: %.3f Test MSE: %.3f ~MAPE: %.6f WAPE: %.3f' % (r2, error, mape, wape))    
    
    return model, predictions, mape;

# define base model
def baseline_model():
	# create model
	model = Sequential()
	model.add(Dense(5, input_dim=5, kernel_initializer='normal', activation='relu'))
	model.add(Dense(1, kernel_initializer='normal'))
	# Compile model
	model.compile(loss='mean_squared_error', optimizer='adam')
	return model

# XGB Configuration
def xgb_regressor(X, Y, X_test, Y_test):
    xgb = xgboost.XGBRegressor(n_estimators=100, 
                           learning_rate=0.1, 
                           gamma=0.1, 
                           subsample=0.8,
                           colsample_bytree=0.75, 
                           max_depth=3,
                           min_child_weight=1)

    xgb.fit(X.values,Y.values)
    
    param_test1 = {
     'max_depth':range(3,100,2),
     'min_child_weight':range(1,6,2)
#     'learning_rate':np.arange(0.1,1,0.1),
#     'gamma':[i/10.0 for i in range(0,5)],
#     'subsample':[i/10.0 for i in range(6,10)],
#     'colsample_bytree':[i/10.0 for i in range(6,10)]
     }

    gsearch1 = GridSearchCV(estimator = xgb, 
                        param_grid = param_test1, 
                        n_jobs=1,iid=False, 
                        cv=5)

    gsearch1.fit(X.values,Y.values)

    print('Grid Score')
    print(gsearch1.grid_scores_)
    print('Best params')
    print(gsearch1.best_params_)
    print('Best Score')
    print(gsearch1.best_score_)
    
    predictions = xgb.predict(X_test.values)
    mape = mean_absolute_percentage_error(Y_test.values, predictions)
    evs = explained_variance_score(predictions, Y_test.values)
    return xgb, predictions, mape, evs

def lstm_regressor(X, Y, X_test, Y_test):
    max_features = 1024
    
    model = Sequential()
    model.add(Embedding(max_features, output_dim=256))
    model.add(LSTM(128))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))
    
    model.compile(loss='mape',
                  optimizer='rmsprop',
                  metrics=['accuracy'])
    
    model.fit(x_train, y_train, batch_size=16, epochs=10)
    score = model.evaluate(x_test, y_test, batch_size=16)