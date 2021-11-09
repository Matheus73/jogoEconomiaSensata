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

from .models import Answer
from user.models import User

from random import random  # APAGAR no oficial

from django_plotly_dash import DjangoDash

app = DjangoDash('SimpleExample')


def graph(x, y1, y2, color1, color2):
    data = go.Bar(
        x=x,
        y=y1,
        marker={'color': color1},
        #text = y1,
        textfont={'size': 14},
        textposition='outside',
        name='Resultado sozinho'
    )

    data2 = go.Bar(
        x=x,
        y=y2,
        marker={'color': color2},
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


paises = sorted([i.country for i in User.objects.all()])

ministerios = ['paises', 'Agricultura', 'Educação', 'Meio Ambiente',
               'Saúde', 'Ciência', 'Desenvolvimento', 'Banco Central', 'Economia']

tuples = []
for i in Answer.objects.all():
    leader = i.leader
    tuples.append([leader.country, i.result_agricultura, i.result_educacao, i.result_ambiente,
                   i.result_saude, i.result_infraestrutura, i.result_desenvolvimento,
                   i.result_bancoCentral, i.result_economia])

df = pd.DataFrame(tuples, columns=ministerios)
print(df.head())

somas = {}
for i in df["paises"]:
    soma = 0
    for j in df[df["paises"] == i].iloc[:, 1:].sum():
        soma += j
    somas[i] = soma

print(somas)
# Resultados

total = [random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() *
         100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100]

users = User.objects.all()
blocos = {}
for i in users:
    if i.bloc in blocos.keys():
        blocos[i.bloc].append(i.country)
    else:
        blocos[i.bloc] = [i.country]
print(blocos)
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
print(blocos)

somas_final = {}
for i in somas:
    user = User.objects.filter(country=i)[0]
    somas_final[i] = somas[i] + (0.1 * blocos[user.bloc]['media'])
print(somas_final)

fig_total = graph(list(somas.keys()), list(somas.values()),
                  list(somas_final.values()), '#e99e2a', '#bdc3c7')

app.layout = html.Div([
    H4('Ranking por ministério'),

    # Ranking por ministério
    dbc.Row([
            dbc.Col(
                Div([
                    Dropdown(
                        id='meu_dropdown',
                        value='Argentina',
                        options=[
                            {'label': x, 'value': x} for x in paises
                        ]
                    ),
                    #H4('Ministério da Agricultura e Desenvolvimento rural'),
                    dcc.Graph(
                        id='Gráfico ministério da agricultura e desenvolvimento',
                        config={'displayModeBar': False},
                        figure={}
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
                        figure=fig_total
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
        nome_pais = ''

    ministerios = ['paises', 'Agricultura', 'Educação', 'Meio Ambiente',
                   'Saúde', 'Ciência', 'Desenvolvimento', 'Banco Central', 'Economia']

    tuples = []
    for i in Answer.objects.all():
        leader = i.leader
        tuples.append([leader.country, i.result_agricultura, i.result_educacao, i.result_ambiente,
                       i.result_saude, i.result_infraestrutura, i.result_desenvolvimento,
                       i.result_bancoCentral, i.result_economia])

    df = pd.DataFrame(tuples, columns=ministerios)
    # print(df.head())
    # df['paises'] = paises * 10

    data = go.Scatter(
        x=df[df['paises'] == nome_pais].sum().index[1:],
        y=df[df['paises'] == nome_pais].sum()[1:],
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
