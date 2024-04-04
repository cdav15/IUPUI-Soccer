# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 06:33:34 2024

@author: cadgo
"""

### Men's Soccer Code

import pandas as pd
import streamlit as st
from urllib.request import urlopen
import matplotlib.pyplot as plt
from PIL import Image
from highlight_text import fig_text
from mplsoccer import PyPizza, add_image, FontManager
import numpy as np
from scipy import stats
import math
import sys
import io


def get_data():
    df = pd.read_csv('https://raw.githubusercontent.com/cdav15/IUPUISOC/main/IUPUI_MSOC_FORWARDS.csv')
    return df.set_index("Player")


def single_graph(params, player, values):
    baker = PyPizza(
    params=params,                  # list of parameters
    straight_line_color="#000000",  # color for straight lines
    straight_line_lw=1,             # linewidth for straight lines
    last_circle_lw=1,               # linewidth of last circle
    other_circle_lw=1,              # linewidth for other circles
    other_circle_ls="-."            # linestyle for other circles
    )

    # plot pizza
    fig, ax = baker.make_pizza(
        values,              # list of values
        figsize=(12, 12),      # adjust figsize according to your need
        param_location=110,  # where the parameters will be added
        kwargs_slices=dict(
            facecolor="cornflowerblue", edgecolor="#000000",
            zorder=2, linewidth=1
        ),                   # values to be used when plotting slices
        kwargs_params=dict(
            color="#000000", fontsize=10,
            va="center"
        ),                   # values to be used when adding parameter
        kwargs_values=dict(
            color="#000000", fontsize=12,  
            zorder=3,
            bbox=dict(
                edgecolor="#000000", facecolor="cornflowerblue",
                boxstyle="round,pad=0.2", lw=1
            )
        )                    # values to be used when adding parameter-values
    )

    # add title
    fig.text(
        0.515, 0.97, player, size=18,
        ha="center",   color="#000000"
    )

    # add subtitle
    fig.text(
        0.515, 0.942,
        "per 90 min Percentile Rank compared to teammates",
        size=15,
        ha="center",  color="#000000"
    )

    # add credits
    CREDIT_1 = "Data: Wyscout, compiled together by Chandler Davis"
    CREDIT_2 = ""

    fig.text(
        0.99, 0.005, f"{CREDIT_1}\n{CREDIT_2}", size=9,
        color="#000000",
        ha="right"
    )

    st.pyplot(fig)
    
    st.write('#### Download Graph as Image Below:')
    download_filename = st.text_input('Choose File Name:', value=player)
    
    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format='png')
    
    file_name1 = download_filename + '.jpg'
    
    st.download_button(
        label="Download Graph as PNG",
        data=img_bytes,
        file_name=file_name1,
        mime='image/png',
    )
    
def comparison_graph(params, player1, values1, player2, values2):
    baker3 = PyPizza(
        params=params,                 
        background_color="#EBEBE9",     
        straight_line_color="#222222",
        straight_line_lw=1,             
        last_circle_lw=1,               
        last_circle_color="#222222",    
        other_circle_ls="-.",           
        other_circle_lw=1               
    )


    fig3, ax3 = baker3.make_pizza(
        values1,                     
        compare_values=values2,    
        figsize=(12, 12),             
        kwargs_slices=dict(
            facecolor="#1A78CF", edgecolor="#222222",
            zorder=2, linewidth=1
        ),                          
        kwargs_compare=dict(
            facecolor="#FF9300", edgecolor="#222222",
            zorder=2, linewidth=1,
        ),
        kwargs_params=dict(
            color="#000000", fontsize=10,
            va="center"
        ),                          
        kwargs_values=dict(
            color="#000000", fontsize=12,
            zorder=3,
            bbox=dict(
                edgecolor="#000000", facecolor="cornflowerblue",
                boxstyle="round,pad=0.2", lw=1
            )
        ),                          
        kwargs_compare_values=dict(
            color="#000000", fontsize=12, zorder=3,
            bbox=dict(edgecolor="#000000", facecolor="#FF9300", boxstyle="round,pad=0.2", lw=1)
        ),                          
    )

    fig_text(
        0.515, 0.99, f"<{player1}> vs <{player2}>", size=17, fig=fig3,
        highlight_textprops=[{"color": '#1A78CF'}, {"color": '#EE8900'}],
        ha="center", color="#000000"
    )

    fig3.text(
        0.515, 0.942,
        "IUPUI Men's Soccer Player Comparison",
        size=15,
        ha="center", color="#000000"
    )

    CREDIT_1 = "data: Wyscout, compiled together by Chandler Davis"
    CREDIT_2 = ""

    fig3.text(
        0.99, 0.005, f"{CREDIT_1}\n{CREDIT_2}", size=9,
        color="#000000",
        ha="right"
    )
    pnames = player1 + ' and ' + player2 
    st.pyplot(fig3)
    st.write('#### Download Graph as Image Below:')
    download_filename = st.text_input('Choose File Name:', value=pnames)
    
    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format='png')
    
    file_name1 = download_filename + '.jpg'
    
    st.download_button(
        label="Download Graph as PNG",
        data=img_bytes,
        file_name=file_name1,
        mime='image/png',
    )
    
    
try:
    df = get_data()
    st.write("# IUPUI Men's Soccer Per 90 min Radar Charts")
    st.write("I've created this web app to help coaches better understand their data and to examine the strengths and weaknesses of their players.")
    st.write("Created by Chandler Davis")
    st.write("### Forwards, Midfielders, Defenders")
    df = df.drop(columns=['Position'])
    player_select = st.selectbox(
        "Choose one player", list(df.index)
    )
    if not player_select:
        st.error("Please Select a Player.")
    else:
        data = df.loc[[player_select]]
        
        st.write("### Player per 90 min Stats", data)

        params = list(df.columns)
        
        player = df.loc[[player_select]].reset_index()
        player = list(player.loc[0])
        player = player[1:]
        
        values = []
        for x in range(len(params)):
            values.append(math.floor(stats.percentileofscore(df[params[x]],player[x])))
            
        single_graph(params, player_select, values)
        
###########################################################################
###########################################################################

        st.write("### Comparison Chart")
        
        players = st.selectbox(
            "## Choose a player:", list(df.index), index=1)
        
        players1 = st.selectbox(
            "## Choose a player to compare to:", list(df.index), index=3)
        
        datas = df.loc[[players, players1]]
        
        
        st.write("### Player per 90 min Stats", datas)
        
        p1 = datas.index[0]
        p2 = datas.index[1]        
        
        params3 = list(df.columns)
        
        player3 = df.loc[[p1]].reset_index()
        player3 = list(player3.loc[0])
        player3 = player3[1:]
        
        values3 = []
        for x in range(len(params3)):
            values3.append(math.floor(stats.percentileofscore(df[params3[x]],player3[x])))
       
        player4 = df.loc[[p2]].reset_index()
        player4 = list(player4.loc[0])
        player4 = player4[1:]
        
        values4 = []
        for x in range(len(params3)):
            values4.append(math.floor(stats.percentileofscore(df[params3[x]],player4[x]))) 
            
        comparison_graph(params3, p1, values3, p2, values4)
###########################################################################
###########################################################################

        
except Exception as e:
    st.error(f"Error: {str(e)}")
    st.error(f"Line causing the error: {sys.exc_info()[-1].tb_lineno}")