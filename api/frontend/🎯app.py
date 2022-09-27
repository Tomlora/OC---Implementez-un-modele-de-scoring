import streamlit as st
import streamlit.components.v1 as components
import requests
import pandas as pd
import plotly.figure_factory as ff
import numpy as np
import plotly.express as px
import json
import plotly.graph_objects as go
import matplotlib.pyplot as plt

# Ordre : 
# - Data (Analyse exploratoire)
# - Comparaison
# - Shap
# - Observation sur les plus proches voisins selon MES critères (Qui rembourse ? Qui rembourse pas ?)

# Regarder le package Altair

url_api = 'kevin-oc-api.herokuapp.com'

# Inspiration :

# https://blog.streamlit.io/introducing-theming/
# https://github.com/dataprofessor/dashboard CSS
# https://www.youtube.com/watch?v=tx6bT2Sh9R8 CSS
# https://www.youtube.com/watch?v=fThcHGiTOeQ
# https://github.com/Sven-Bo/streamlit-sales-dashboard color
# https://camo.githubusercontent.com/199cfa19cd6a1639129c898a8d8086eb34936ba54630f19e867747d441d99414/68747470733a2f2f636f6e74656e742e73637265656e636173742e636f6d2f75736572732f6a756262656c332f666f6c646572732f536e616769742f6d656469612f36346234643634612d346535392d346265632d396631362d3737316562316139393030352f30382e31382e323032312d31392e35302e6a7067
# https://uploads-ssl.webflow.com/5faacf1ab5208b6ac2d6a141/60947b668904674c610a5496_worst_case_app.png

# https://github.com/Jcharis/Streamlit_DataScience_Apps
# https://github.com/Jcharis/Machine-Learning-Web-Apps

# Variables

sequence_color = ['#0000CC', '#00BFFF', '#4169E1']


# shap_explainer = pickle.load(open('shap_model/explainer.pkl', 'rb'))
   

# Fonctions

def positive_nombre(x):
    if type(x) == int or type(x) == float:
        if x < 0:
            x = x * (-1) 
    return x

def collect_donnees(lien, shap:bool=False, client_connu:bool=True):

    if client_connu:
        response = requests.get(lien)
        data_table = pd.DataFrame.from_dict(response.json(), orient="index")
    else:
        data_table = pd.DataFrame.from_dict(lien, orient="index")

    
    data_table = data_table.transpose()
    
    # on transforme tous les nombres négatifs dans la data de départ en positif ... Ce sera plus lisible pour les graphiques.
    
    for col in data_table.columns:
        data_table[col] = data_table[col].apply(positive_nombre)
        
    if shap:
        data_table.drop(['PROBABILITY'], axis=1, inplace=True)
        
    return data_table

def collecte_prediction(client_id):
    response = requests.get(f'https://{url_api}/client/probability/{client_id}').json()
    
    return response['result']


def collecte_id_clients():
    response = requests.get(f'http://{url_api}/client/all/').json()
    response = np.asarray(json.loads(response))
    return response

def pie(value:list, name:list, type=None):
    graph = px.pie(values=value,
                    names=name, color_discrete_sequence=sequence_color)

    if type == 'value':
        graph.update_traces(textinfo='value')
    graph.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    'font_color' : "white",
    })
    
    return graph

def scatter_comparaison_avg(dict_comparaison):
    '''Compare la moyenne de la variable et la valeur de la variable de la target'''
    # moyenne des clients qui remboursent et moyenne des clients qui remboursent pas
    fig = go.Figure()
    i = 0
    for item, value in dict_comparaison.items():
        if i==0: # on ne prendra la légende que du premier pur éviter des doublons
            showlegend=True
        else:
            showlegend=False
            
        fig.add_trace(go.Scatter(
            x = [item],
            y = data_avg_rembourse[value],
            name = 'rembourse',
            marker_color = '#0000CC',
            marker=dict(size=[30]),
            showlegend=showlegend,

            
        ))
        
        fig.add_trace(go.Scatter(
            x = [item],
            y = data_avg_no_rembourse[value],
            name = 'non-rembourse',
            marker_color = '#4169E1',
            marker=dict(size=[30]),
            showlegend=showlegend,

            
        ))

        fig.add_trace(go.Scatter(
            x = [item],
            y = collect_donnees(f'http://{url_api}/client/{client_id}')[value],
            name = "Client",
            marker_color = '#00BFFF',
            marker=dict(size=[30]),
            showlegend=showlegend,

        ))
    
        i += 1
    # fig.update_layout(showlegend=True)
    fig.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    bgcolor='rgba(0,0,0,0)',
    y=1.02,
    xanchor="right",
    x=1
    ))
        
        
    return fig

