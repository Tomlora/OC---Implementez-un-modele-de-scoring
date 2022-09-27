from flask import Flask, render_template, request, jsonify
import pandas as pd
import json
import plotly
import plotly.express as px
import yfinance as yf
from sklearn.metrics import confusion_matrix, make_scorer
import pickle
import numpy as np
import requests


# A lire
# https://openclassrooms.com/fr/courses/4525361-realisez-un-dashboard-avec-tableau/5774821-affichez-vos-visualisations-grace-a-javascript-et-html


app = Flask(__name__)
app.config["DEBUG"] = True
# Create some test data for our catalog in the form of a list of dictionaries.

# -- fonc test

import re

def extract_keywords(texts):
    """
    Prends une liste de textes et en détecte les mots les plus fréquents. Cette fonction renvoie 
    la liste des textes et le comptage des mots.
    """

    keywords = {}
    articles = []

    for i, text in enumerate(texts):
        # Extraction des éléments selon la structure JSON renvoyée par l'API NEWSAPI.ORG
        source = text["source"]["name"]
        title = text["title"]
        description = text["description"]
        url = text["url"]
        content = text["content"]

        # Stockage des articles dans la variable articles
        articles.append({'title': title, 'url': url, 'source':source})

        # Détection des mots clés (mots les plus utilisés)
        text = str(title) + ' ' + str(description) + ' ' + str(content)
        words = normalise_and_get_words(text)

        # Comptage des mots
        for w in words :
            if w not in keywords:
                keywords[w] = {'cnt': 1, 'articles':[i]}
            else:
                keywords[w]['cnt'] += 1
                if i not in keywords[w]['articles']:
                    keywords[w]['articles'].append(i)

    # Tri des mots, du plus utilisé au moins utilisé
    keywords = [{'word':word, **data} for word,data in keywords.items()] 
    keywords = sorted(keywords, key=lambda x: -x['cnt'])

    return keywords, articles

def load_stop_words():
    """
    Charge la liste des stopwords français (les mots très utilisés qui ne sont pas porteurs de sens comme LA, LE, ET, etc.)
    """

    words = []
    # Ouverture du fichier "stop_words.txt"
    with open("flask/stop_words.txt") as f:
        for word in f.readlines():
            words.append(word[:-1])
    return words

def normalise_and_get_words(text):
    """
    Prends un texte, le formate puis renvoie tous les mots significatifs qui le constituent
    """

    stop_words = load_stop_words()

    # Utilisation des expressions régulières (voir https://docs.python.org/3.7/library/re.html et https://openclassrooms.com/fr/courses/4425111-perfectionnez-vous-en-python/4464009-utilisez-des-expressions-regulieres)
    text = re.sub("\W"," ",text) # suppression de tous les caractères autres que des mots
    text = re.sub(" \d+", " ", text) # suppression des nombres
    text = text.lower() # convertit le texte en minuscules
    words = re.split("\s",text) # sépare tous les mots du texte

    words = [w for w in words if len(w) > 2] # suppression des mots de moins de 2 caractères
    words = [w for w in words if w not in stop_words] # suppression des stopwords
    return words

# ---------------------- Data

with open('flask/data.pkl', 'rb') as f:
    fichier = pickle.load(f)
    
    
df_data = pd.DataFrame(pd.read_pickle('flask/data.pkl')).transpose()
    
# ---------------------- Pipeline

def cout_metier(y_test, pred_test_y):
    poids_tn = 1 # on maximise le nombre de personnes pouvant rembourser son prêt
    poids_fp = 0
    poids_fn = -10 # on veut à tout prix éviter les personnes ne remboursant pas le prêt que l'algorithme n'arrive pas à détecter
    poids_tp = 0
    conf_mat = confusion_matrix(y_test, pred_test_y)
    tn, fp, fn, tp = conf_mat.ravel()
    total = tn+fp+fn+tp
    
    return (tn*poids_tn + fp*poids_fp + fn*poids_fn + tp * poids_tp)/total


metric_custom = make_scorer(cout_metier)




