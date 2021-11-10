import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from dash_html_components import Div, H1, H2, H3, H4
from dash_core_components import Dropdown, Checklist
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output

from .models import Answer
from user.models import User
from form.models import Form

from random import random  # APAGAR no oficial

from django_plotly_dash import DjangoDash

app = DjangoDash('SimpleExample')

paises = sorted([i.country for i in User.objects.all(
) if i.country is not None])


formularios = sorted([i.name for i in Form.objects.all()])

ministerios = ['paises', 'Agricultura', 'Educação', 'Meio Ambiente',
               'Saúde', 'Ciência', 'Desenvolvimento', 'Banco Central', 'Economia']


app.layout = html.Div([
    H4('Ranking por ministério'),

    # Ranking por ministério
    dbc.Row([
            dbc.Col(
                Div([
                    Dropdown(
                        id='meu_dropdown',
                        value='',
                        options=[
                            {'label': x, 'value': x} for x in paises
                        ]
                    ),
                    Checklist(
                        id='my_checklist',
                        value=['2023'],
                        options=[
                            {'label': x, 'value': x} for x in formularios
                        ],
                        labelStyle={'display': 'inline-block'}
                    ),
                    #H4('Ministério da Agricultura e Desenvolvimento rural'),
                    dcc.Graph(
                        id='Gráfico ministério da agricultura e desenvolvimento',
                        config={'displayModeBar': False},
                        figure={}
                    ),
                    dcc.Interval(
                        id='interval-component',
                        interval=1*1000, # in milliseconds
                        n_intervals=0
                    )
                ]),
                width=12)]),

    # Ranking dos países
    H4('Ranking Geral'),
    dbc.Row([
            dbc.Col(
                Div([
                    dcc.Graph(
                        id='Gráfico total',
                        config={'displayModeBar': False},
                        figure={}
                    ),
                    dcc.Interval(
                        id='interval-component',
                        interval=1*1000, # in milliseconds
                        n_intervals=0
                    )
                ]),
                width=12)]),


])


@app.callback(
    Output('Gráfico ministério da agricultura e desenvolvimento', 'figure'),
    [Input('meu_dropdown', 'value'), Input('my_checklist', 'value'), Input('interval-component', 'n_intervals')],
)
def my_callback(nome_pais, formulario, n):
    if not nome_pais:
        nome_pais = ''

    ministerios = ['paises', 'Ano', 'Agricultura', 'Educação', 'Meio Ambiente',
                   'Saúde', 'Ciência', 'Desenvolvimento', 'Banco Central',
                   'Economia']
    
    tuples = []
    for i in Answer.objects.all():
        leader = i.leader
        form = i.form
        tuples.append([leader.country, form.name, i.result_agricultura,
                       i.result_educacao, i.result_ambiente,
                       i.result_saude, i.result_infraestrutura,
                       i.result_desenvolvimento,
                       i.result_bancoCentral, i.result_economia])

    df = pd.DataFrame(tuples, columns=ministerios)
    # df['paises'] = paises * 10

    data = go.Scatter(
        x=df[(df['Ano'].isin(list(formulario))) & (
            df['paises'] == nome_pais)].sum().index[2:],
        y=df[(df['Ano'].isin(list(formulario))) &
             (df['paises'] == nome_pais)].sum()[2:],
        marker={'color': '#b86224'},
        #text = y,
        textfont={'size': 14},
        # textposition = 'outside'
    )

    configuracoes_layout = go.Layout(
        title={
            'text': f'Rank para {nome_pais}',
            'font': {'size': 20},
            'x': 0.5,
            'xanchor': 'center',
            'font': {'color': '#bdc3c7'}
        },
        xaxis={
            'title': 'Países',
            'titlefont': {'color': '#bdc3c7'},
            'tickfont': {'size': 12},
        },
        yaxis={
            'title': 'Valor para Cada Ministério',
            'titlefont': {'color': '#bdc3c7'}
        },
        template='plotly_white'
    )

    fig = go.Figure(data=data, layout=configuracoes_layout)
    return fig

@app.callback(
    Output('Gráfico total', 'figure'),
    [Input('interval-component', 'n_intervals')],
)

def my_graph(n):
    
    tuples = []
    for i in Answer.objects.all():
        leader = i.leader
        tuples.append([leader.country, i.result_agricultura, i.result_educacao, i.result_ambiente,
                    i.result_saude, i.result_infraestrutura, i.result_desenvolvimento,
                    i.result_bancoCentral, i.result_economia])

    df = pd.DataFrame(tuples, columns=ministerios)

    somas = {}
    for i in df["paises"]:
        soma = 0
        for j in df[df["paises"] == i].iloc[:, 1:].sum():
            soma += j
        somas[i] = soma

    # Resultados

    users = User.objects.all()
    blocos = {}
    for i in users:
        if i.bloc in blocos.keys():
            blocos[i.bloc].append(i.country)
        else:
            blocos[i.bloc] = [i.country]
    for i in blocos:
        soma = 0
        for j in blocos[i]:
            valor = somas.get(j)
            if valor:
                soma += valor
            else:
                soma += 0
        blocos[i] = {"paises": blocos[i],
                    "soma": soma, "media": soma/len(blocos[i])}

    somas_final = {}
    for i in somas:
        user = User.objects.filter(country=i)[0]
        somas_final[i] = somas[i] + (0.1 * blocos[user.bloc]['media'])
    

    data = go.Bar(
        x=list(somas.keys()),
        y=list(somas.values()),
        marker={'color': '#e99e2a'},
        #text = y1,
        textfont={'size': 14},
        textposition='outside',
        name='Resultado sozinho'
    )

    data2 = go.Bar(
        x=list(somas.keys()),
        y=list(somas_final.values()),
        marker={'color': '#bdc3c7'},
        #text = y2,
        textfont={'size': 14},
        textposition='outside',
        name='Resultado com o do grupo'
    )

    configuracoes_layout = go.Layout(
        # title = {
        # 'text': f'Rank para o {ministerio}',
        # 'font': {'size': 20},
        # 'x': 0.5,
        # 'xanchor': 'center',
        # 'font': {'color': '#bdc3c7'}
        # },
        xaxis={
            'title': 'Países',
            'titlefont': {'color': '#bdc3c7'},
            'tickfont': {'size': 12},
        },
        yaxis={
            'title': 'Valor Conquistado no Rodada',
            'titlefont': {'color': '#bdc3c7'}
        },
        template='plotly_white'
    )

    fig = go.Figure(data=[data, data2], layout=configuracoes_layout)
    return fig