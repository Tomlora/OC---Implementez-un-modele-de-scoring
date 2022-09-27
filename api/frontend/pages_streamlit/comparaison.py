import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def comparaison_client(data_avg_rembourse, data_avg_no_rembourse, data_all_rembourse, data_all_no_rembourse):

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
                name = 'Remboursé',
                marker_color = '#0000CC',
                marker=dict(size=[30]),
                showlegend=showlegend,

                
            ))
            
            fig.add_trace(go.Scatter(
                x = [item],
                y = data_avg_no_rembourse[value],
                name = 'Non-remboursé',
                marker_color = '#4169E1',
                marker=dict(size=[30]),
                showlegend=showlegend,

                
            ))

            fig.add_trace(go.Scatter(
                x = [item],
                y = st.session_state.data[value],
                name = 'Client',
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

    sequence_color = ['#2C75FF', '#00BFFF', '#4169E1', '#ADD8E6', '#F0FFFF', '#87CEFA']
    def boxplot_comparaison(dict_comparaison, remboursement:bool=True):
        '''Compare la boxplot de la variable et la valeur de la variable de la target'''
        # moyenne des clients qui remboursent et moyenne des clients qui remboursent pas
        fig = go.Figure()
        i = 0
        
        if remboursement == True:
            y = data_all_rembourse
        else:
            y = data_all_no_rembourse  
            
        for item, value in dict_comparaison.items():
            fig.add_trace(go.Box(
                    y = y[value],
                    marker_color=sequence_color[i], # à modifier
                    name=item,
            
                ))
            
                
            fig.add_trace(go.Scatter(
                x=[item],
                y=st.session_state.data[value],
                name=item,mode='markers',
                marker_color='rgba(255,255,255,1)', # à modifier
                marker=dict(size=[30]),
    
                ))
            i += 1
            
        fig.update_layout(showlegend=False)

        fig.show()
                                    
            
        return fig


            # Par rapport aux autres ?
            
    st.markdown("<h3 style='color: white;'>Comparaison</h3>", unsafe_allow_html=True )

    dict_filtre = {'EXT_SOURCE' : {'EXT_SOURCE_1' : 'EXT_SOURCE_1',
                                    'EXT_SOURCE_2' : 'EXT_SOURCE_2',
                                    'EXT_SOURCE_3' : 'EXT_SOURCE_3'},
                   'CREDIT' : {'AMT_CREDIT' : 'AMT_CREDIT',
                               'AMT_ANNUITY' : 'AMT_ANNUITY',
                               'AMT_GOODS_PRICE' : 'AMT_GOODS_PRICE'},
                   'PAYMENT_RATE' : {'PAYMENT_RATE' : 'PAYMENT_RATE'},
                   'INFOS PERSONNELLES' : {'DAYS_BIRTH' : 'DAYS_BIRTH',
                                           'DAYS_EMPLOYED' : 'DAYS_EMPLOYED',
                                           'DAYS_ID_PUBLISH' : 'DAYS_ID_PUBLISH',
                                           'DAYS_REGISTRATION' : 'DAYS_REGISTRATION',
                                           'OWN_CAR_AGE' : 'OWN_CAR_AGE',
                                           'DAYS_LAST_PHONE_CHANGE' : 'DAYS_LAST_PHONE_CHANGE'},
                   'INFOS PERSONNELLES(%)' : {'DAYS_EMPLOYED_PERC' : 'DAYS_EMPLOYED_PERC',
                                              'INCOME_CREDIT_PERC' : 'INCOME_CREDIT_PERC'}}


    filtre = st.selectbox('Variables', list(dict_filtre.keys()))
    
    row1_col1, row1_col2, row1_col3 = st.columns(3)

    with row1_col2:
        st.subheader('Comparaison à la moyenne')
        graph3 = scatter_comparaison_avg(dict_filtre[filtre])
                

        graph3.update_layout({
                    'plot_bgcolor': 'rgb(0, 0, 0, 0)',
                    'paper_bgcolor': 'rgb(0, 0, 0, 0)',
                    'font_color' : "white",
                    })
                    # rgba(0,0,0,0)
                    
                    
        st.write(graph3)
            
    row2_col1, row2_col2 = st.columns(2)
            
            



    with row2_col1:
        st.subheader('Remboursement')
        graph4 = boxplot_comparaison(dict_filtre[filtre])
        graph4.update_layout({
                'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                'font_color' : "white",
                })
            
        st.write(graph4)
            
                
    with row2_col2:
        st.subheader('Non remboursement')
        graph5 = boxplot_comparaison(dict_filtre[filtre], False)
        graph5.update_layout({
                'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                'font_color' : "white",
                })
            
        st.write(graph5)