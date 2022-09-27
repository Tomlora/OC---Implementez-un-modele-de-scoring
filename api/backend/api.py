from fastapi import FastAPI
import uvicorn
import pickle
from sklearn.metrics import confusion_matrix, make_scorer
import pandas as pd
import lightgbm
import numpy as np
import json
from fonction import cout_metier

app = FastAPI(title='API for OpenClassroom', description='Prediction bancaire')

# ---------------------- Data

url_data = './data/data.pkl'

with open(url_data, 'rb') as f:
    fichier = pickle.load(f)
       
# ---------------------- Pipeline


# corrige l'erreur d'uvicorn qui ne reconnait pas la fonction cout_metier
class CustomUnpickler(pickle.Unpickler):

    def find_class(self, module, name):
        if name == 'cout_metier':
            from fonction import cout_metier
            return cout_metier
        return super().find_class(module, name)


metric_custom = make_scorer(cout_metier)

url_pipeline = './pipeline/pipeline_perso_random_iter50.pkl'
pipe = CustomUnpickler(open(url_pipeline, 'rb')).load()
# pipe = pickle.load(open(url_pipeline, 'rb'))

# pipe.best_estimator_[0].transform utilisation d'iterativeimputer

def predict(dict):
    # si on a déjà predict, la valeur est retenue, donc :
    if len(dict) >= 41:
        del dict['PROBABILITY']
        
    df = pd.DataFrame.from_dict(dict, orient="index")
    df = df.transpose()
    df = df.replace('Indisp', None)
    proba = pipe.predict_proba(df)[:,1] # Probabilité de remboursement
    proba = round(np.array(proba)[0],2)
    return proba

# Fonction de correction

def isNan(num):
    return num != num


def format_json(data_dict):
    
    data_copy = data_dict.copy()
    
    
    for key in data_copy.keys():
        if isNan(data_copy[key]):
            data_copy[key] = 'Indisp'
            
    
    return data_copy
    
 
@app.get('/client/{client_id}')
async def infos_client(client_id:int):
    fichier[client_id]['PROBABILITY'] = predict(fichier[client_id])
    
    data = format_json(fichier[client_id])
    
    return data

@app.get('/client/probability/{client_id}')
async def predict_probability(client_id:int):
    proba = predict(fichier[client_id])
    
    
    return {'result' : proba}

@app.get('/client/all/')
async def client_all():
    
    return json.dumps(list(fichier.keys()))



