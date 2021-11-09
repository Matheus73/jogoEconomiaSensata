import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from dash_html_components import Div, H1, H2, Img, P, Header, Span

from random import random #APAGAR no oficial


from django_plotly_dash import DjangoDash

app = DjangoDash('SimpleExample')


def graph(x, y, ministerio, color):
    data = go.Bar(
    x = x,
    y = y, 
    marker = {'color': color},
    text = y,
    textfont = {'size': 14},
    textposition = 'outside'
    )

    configuracoes_layout = go.Layout(
        title = {
            'text': f'Rank para o {ministerio}',
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
            'title': 'Valor Conquistado no Rodada', 
            'titlefont': {'color': '#bdc3c7'}
        },
        template='plotly_white'
    )

    fig = go.Figure(data=data, layout=configuracoes_layout)
    return fig

paises = ['Argentina', 'Australia', 'Brasil', 'Canadá', 'China', 'França', 'Alemanha', 'India', 'Indonésia', 'Italia', 'Japão', 'Coreia do Sul', 'México']

#Resultados
resultados_dos_usuarios_agricultura = [random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100]
resultados_dos_usuarios_educacao = [random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100]
resultados_dos_usuarios_clima= [random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100]
resultados_dos_usuarios_saude= [random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100]
resultados_dos_usuarios_ciencia = [random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100]
resultados_dos_usuarios_desenvolvimento = [random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100]
resultados_dos_usuarios_banco_central = [random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100]
resultados_dos_usuarios_economia = [random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100, random() * 100]


fig_agricultura = graph(paises, resultados_dos_usuarios_agricultura, 'ministério da Agricultura e Desenvolvimento rural', '#b86224')
fig_educacao = graph(paises, resultados_dos_usuarios_educacao, 'ministério da Educação', '#6c8eb0')
fig_clima = graph(paises, resultados_dos_usuarios_clima, 'ministério do Meio Ambiente', '#e99e2a')
fig_saude = graph(paises, resultados_dos_usuarios_saude, 'ministério da Saúde', '#c3aca0')
fig_ciencia = graph(paises, resultados_dos_usuarios_ciencia, 'ministério da Infraestreutura, Ciência e Tecnologia', '#1b1505')
fig_desenvolvimento = graph(paises, resultados_dos_usuarios_desenvolvimento, 'ministério do Desenvolvimento', '#db6e25')
fig_banco_central = graph(paises, resultados_dos_usuarios_banco_central, 'banco central', '#989998')
fig_economia = graph(paises, resultados_dos_usuarios_economia, 'ministério da economia', '#e99e2a')

app.layout = html.Div([
        H1('Dashboard'),
        
        #Agricultura
        H2('Ministério da Agricultura e Desenvolvimento rural'),
        dbc.Row([
            dbc.Col(
                Div([
                    dcc.Graph(
                        id = 'Gráfico ministério da agricultura e desenvolvimento',
                        config = {'displayModeBar': False},
                        figure = fig_agricultura
                        )
                    ]), 
                width=12)]),

        #Educação
        H2('Ministério da Educação'),
        dbc.Row([
            dbc.Col(
                Div([
                    dcc.Graph(
                        id = 'Gráfico ministério da educação',
                        config = {'displayModeBar': False},
                        figure = fig_educacao
                        )
                    ]), 
                width=12)]),
        
        #Clima
        H2('Ministério do Meio Ambiente'),
        dbc.Row([
            dbc.Col(
                Div([
                    dcc.Graph(
                        id = 'Gráfico ministério do Meio Ambiente',
                        config = {'displayModeBar': False},
                        figure = fig_clima
                        )
                    ]), 
                width=12)]),

        #Saúde
        H2('Ministério da Saúde'),
        dbc.Row([
            dbc.Col(
                Div([
                    dcc.Graph(
                        id = 'Gráfico ministério da saúde',
                        config = {'displayModeBar': False},
                        figure = fig_saude
                        )
                    ]), 
                width=12)]),

        #Ciência
        H2('Ministério da Infraestreutura, Ciência e Tecnologia'),
        dbc.Row([
            dbc.Col(
                Div([
                    dcc.Graph(
                        id = 'Gráfico ministério do Infraestreutura, Ciência e Tecnologia',
                        config = {'displayModeBar': False},
                        figure = fig_ciencia
                        )
                    ]), 
                width=12)]),
        
        #Desenvolvimento
        H2('Banco Central'),
        dbc.Row([
            dbc.Col(
                Div([
                    dcc.Graph(
                        id = 'Gráfico do ministério do Desenvolvimento',
                        config = {'displayModeBar': False},
                        figure = fig_desenvolvimento
                        )
                    ]), 
                width=12)]),
        
        #Banco Central
        H2('Banco Central'),
        dbc.Row([
            dbc.Col(
                Div([
                    dcc.Graph(
                        id = 'Gráfico banco central',
                        config = {'displayModeBar': False},
                        figure = fig_banco_central
                        )
                    ]), 
                width=12)]),

        #Economia
        H2('Ministério da Economia'),
        dbc.Row([
            dbc.Col(
                Div([
                    dcc.Graph(
                        id = 'Gráfico ministério da Economia',
                        config = {'displayModeBar': False},
                        figure = fig_economia
                        )
                    ]), 
                width=12)]),
])
