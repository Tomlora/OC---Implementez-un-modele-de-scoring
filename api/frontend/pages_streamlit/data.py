import streamlit as st
import pandas as pd
import numpy as np



def show_data():
    
    def positive_nombre(x):
        if type(x) == int or type(x) == float:
            if x < 0:
                x = x * (-1) 
        return x
 
    # Data
        
    st.markdown("<h3 style='color: white;'>View data</h3>", unsafe_allow_html=True )

    property_cells = {'background-color': '#0083B9',
                                'border-color': 'white',
                                'props' : 'black'}

    # Modification des features
    
    data_brut = st.session_state.data.copy()

        
    # Certaines colonnes seront plus lisibles en étant positive
    for col in ['DAYS_EMPLOYED', 'DAYS_ID_PUBLISH', 'DAYS_BIRTH']:
        data_brut[col] = data_brut[col].apply(positive_nombre)
        
    # pour plus de lisibilité, on va changer les jours en mois

    for col in ['DAYS_BIRTH', 'DAYS_ID_PUBLISH', 'DAYS_EMPLOYED']:
        data_brut[col] = np.ceil(data_brut[col] / 30)
        
    data_brut.rename(columns={'DAYS_BIRTH' : 'MONTHS_BIRTH',
                        'DAYS_ID_PUBLISH' : 'MONTH_ID_PUBLISH',
                        'DAYS_EMPLOYED' : 'MONTH_EMPLOYED'}, inplace=True )
        

    # Affichage

    df_style = data_brut.style.set_properties(**property_cells)



    checkbox_data = st.checkbox('Show data')

    if checkbox_data:
        st.dataframe(df_style)
               

        # Definition de la data


    descriptif = pd.read_csv('/app/description_variables.csv')
    liste_columns = list(data_brut.columns)

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
                
            
    checkbox_description = st.checkbox('Definition data')

    if checkbox_description:
        st.dataframe(descriptif[descriptif['Row'].isin(liste_columns)].set_index('Row')['Description'])