@app.get('/client/new/')
async def new_client(PAYMENT_RATE:float=None,
                     EXT_SOURCE_1:float=None,
                     EXT_SOURCE_2:float=None,
                     EXT_SOURCE_3:float=None,
                     DAYS_BIRTH:float=None,
                     AMT_ANNUITY:float=None,
                     DAYS_EMPLOYED:float=None,
                     APPROVED_CNT_PAYMENT_MEAN:float=None,
                     DAYS_ID_PUBLISH:float=None,
                     INCOME_CREDIT_PERC:float=None,
                     ACTIVE_DAYS_CREDIT_MAX:float=None,
                     INSTAL_DAYS_ENTRY_PAYMENT_MAX:float=None,
                     INSTAL_DPD_MEAN:float=None,
                     DAYS_REGISTRATION:float=None,
                     DAYS_EMPLOYED_PERC:float=None,
                     ACTIVE_DAYS_CREDIT_ENDDATE_MIN:float=None,
                     AMT_CREDIT:float=None,
                     PREV_CNT_PAYMENT_MEAN:float=None,
                     AMT_GOODS_PRICE:float=None,
                     INSTAL_AMT_PAYMENT_SUM:float=None,
                     REGION_POPULATION_RELATIVE:float=None,
                     INSTAL_DBD_SUM:float=None,
                     DAYS_LAST_PHONE_CHANGE:float=None,
                     BURO_AMT_CREDIT_MAX_OVERDUE_MEAN:float=None,
                     CLOSED_DAYS_CREDIT_MAX:float=None,
                     OWN_CAR_AGE:int=None,
                     CLOSED_DAYS_CREDIT_ENDDATE_MAX:float=None,
                     APPROVED_DAYS_DECISION_MAX:float=None,
                     POS_MONTHS_BALANCE_SIZE:float=None,
                     ACTIVE_AMT_CREDIT_SUM_SUM:float=None,
                     ACTIVE_DAYS_CREDIT_UPDATE_MEAN:float=None,
                     BURO_DAYS_CREDIT_MAX:float=None,
                     BURO_DAYS_CREDIT_ENDDATE_MAX:float=None,
                     INSTAL_AMT_PAYMENT_MIN:float=None,
                     ACTIVE_DAYS_CREDIT_ENDDATE_MAX:float=None,
                     ACTIVE_DAYS_CREDIT_MEAN:float=None,
                     INSTAL_DBD_MAX:float=None,
                     CLOSED_AMT_CREDIT_SUM_MEAN:float=None,
                     BURO_AMT_CREDIT_SUM_DEBT_MEAN:float=None,
                     ACTIVE_DAYS_CREDIT_ENDDATE_MEAN:float=None):
    
    data = {
  "PAYMENT_RATE": PAYMENT_RATE,
  "EXT_SOURCE_1": EXT_SOURCE_1,
  "EXT_SOURCE_2": EXT_SOURCE_2,
  "EXT_SOURCE_3": EXT_SOURCE_3,
  "DAYS_BIRTH": DAYS_BIRTH,
  "AMT_ANNUITY": AMT_ANNUITY,
  "DAYS_EMPLOYED": -DAYS_EMPLOYED,
  "APPROVED_CNT_PAYMENT_MEAN": APPROVED_CNT_PAYMENT_MEAN,
  "DAYS_ID_PUBLISH": -DAYS_ID_PUBLISH,
  "INCOME_CREDIT_PERC": INCOME_CREDIT_PERC,
  "ACTIVE_DAYS_CREDIT_MAX": -ACTIVE_DAYS_CREDIT_MAX,
  "INSTAL_DAYS_ENTRY_PAYMENT_MAX": -INSTAL_DAYS_ENTRY_PAYMENT_MAX,
  "INSTAL_DPD_MEAN": INSTAL_DPD_MEAN,
  "DAYS_REGISTRATION": -DAYS_REGISTRATION,
  "DAYS_EMPLOYED_PERC": DAYS_EMPLOYED_PERC,
  "ACTIVE_DAYS_CREDIT_ENDDATE_MIN": -ACTIVE_DAYS_CREDIT_ENDDATE_MIN,
  "AMT_CREDIT": AMT_CREDIT,
  "PREV_CNT_PAYMENT_MEAN": PREV_CNT_PAYMENT_MEAN,
  "AMT_GOODS_PRICE": AMT_GOODS_PRICE,
  "INSTAL_AMT_PAYMENT_SUM": INSTAL_AMT_PAYMENT_SUM,
  "REGION_POPULATION_RELATIVE": REGION_POPULATION_RELATIVE,
  "INSTAL_DBD_SUM": INSTAL_DBD_SUM,
  "DAYS_LAST_PHONE_CHANGE": -DAYS_LAST_PHONE_CHANGE,
  "BURO_AMT_CREDIT_MAX_OVERDUE_MEAN": BURO_AMT_CREDIT_MAX_OVERDUE_MEAN,
  "CLOSED_DAYS_CREDIT_MAX": -CLOSED_DAYS_CREDIT_MAX,
  "OWN_CAR_AGE": OWN_CAR_AGE,
  "CLOSED_DAYS_CREDIT_ENDDATE_MAX": -CLOSED_DAYS_CREDIT_ENDDATE_MAX,
  "APPROVED_DAYS_DECISION_MAX": -APPROVED_DAYS_DECISION_MAX,
  "POS_MONTHS_BALANCE_SIZE": POS_MONTHS_BALANCE_SIZE,
  "ACTIVE_AMT_CREDIT_SUM_SUM": ACTIVE_AMT_CREDIT_SUM_SUM,
  "ACTIVE_DAYS_CREDIT_UPDATE_MEAN": -ACTIVE_DAYS_CREDIT_UPDATE_MEAN,
  "BURO_DAYS_CREDIT_MAX": -BURO_DAYS_CREDIT_MAX,
  "BURO_DAYS_CREDIT_ENDDATE_MAX": -BURO_DAYS_CREDIT_ENDDATE_MAX,
  "INSTAL_AMT_PAYMENT_MIN": INSTAL_AMT_PAYMENT_MIN,
  "ACTIVE_DAYS_CREDIT_ENDDATE_MAX": -ACTIVE_DAYS_CREDIT_ENDDATE_MAX,
  "ACTIVE_DAYS_CREDIT_MEAN": -ACTIVE_DAYS_CREDIT_MEAN,
  "INSTAL_DBD_MAX": INSTAL_DBD_MAX,
  "CLOSED_AMT_CREDIT_SUM_MEAN": CLOSED_AMT_CREDIT_SUM_MEAN,
  "BURO_AMT_CREDIT_SUM_DEBT_MEAN": BURO_AMT_CREDIT_SUM_DEBT_MEAN,
  "ACTIVE_DAYS_CREDIT_ENDDATE_MEAN": -ACTIVE_DAYS_CREDIT_ENDDATE_MEAN
    }
                
    proba = predict(data)
       
    return {'result' : proba}