url_pipeline = 'pipeline/pipeline_perso_random_iter50.pkl'
pipe = pickle.load(open(url_pipeline, 'rb'))

def predict(dict):
    # si on a déjà predict, la valeur est retenue, donc :
    if len(dict) >= 41:
        del dict['PROBABILITY']
        
    df = pd.DataFrame.from_dict(dict, orient="index")
    df = df.transpose()
    proba = pipe.predict_proba(df)[:,1] # Probabilité de remboursement
    proba = round(np.array(proba)[0],2)
    return proba

# Fonction de correction

def isNan(num):
    return num != num


# ---------------------- API (Raw data)

@app.route('/', methods=['GET'])
def home():
 return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''

@app.route('/api/v1/resources/search')
def form():
    return render_template('form.html')
  
@app.route('/api/v1/resources/data/all', methods=['GET'])
def api_all():
    return jsonify({'data' : fichier})

@app.route('/api/v1/resources/data', methods=['GET'])
def api_id():
 # Check if an ID was provided as part of the URL.
 # If ID is provided, assign it to a variable.
 # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."
    # On fait un doublon sinon il le garde en mémoire et l'algorithme a trop de features


    fichier[id]['PROBABILITY'] = predict(fichier[id])
            

    return jsonify({'status' : 'ok',
                    'data' : {'client' : fichier[id]}})


# ------------------- API (Dashboard)

@app.route('/api/v1/dashboard/search')
def form_dashboard():
    return render_template('form.html')

@app.route('/api/v1/dashboard/result')
def dash():
    
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."
    
    # On fait un doublon sinon il le garde en mémoire et l'algorithme a trop de features
    
    # predict 
    
    fichier[id]['PROBABILITY'] = predict(fichier[id])
    
    for key in fichier[id].keys():
        if isNan(fichier[id][key]):
            fichier[id][key] = 0
    
    # Graphique 2 -----
    
    fig = px.pie(values=[df_data.loc[id]['EXT_SOURCE_1'], df_data.loc[id]['EXT_SOURCE_2'], df_data.loc[id]['EXT_SOURCE_3']],
                names=['EXT_SOURCE_1', 'EXT_SOURCE_2', 'EXT_SOURCE_3'])
    fig.update_traces(textinfo='value')
    
    graphJSON2 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    

    # Graphique 3 -----

    df = pd.DataFrame({
        "Vegetables": ["Lettuce", "Cauliflower", "Carrots", "Lettuce", "Cauliflower", "Carrots"],
        "Amount": [10, 15, 8, 5, 14, 25],
        "City": ["London", "London", "London", "Madrid", "Madrid", "Madrid"]
    })

    fig = px.bar(df, x="Vegetables", y="Amount", color="City", barmode="stack")

    graphJSON3 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('dashboard.html', graphJSON3 = graphJSON3, graphJSON2=graphJSON2, client = id, predict = fichier[id]['PROBABILITY'])

# ------------ test

# Define the root route
@app.route('/test/')
def index():

    return render_template('index3.html')

@app.route('/callback/<endpoint>')
def cb(endpoint):   
    if endpoint == "getStock":
        return gm(request.args.get('data'),request.args.get('period'),request.args.get('interval'))
    elif endpoint == "getInfo":
        stock = request.args.get('data')
        st = yf.Ticker(stock)
        return json.dumps(st.info)
    else:
        return "Bad endpoint", 400

# Return the JSON data for the Plotly graph
def gm(stock,period, interval):
    st = yf.Ticker(stock)
  
    # Create a line graph
    df = st.history(period=(period), interval=interval)
    df=df.reset_index()
    df.columns = ['Date-Time']+list(df.columns[1:])
    max = (df['Open'].max())
    min = (df['Open'].min())
    range = max - min
    margin = range * 0.05
    max = max + margin
    min = min - margin
    fig = px.area(df, x='Date-Time', y="Open",
        hover_data=("Open","Close","Volume"), 
        range_y=(min,max), template="seaborn" )


    # Create a JSON representation of the graph
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
 

app.run(debug=True)