sequence_color = ['#0000CC', '#00BFFF', '#4169E1']
def boxplot_comparaison(dict_comparaison):
    '''Compare la boxplot de la variable et la valeur de la variable de la target'''
    # moyenne des clients qui remboursent et moyenne des clients qui remboursent pas
    fig = go.Figure()
    i = 0
    for item, value in dict_comparaison.items():
        fig.add_trace(go.Box(
                y = data_all_rembourse[value],
                marker_color=sequence_color[i], # à modifier
                name=item,
          
            ))
        
        # fig.add_trace(go.Box(
        #         y = data_all_no_rembourse[value],
        #         marker_color=sequence_color[i], # à modifier
        #         name=item            
        #     ))
            
        fig.add_trace(go.Scatter(
            x=[item],
            y=collect_donnees(f'http://{url_api}/client/{client_id}')[value],
            name=item,mode='markers',
            marker_color='rgba(255,255,255,1)', # à modifier
            marker=dict(size=[30]),
 
            ))
        i += 1
        
    fig.update_layout(showlegend=False)

    fig.show()
                                   
        
    return fig

# ----------------------------------------------------------------------------------------

# config de la page

st.set_page_config(
    page_title="Tableau de bord",
    page_icon="✅",
    layout="wide",
)

# CSS

with open('/app/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# title du dashboard
st.markdown("<h1 style='text-align: center; color: white;'>Tableau de bord </h1>", unsafe_allow_html=True )

# Choix de la méthode

st.session_state.type_requete = st.selectbox('Type de client', ['Client déjà enregistré', 'Nouveau client'])

# data qui ne change pas

@st.cache
def chargement_data():
    data_avg_rembourse = collect_donnees('https://kevin-oc-api.herokuapp.com/client/client_avg/?remboursement=true')
    data_avg_no_rembourse = collect_donnees('https://kevin-oc-api.herokuapp.com/client/client_avg/?remboursement=false')
    data_all_rembourse = collect_donnees('https://kevin-oc-api.herokuapp.com/alldata/?remboursement=true').transpose()
    data_all_no_rembourse = collect_donnees('https://kevin-oc-api.herokuapp.com/alldata/?remboursement=false').transpose()
    return data_avg_rembourse, data_avg_no_rembourse, data_all_rembourse, data_all_no_rembourse

data_avg_rembourse, data_avg_no_rembourse, data_all_rembourse, data_all_no_rembourse = chargement_data()

# filtre

if st.session_state['type_requete'] == 'Client déjà enregistré':
    client_id = st.selectbox('Select the client', collecte_id_clients()) # Trop de clients = lag
    proba_non_remboursement = collecte_prediction(client_id)
    df_data = collect_donnees(f'http://{url_api}/client/{client_id}')
    st.session_state['data'] = df_data
    
    
    
else:
    with st.form('Formulaire'):
        st.write("None si inconnu")
        
        header = {
              "PAYMENT_RATE": 0,
              "EXT_SOURCE_1": 0,
              "EXT_SOURCE_2": 0,
              "EXT_SOURCE_3": 0,
              "DAYS_BIRTH": 0,
              "AMT_ANNUITY": 0,
              "DAYS_EMPLOYED": 0,
              "APPROVED_CNT_PAYMENT_MEAN": 0,
              "DAYS_ID_PUBLISH": 0,
              "INCOME_CREDIT_PERC": 0,
              "ACTIVE_DAYS_CREDIT_MAX": 0,
              "INSTAL_DAYS_ENTRY_PAYMENT_MAX": 0,
              "INSTAL_DPD_MEAN": 0,
              "DAYS_REGISTRATION": 0,
              "DAYS_EMPLOYED_PERC": 0,
              "ACTIVE_DAYS_CREDIT_ENDDATE_MIN": 0,
              "AMT_CREDIT": 0,
              "PREV_CNT_PAYMENT_MEAN": 0,
              "AMT_GOODS_PRICE": 0,
              "INSTAL_AMT_PAYMENT_SUM": 0,
              "REGION_POPULATION_RELATIVE": 0,
              "INSTAL_DBD_SUM": 0,
              "DAYS_LAST_PHONE_CHANGE": 0,
              "BURO_AMT_CREDIT_MAX_OVERDUE_MEAN": 0,
              "CLOSED_DAYS_CREDIT_MAX": 0,
              "OWN_CAR_AGE": 0,
              "CLOSED_DAYS_CREDIT_ENDDATE_MAX": 0,
              "APPROVED_DAYS_DECISION_MAX": 0,
              "POS_MONTHS_BALANCE_SIZE": 0,
              "ACTIVE_AMT_CREDIT_SUM_SUM": 0,
              "ACTIVE_DAYS_CREDIT_UPDATE_MEAN": 0,
              "BURO_DAYS_CREDIT_MAX": 0,
              "BURO_DAYS_CREDIT_ENDDATE_MAX": 0,
              "INSTAL_AMT_PAYMENT_MIN": 0,
              "ACTIVE_DAYS_CREDIT_ENDDATE_MAX": 0,
              "ACTIVE_DAYS_CREDIT_MEAN": 0,
              "INSTAL_DBD_MAX": 0,
              "CLOSED_AMT_CREDIT_SUM_MEAN": 0,
              "BURO_AMT_CREDIT_SUM_DEBT_MEAN": 0,
              "ACTIVE_DAYS_CREDIT_ENDDATE_MEAN": 0
            }
        
        help_input = { # à compléter
              "PAYMENT_RATE": 0,
              "EXT_SOURCE_1": 0,
              "EXT_SOURCE_2": 0,
              "EXT_SOURCE_3": 0,
              "DAYS_BIRTH": 0,
              "AMT_ANNUITY": 0,
              "DAYS_EMPLOYED": 0,
              "APPROVED_CNT_PAYMENT_MEAN": 0,
              "DAYS_ID_PUBLISH": 0,
              "INCOME_CREDIT_PERC": 0,
              "ACTIVE_DAYS_CREDIT_MAX": 0,
              "INSTAL_DAYS_ENTRY_PAYMENT_MAX": 0,
              "INSTAL_DPD_MEAN": 0,
              "DAYS_REGISTRATION": 0,
              "DAYS_EMPLOYED_PERC": 0,
              "ACTIVE_DAYS_CREDIT_ENDDATE_MIN": 0,
              "AMT_CREDIT": 0,
              "PREV_CNT_PAYMENT_MEAN": 0,
              "AMT_GOODS_PRICE": 0,
              "INSTAL_AMT_PAYMENT_SUM": 0,
              "REGION_POPULATION_RELATIVE": 0,
              "INSTAL_DBD_SUM": 0,
              "DAYS_LAST_PHONE_CHANGE": 0,
              "BURO_AMT_CREDIT_MAX_OVERDUE_MEAN": 0,
              "CLOSED_DAYS_CREDIT_MAX": 0,
              "OWN_CAR_AGE": 0,
              "CLOSED_DAYS_CREDIT_ENDDATE_MAX": 0,
              "APPROVED_DAYS_DECISION_MAX": 0,
              "POS_MONTHS_BALANCE_SIZE": 0,
              "ACTIVE_AMT_CREDIT_SUM_SUM": 0,
              "ACTIVE_DAYS_CREDIT_UPDATE_MEAN": 0,
              "BURO_DAYS_CREDIT_MAX": 0,
              "BURO_DAYS_CREDIT_ENDDATE_MAX": 0,
              "INSTAL_AMT_PAYMENT_MIN": 0,
              "ACTIVE_DAYS_CREDIT_ENDDATE_MAX": 0,
              "ACTIVE_DAYS_CREDIT_MEAN": 0,
              "INSTAL_DBD_MAX": 0,
              "CLOSED_AMT_CREDIT_SUM_MEAN": 0,
              "BURO_AMT_CREDIT_SUM_DEBT_MEAN": 0,
              "ACTIVE_DAYS_CREDIT_ENDDATE_MEAN": 0
            }
        
        for key_value in header.keys(): # Formulaire
            header[key_value] = st.text_input(key_value, value=None)
            
            if header[key_value] == 'None': # le text input ne renvoie qu'un str, donc on transpose en vrai 'None'
                header[key_value] = None
        
        
        
        submitted = st.form_submit_button('Valider')
        if submitted: # tout à faire
            st.write('Envoyé !') # Requete api avec les données
            url = f'https://{url_api}/client/new/'

            client_id = requests.get(url, params=header).json()
            proba_non_remboursement = client_id['result'] # Requete à l'api avec les données
            header['PROBABILITY'] = proba_non_remboursement
            df_data = collect_donnees(header, client_connu=False) # df avec demander les donnees

# boxplot avec une barre "où est situé le client" dans la distribution
# afficher les clients proches du client selectionné pour voir les différences 


if st.session_state['type_requete'] == 'Client déjà enregistré' or submitted:
    
        # Infos client
            
    st.markdown("<h2 style='text-align: center; color: white;'>Situation du client </h2>", unsafe_allow_html=True )

    ## Temps de travail
    
    with st.expander('Infos client'):
        
        exp1_row1_col1, exp1_row1_col2, exp1_row1_col3 = st.columns(3)

        with exp1_row1_col1:
            age = int(df_data['DAYS_BIRTH'] / 365) # L'age est en jour, on le met en année
            st.metric('Age', age )
            
        with exp1_row1_col2:
            if df_data['OWN_CAR_AGE'].iloc[0] != 'Indisp':
                st.metric('Age voiture', int(df_data['OWN_CAR_AGE']))
                
        with exp1_row1_col3:
            if df_data['DAYS_EMPLOYED'].iloc[0] != 'Indisp':
                st.metric('Jours travaillés', int(df_data['DAYS_EMPLOYED']))
                
        
        exp2_row2_col1, exp2_row2_col2 = st.columns(2)
        
        with exp2_row2_col1:
            graph1 = pie([df_data['EXT_SOURCE_1'][0], df_data['EXT_SOURCE_2'][0], df_data['EXT_SOURCE_3'][0]],
                 ['EXT_SOURCE_1', 'EXT_SOURCE_2', 'EXT_SOURCE_3'], 'value')
            st.markdown("<h3 style='color: white;'>Notation Ext-Source</h3>", unsafe_allow_html=True )
            st.write(graph1)
        
        with exp2_row2_col2:
            if df_data['DAYS_BIRTH'].iloc[0] != 'Indisp' and df_data['DAYS_EMPLOYED'].iloc[0] != "Indisp":
                st.markdown(f"<h3 style='color: white;'>Durée totale travaillée ({round(df_data['DAYS_EMPLOYED_PERC'].iloc[0]*100,2)}%)</h3>", unsafe_allow_html=True )
                st.write(f'Durée totale travaillée ({round(df_data["DAYS_EMPLOYED_PERC"].iloc[0]*100,2)}%)')
                graph7 = pie([df_data['DAYS_EMPLOYED'].iloc[0], df_data['DAYS_EMPLOYED'].iloc[0] + df_data['DAYS_BIRTH'].iloc[0]],
                             ['Temps travaillé', 'Total'])
                st.write(graph7)
               
                
    row1_col1, row1_col2 = st.columns(2)

    fig_score = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = proba_non_remboursement,
        mode = "gauge+number",
        gauge = {'axis': {'range': [None, 1],
                        'tickmode' : 'array',
                        'tickvals' : [0, 0.2, 0.4, 0.6, 0.8, 1.0],
                        'ticktext' : ['Risque faible', 0.2, '0.4 - Risque moyen', '0.6 - Risque élevée', 0.8, 'Très élevée']},
                'bar' : {'color' : "darkblue"},
                'steps' : [
                    {'range': [0, 0.4], 'color': "cyan"},
                    {'range': [0.4, 0.6], 'color': "blue"},
                    {'range': [0.6, 1.0], 'color': "royalblue"}],
                'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 0.6}}))


    # with row1_col1:
    st.markdown("<h4 style= color: white;>Risque de non-remboursement 🎯</h4>", unsafe_allow_html=True )
    st.plotly_chart(fig_score)

    # Mise en place des graphiques :

    st.markdown("<h2 style='text-align: center; color: white;'>Credit </h2>", unsafe_allow_html=True )

    with st.expander('Credit'):
        exp2_row1_col1, exp2_row1_col2 = st.columns(2)
         
        with exp2_row1_col1:
            stats_name = ['CREDIT', 'ANNUITE', 'AMT GOOD PRICES']
            stats_value = [df_data['AMT_CREDIT'].values[0], df_data['AMT_ANNUITY'].values[0], df_data['AMT_GOODS_PRICE'].values[0]]

            df_stats = pd.DataFrame([stats_name, stats_value]).transpose()
            df_stats.columns = ['Indicateurs', 'value']

            graph2 = px.histogram(df_stats, 'Indicateurs', 'value', color='Indicateurs', text_auto=True, color_discrete_sequence=sequence_color)
            graph2.update_layout(showlegend=False, font=dict(size=20))
            graph2.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
            'font_color' : "white",
            })
            graph2.update_yaxes(visible=False)
            st.markdown("<h3 style='color: white;'>Credit</h3>", unsafe_allow_html=True )
            st.write(graph2)
            
        # Par rapport aux autres ?
        
        st.markdown("<h3 style='color: white;'>Comparaison</h3>", unsafe_allow_html=True )
        
        exp2_row2_col1, exp2_row2_col2 = st.columns(2)
        
        
        graph3 = scatter_comparaison_avg({'EXT_SOURCE_1' : 'EXT_SOURCE_1',
                                    'EXT_SOURCE_2' : 'EXT_SOURCE_2',
                                    'EXT_SOURCE_3' : 'EXT_SOURCE_3'})
        
        graph4 = boxplot_comparaison({'EXT_SOURCE_1' : 'EXT_SOURCE_1',
                                    'EXT_SOURCE_2' : 'EXT_SOURCE_2',
                                    'EXT_SOURCE_3' : 'EXT_SOURCE_3'})
        
        with exp2_row2_col1:
            graph3.update_layout({
            'plot_bgcolor': 'rgb(0, 0, 0, 0)',
            'paper_bgcolor': 'rgb(0, 0, 0, 0)',
            'font_color' : "white",
            })
            # rgba(0,0,0,0)
            st.write(graph3)
            
        with exp2_row2_col2:
            graph4.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
            'font_color' : "white",
            })
            
            st.write(graph4)


    # Index

