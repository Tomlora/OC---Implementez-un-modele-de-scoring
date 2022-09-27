import shap
import streamlit as st
import streamlit.components.v1 as components
import pickle
import matplotlib.pyplot as plt

 

st.set_page_config(
    page_title="Tableau de bord",
    page_icon="✅",
    layout="wide",
)

df_data = st.session_state.data
index_liste = st.session_state.index   

# Fonctions

def st_shap(plot, height=None):
    shap_html = f"<head>{shap.getjs()}</head><body>{plot.html()}</body>"
    components.html(shap_html, height=height)
    
# Shap

shap_values = pickle.load(open('/app/shap_model/values.pkl', 'rb'))
shap_expected_values = pickle.load(open('/app/shap_model/expected_values.pkl', 'rb'))
shap_value_decision0 = pickle.load(open('/app/shap_model/decision_plot0.pkl', 'rb'))
shap_value_decision1 = pickle.load(open('/app/shap_model/decision_plot1.pkl', 'rb'))   

# Data

df_shap = df_data.drop(['PROBABILITY'], axis=1)
    
# CSS

with open('/app/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# title du dashboard
st.markdown("<h1 style='text-align: center; color: white;'>Tableau de bord (Shap) </h1>", unsafe_allow_html=True )

if index_liste != -1: # si pas -1, on a le client

    shap1, shap2 = st.columns(2)

            
            
    with shap1:
        st_shap(shap.force_plot(shap_expected_values[0], shap_values[0][index_liste,:], df_shap, link='logit', show=False))
                
    with shap2:    
        st_shap(shap.force_plot(shap_expected_values[1], shap_values[1][index_liste,:], df_shap, link='logit', show=False))
                

    shap3, shap4 = st.columns(2)

    with shap3:
        shap.decision_plot(shap_expected_values[0], shap_values[0][index_liste,:], df_shap,  show=False)
        plt.savefig("decision0.png",dpi=150, bbox_inches='tight')
        st.image('decision0.png')
        plt.clf()

    with shap4:
        shap.decision_plot(shap_expected_values[1], shap_values[1][index_liste,:], df_shap, show=False)
        plt.savefig("decision1.png",dpi=150, bbox_inches='tight')
        st.image('decision1.png')
        plt.clf()
        
else:
    
    st.write("Indisponible pour les clients non-enregistrés")