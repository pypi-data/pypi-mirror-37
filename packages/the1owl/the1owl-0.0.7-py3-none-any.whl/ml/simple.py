import scipy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn import metrics
from sklearn import feature_extraction
from multiprocessing import Pool, cpu_count

#define metric
#create a common evaluation function passthrough for all models

class Data(object):
    def __init__(self, TRAIN, TEST, ID, TARGET, PREPROCESSING_PARAMS={}):
        if 'drop' in PREPROCESSING_PARAMS:
            TRAIN.drop(columns=PREPROCESSING_PARAMS['drop'], inplace=True)
            TEST.drop(columns=PREPROCESSING_PARAMS['drop'], inplace=True)
            print("Columns " + ' '.join(map(str, PREPROCESSING_PARAMS['drop'])))

        if 'fillna' in PREPROCESSING_PARAMS:
           col = [c for c in TRAIN.columns if c not in [ID, TARGET]]
           imp = PREPROCESSING_PARAMS['fillna']
           for c in col:
               if PREPROCESSING_PARAMS['fillna'] == 'mean':
                   imp = np.mean(TRAIN[c])
               if PREPROCESSING_PARAMS['fillna'] == 'median':
                   imp = np.median(TRAIN[c])

               TRAIN[c].fillna(imp, inplace=True)
               TEST[c].fillna(imp, inplace=True)
           print("fillna complete")

        self.TRAIN = TRAIN
        self.TEST = TEST
        self.ID = ID
        self.TARGET = TARGET

class Model(object):
    def __init__(self, DATA, MODEL='ETR', PARAMS={}, TEST_SIZE = 0.25, RANDOM_STATE=5):
        from sklearn import  model_selection
        col = [c for c in DATA.TRAIN.columns if c not in [DATA.ID,DATA.TARGET]]
        X1, X2, Y1, Y2 =  model_selection.train_test_split(DATA.TRAIN[col], DATA.TRAIN[DATA.TARGET], test_size=TEST_SIZE, random_state=RANDOM_STATE)
        if MODEL in ['ETR']:
            from sklearn import ensemble
            LIB = ensemble.ExtraTreesRegressor(n_jobs=-1, random_state = RANDOM_STATE)
            PARAMS_ = LIB.get_params()
            for p in PARAMS:
                if p in PARAMS_:
                    LIB.set_params({p: PARAMS[p]})
            LIB.fit(DATA.TRAIN[col], DATA.TRAIN[DATA.TARGET])
            DATA.TEST[DATA.TARGET] = LIB.predict(DATA.TEST[col])
            self.PRED = DATA.TEST[[DATA.ID, DATA.TARGET]]
        elif MODEL in ['XGB']:
            import xgboost as xgb
            default_params = {'num_round': 20, 'verbose_eval': 10, 'early_stopping_rounds': 20}

            if PARAMS == {}:
                PARAMS = {'eta': 0.2, 'max_depth': 4, 'objective': 'reg:linear', 'eval_metric': 'rmse', 'seed': RANDOM_STATE, 'silent': True, 'num_round': 20, 'verbose_eval': 10, 'early_stopping_rounds': 20}
            if 'num_round' in PARAMS:
                default_params['num_round'] = PARAMS['num_round'] 
            if 'verbose_eval' in PARAMS:
                default_params['verbose_eval'] = PARAMS['verbose_eval'] 
            if 'early_stopping_rounds' in PARAMS:
                default_params['early_stopping_rounds'] = PARAMS['early_stopping_rounds'] 

            def xgb_rmse(preds, y):
                y = y.get_label()
                score = np.sqrt(metrics.mean_squared_error(y, preds))
                return 'RMSE', score

            watchlist = [(xgb.DMatrix(X1, Y1), 'train'), (xgb.DMatrix(X2, Y2), 'valid')] 
            eval_str = "xgb.train(PARAMS, xgb.DMatrix(X1, Y1), " + str(default_params['num_round']) + ",  watchlist, verbose_eval=" + str(default_params['verbose_eval']) + ", early_stopping_rounds=" + str(default_params['early_stopping_rounds']) + ")" #feval=xgb_rmse, maximize=False
            LIB = eval(eval_str)
            DATA.TEST[DATA.TARGET] = LIB.predict(xgb.DMatrix(DATA.TEST[col]), ntree_limit=LIB.best_ntree_limit)
            self.PRED = DATA.TEST[[DATA.ID, DATA.TARGET]].copy()

        elif MODEL in ['LGB']:
            import lightgbm as lgb
            default_params = {'verbose_eval': 10}

            if PARAMS == {}:
                PARAMS = {'learning_rate': 0.2, 'max_depth': 7, 'boosting': 'gbdt', 'objective': 'regression', 'metric':'rmse', 'seed': RANDOM_STATE, 'num_iterations': 100, 'early_stopping_round': 20}
            if 'verbose_eval' in PARAMS:
                default_params['verbose_eval'] = PARAMS['verbose_eval']

            def lgb_rmse(preds, y):
                y = np.array(list(y.get_label()))
                score = np.sqrt(metrics.mean_squared_error(y, preds))
                return 'RMSE', score, False

            eval_str = "lgb.train(PARAMS, lgb.Dataset(X1, label=Y1), valid_sets=lgb.Dataset(X2, label=Y2), verbose_eval=" + str(default_params['verbose_eval']) + ")" #feval=lgb_rmse
            LIB = eval(eval_str)
            DATA.TEST[DATA.TARGET] = LIB.predict(DATA.TEST[col], num_iteration=LIB.best_iteration)
            self.PRED = DATA.TEST[[DATA.ID, DATA.TARGET]].copy()

        elif MODEL in ['CB']:
            from catboost import CatBoostRegressor

            LIB = CatBoostRegressor(iterations=100, learning_rate=0.2, depth=7, loss_function='RMSE', eval_metric='RMSE', random_seed=RANDOM_STATE, od_type='Iter', od_wait=20) 
            LIB.fit(X1, Y1, eval_set=(X2, Y2), use_best_model=True, verbose=False)
            DATA.TEST[DATA.TARGET] = LIB.predict(DATA.TEST[col])
            self.PRED = DATA.TEST[[DATA.ID, DATA.TARGET]].copy()

        else:
            DATA.TEST[DATA.TARGET] = np.median(DATA.TRAIN[DATA.TARGET])
            self.PRED = DATA.TEST[[DATA.ID, DATA.TARGET]].copy()

class Blend(object):
    def __init__(self, FILES=[], ID='id', TARGET='target', NAME='blend01.csv'):
        FILES_ = []
        i = 1
        for f in FILES:
            df = pd.read_csv(f, index_col=[ID]).rename(columns={TARGET:'dp' + str(i)})
            FILES_.append(df)
            i += 1
        df = pd.concat(FILES_, sort=False, axis=1)
        df[TARGET] = df.sum(axis=1)
        df[TARGET] /= len(FILES_)
        self.BLEND = df
        BLEND = df[[TARGET]]
        BLEND.to_csv(NAME)