if st.session_state['type_requete'] == 'Client déjà enregistré': # Shap ne supporte pas la partie "Simulation"
    # on cherche dans la liste des clients à quel index il est. Ca va permettre d'utiliser cet index dans le shap_value
    
    for i, index in enumerate(collecte_id_clients()):
        if index == client_id:
            index_liste = i
else:
    index_liste = -1
    
st.session_state['index'] = index_liste


    # D'un point de vue pro, vaut-il mieux montrer le 0 ou le 1 ?

    #     link : "identity" or "logit"
            # The transformation used when drawing the tick mark labels. Using logit will change log-odds numbers
            # into probabilities. 
            
    # Pas certain que les valeurs soient complètement fiables. Faut-il faire les étapes précédentes de la pipeline ? (Voir notebook 3 : class explain_predict)
            
    # https://medium.com/@ulalaparis/repousser-les-limites-dexplicabilit%C3%A9-un-guide-avanc%C3%A9-de-shap-a33813a4bbfc
    # https://www.aquiladata.fr/insights/shap-mieux-comprendre-linterpretation-de-modeles/#:~:text=Gr%C3%A2ce%20%C3%A0%20la%20valeur%20de,l'article%20%5B3%5D)
    # # https://www.aidancooper.co.uk/a-non-technical-guide-to-interpreting-shap-analyses/
    # https://blog.ysance.com/algorithme-n7-lime-ou-shap
    # https://datascience.eu/fr/apprentissage-automatique/interpretation-de-votre-modele-dapprentissage-profond-par-le-shap/
    # https://pythonmana.com/2022/01/202201100054096643.html
            
            






