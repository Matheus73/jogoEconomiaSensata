import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from dash_html_components import Div, H1, H2, H3, H4
from dash_core_components import Dropdown
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output

from random import random #APAGAR no oficial

from django_plotly_dash import DjangoDash

app = DjangoDash('SimpleExample')


def graph(x, y1, y2, color1, color2):
    data = go.Bar(
    x = x,
    y = y1, 
    marker = {'color': color1},
    #text = y1,
    textfont = {'size': 14},
    textposition = 'outside',
    name ='Resultado sozinho'
    )

    data2 = go.Bar(
    x = x,
    y = y2, 
    marker = {'color': color2},
    #text = y2,
    textfont = {'size': 14},
    textposition = 'outside',
    name ='Resultado com o do grupo'
    )

    configuracoes_layout = go.Layout(
        #title = {
            #'text': f'Rank para o {ministerio}',
            #'font': {'size': 20},
            #'x': 0.5,
            #'xanchor': 'center',
            #'font': {'color': '#bdc3c7'}
        #},
        xaxis = {
            'title': 'Países',
            'titlefont': {'color': '#bdc3c7'},
            'tickfont': {'size': 12},
        },
        yaxis = {
            'title': 'Valor Conquistado no Rodada', 
            'titlefont': {'color': '#bdc3c7'}
        },
        template='plotly_white'
    )

    fig = go.Figure(data=[data, data2], layout=configuracoes_layout)
    return fig

paises = ['Argentina', 'Australia', 'Brasil', 'Canadá', 'China', 'França', 'Alemanha', 'India', 'Indonésia', 'Italia', 'Japão', 'Coreia do Sul', 'México']

#Resultados
total = [random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100]
total_2 = [random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100]


fig_total = graph(paises, total, total_2, '#e99e2a', '#bdc3c7')

app.layout = html.Div([
        H1('Dashboard'),
        
        #Ranking por ministério
        dbc.Row([
            dbc.Col(
                Div([
                    Dropdown(
                        id = 'meu_dropdown',
                        value='Argentina',
                        options=[
                            {'label': x, 'value': x} for x in paises
                        ]
                    ),
                    #H4('Ministério da Agricultura e Desenvolvimento rural'),
                    dcc.Graph(
                        id = 'Gráfico ministério da agricultura e desenvolvimento',
                        config = {'displayModeBar': False},
                        figure = {}
                        )
                    ]), 
                width=12)]),
        
        #Ranking dos países
        H4('Ranking Geral'),
        dbc.Row([
            dbc.Col(
                Div([
                    dcc.Graph(
                        id = 'Gráfico total',
                        config = {'displayModeBar': False},
                        figure = fig_total
                        )
                    ]), 
                width=12)]),

        
])

@app.callback(
    Output('Gráfico ministério da agricultura e desenvolvimento', 'figure'),
    Input('meu_dropdown', 'value'),
)

def my_callback(nome_pais):
    if nome_pais == None:
        nome_pais = 'Michelle'
    
    ministerios = ['Agricultura', 'Educação', 'Meio Ambiente', 'Saúde', 'Ciência', 'Desenvolvimento', 'Banco Central', 'Economia']
    paises = ['Argentina', 'Australia', 'Brasil', 'Canadá', 'China', 'França', 'Alemanha', 'India', 'Indonésia', 'Italia', 'Japão', 'Coreia do Sul', 'México', 'Rússia']

    df = pd.DataFrame(np.random.randint(0,100,size=(140, 8)), columns=ministerios)
    df['paises'] = paises * 10

    data = go.Bar(
        x =  df[df['paises'] == 'Argentina'].sum().index[:-1],
        y = df[df['paises'] == 'Argentina'].sum(), 
        marker = {'color': '#b86224'},
        #text = y,
        textfont = {'size': 14},
        textposition = 'outside'
    )

    configuracoes_layout = go.Layout(
        title = {
            'text': f'Rank para {nome_pais}',
            'font': {'size': 20},
            'x': 0.5,
            'xanchor': 'center',
            'font': {'color': '#bdc3c7'}
        },
        xaxis = {
            'title': 'Países',
            'titlefont': {'color': '#bdc3c7'},
            'tickfont': {'size': 12},
        },
        yaxis = {
            'title': 'Valor para Cada Ministério', 
            'titlefont': {'color': '#bdc3c7'}
        },
        template='plotly_white'
    )

    fig = go.Figure(data=data, layout=configuracoes_layout)
    return fig
