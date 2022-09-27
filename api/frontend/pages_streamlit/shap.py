import shap
import streamlit as st
import streamlit.components.v1 as components
import pickle
import matplotlib.pyplot as plt


def show_shap(index_liste):


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

    df_shap = st.session_state.data.drop(['PROBABILITY'], axis=1)
        
    # CSS

    with open('/app/style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    # title du dashboard
    st.markdown("<h1 style='text-align: center; color: white;'>Tableau de bord (Shap) </h1>", unsafe_allow_html=True )

    if index_liste != -1: # si pas -1, on a le client

        st_shap(shap.force_plot(shap_expected_values[0], shap_values[0][index_liste,:], df_shap, show=False))
                    

        shap3, shap4 = st.columns(2)

        with shap3:
            shap.plots._waterfall.waterfall_legacy(shap_expected_values[1], shap_values[1][index_liste,:], feature_names=df_shap.columns, show=False, max_display=40)
            plt.savefig("decision_waterfall.png",dpi=150, bbox_inches='tight')
            st.image('decision_waterfall.png')
            plt.clf()

        with shap4:
            shap.decision_plot(shap_expected_values[1], shap_values[1][index_liste,:], df_shap, show=False)
            plt.savefig("decision1.png",dpi=150, bbox_inches='tight')
            st.image('decision1.png')
            plt.clf()
            
    else:
        
        st.write("Indisponible pour les clients non-enregistrés")