@app.get('/client/client_avg/')
async def moyenne_client(remboursement:bool):
    # probability
    for client in fichier.keys():
        fichier[client]['PROBABILITY'] = predict(fichier[client])
    
    
    _avg = {}
    for nom in fichier.keys():
        
        if remboursement == True:
            threshold = fichier[nom]['PROBABILITY'] < 0.5
        else:
            threshold = fichier[nom]['PROBABILITY'] >= 0.5 
        
        for variable in fichier[nom].keys():
            count = 0
            _sum = 0
            if not isNan(fichier[nom][variable])\
                and type(fichier[nom][variable] != "str")\
                    and type(fichier[nom][variable] != "Indisp")\
                        and threshold\
                            and variable != 'PROBABILITY':
                try:
                    count += 1
                    _sum += fichier[nom][variable]
                    _avg[variable] = round(_sum / count,3) # pour plus de lisibilité dans les graph, on va arrondir 
                except TypeError:
                    print('Erreur')
                    print(nom)
                    print(variable)
                    print(fichier[nom][variable])
                    
    
    return _avg

@app.get('/alldata/')
async def ensemble_data(remboursement:bool):
    
    all_data = fichier.copy()
    data_trier = {}
    

    
    for nom in all_data.keys():
        all_data[nom]['PROBABILITY'] = predict(all_data[nom])
        
        if remboursement == True:
            threshold = fichier[nom]['PROBABILITY'] < 0.5
        else:
            threshold = fichier[nom]['PROBABILITY'] >= 0.5 
            
        for variable in all_data[nom].keys():
                if isNan(all_data[nom][variable]):
                    all_data[nom][variable] = 'Indisp'
        if threshold:
                data_trier[nom] = all_data[nom]
                    
        
    return data_trier



    
# {
#   "PAYMENT_RATE": 0.03965625,
#   "EXT_SOURCE_1": "Indisp",
#   "EXT_SOURCE_3": 0.6347055309763198,
#   "EXT_SOURCE_2": 0.7221783702089665,
#   "DAYS_BIRTH": 14144,
#   "AMT_ANNUITY": 28552.5,
#   "DAYS_EMPLOYED": -4516,
#   "APPROVED_CNT_PAYMENT_MEAN": 10.666666666666666,
#   "DAYS_ID_PUBLISH": -4616,
#   "INCOME_CREDIT_PERC": 0.1812857142857142,
#   "ACTIVE_DAYS_CREDIT_MAX": -1409,
#   "INSTAL_DAYS_ENTRY_PAYMENT_MAX": -1076,
#   "INSTAL_DPD_MEAN": 1.6590909090909092,
#   "DAYS_REGISTRATION": -1516,
#   "DAYS_EMPLOYED_PERC": 0.319287330316742,
#   "ACTIVE_DAYS_CREDIT_ENDDATE_MIN": -742,
#   "AMT_CREDIT": 720000,
#   "PREV_CNT_PAYMENT_MEAN": 10.666666666666666,
#   "AMT_GOODS_PRICE": 720000,
#   "INSTAL_AMT_PAYMENT_SUM": 239569.11,
#   "REGION_POPULATION_RELATIVE": 0.030755,
#   "INSTAL_DBD_SUM": 339,
#   "DAYS_LAST_PHONE_CHANGE": -1450,
#   "BURO_AMT_CREDIT_MAX_OVERDUE_MEAN": 4769.622,
#   "CLOSED_DAYS_CREDIT_MAX": -832,
#   "OWN_CAR_AGE": 7,
#   "CLOSED_DAYS_CREDIT_ENDDATE_MAX": -285,
#   "APPROVED_DAYS_DECISION_MAX": -1450,
#   "POS_MONTHS_BALANCE_SIZE": 35,
#   "ACTIVE_AMT_CREDIT_SUM_SUM": 4500,
#   "ACTIVE_DAYS_CREDIT_UPDATE_MEAN": -618,
#   "BURO_DAYS_CREDIT_MAX": -832,
#   "BURO_DAYS_CREDIT_ENDDATE_MAX": -285,
#   "INSTAL_AMT_PAYMENT_MIN": 0.63,
#   "ACTIVE_DAYS_CREDIT_ENDDATE_MAX": -742,
#   "ACTIVE_DAYS_CREDIT_MEAN": -1409,
#   "INSTAL_DBD_MAX": 35,
#   "CLOSED_AMT_CREDIT_SUM_MEAN": 48482.1,
#   "BURO_AMT_CREDIT_SUM_DEBT_MEAN": 0,
#   "ACTIVE_DAYS_CREDIT_ENDDATE_MEAN": -742,
#   "PROBABILITY": 0.16
# }


if __name__ == '__main__':
    uvicorn.run("api:app", host='127.0.0.1', port=8000, log_level='info')
    