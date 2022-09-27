import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Tableau de bord (Data)",
    page_icon="✅",
    layout="wide",
)

df_data = st.session_state.data

# Data
     
st.markdown("<h3 style='color: white;'>View data</h3>", unsafe_allow_html=True )

property_cells = {'background-color': '#0083B9',
                            'border-color': 'white',
                            'props' : 'black'}


    

    # Affichage

df_style = df_data.style.set_properties(**property_cells)

checkbox_data = st.checkbox('Show data')

if checkbox_data:
    st.dataframe(df_style)
        

    # Definition de la data


descriptif = pd.read_csv('/app/description_variables.csv')
liste_columns = list(df_data.columns)

# dans le descriptif, il n'y a pas les notions de min, max, sum ... ni certains mots clés
for index, item in enumerate(liste_columns):
    for mot_cle in ['_MAX', '_SUM', '_MEAN', '_MIN', '_SIZE']:
        if liste_columns[index].find(mot_cle) != -1:
            liste_columns[index] = item[:-len(mot_cle)]
                
    # on supprime le mot cle "buro":
        
    for mot_cle2 in ['BURO_', 'ACTIVE_']: 
        if liste_columns[index].find(mot_cle2) != -1:
            liste_columns[index] = liste_columns[index][len(mot_cle2):]
        
    # parfois il reste un _
        if liste_columns[index][-1] == "_" :
            liste_columns[index] = liste_columns[index][:-1]
            
checkbox_descrption = st.checkbox('Definition data')

if checkbox_descrption:
    st.dataframe(descriptif[descriptif['Row'].isin(liste_columns)].set_index('Row')['Description'])
