from plotly.offline import init_notebook_mode, iplot
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

data = './data_galicia_covid.csv'

df = pd.read_csv(data)

fig = go.Figure()

fig.add_trace(go.Indicator(
    mode = "number+delta",
    value = df["Total casos"].tail(1).values[0],
    domain = {'x': [0, 0.5], 'y': [0.75, 1]},
    delta = {'reference': df["Total casos"].tail(2).values[0], 'position' : "bottom",'valueformat':'f',
            'increasing':{'color':'red'},'decreasing':{'color':'green'}},
    number = {'valueformat':'f'},
    title = "Total de casos"))

fig.add_trace(go.Indicator(
    mode = "number+delta",
    value = df["Total casos"].tail(1).values[0]-df["Total altas"].tail(1).values[0]-df["Total fallecidos"].tail(1).values[0],
    domain = {'x': [0.5, 1], 'y': [0.75, 1]},
    delta = {'reference': df["Total casos"].tail(2).values[0]-df["Total altas"].tail(2).values[0]-df["Total fallecidos"].tail(2).values[0], 'position' : "bottom",'valueformat':'f',
            'increasing':{'color':'red'},'decreasing':{'color':'green'}},
    number = {'valueformat':'f'},
    title = "Casos activos"))

fig.add_trace(go.Indicator(
    mode = "number+delta",
    value = df["Total altas"].tail(1).values[0],
    domain = {'x': [0, 0.5], 'y': [0.35, 0.6]},
    delta = {'reference': df["Total altas"].tail(2).values[0], 'position' : "bottom",'valueformat':'f',
            'increasing':{'color':'green'},'decreasing':{'color':'red'}},
    number = {'valueformat':'f'},
    title = "Total de altas"))

fig.add_trace(go.Indicator(
    mode = "number+delta",
    value = df["Total fallecidos"].tail(1).values[0],
    domain = {'x': [0.5, 1], 'y': [0.35, 0.6]},
    delta = {'reference': df["Total fallecidos"].tail(2).values[0], 'position' : "bottom",'valueformat':'f',
            'increasing':{'color':'red'},'decreasing':{'color':'green'}},
    number = {'valueformat':'f'},
    title = "Total de fallecidos"))

fig.add_trace(go.Indicator(
    mode = "number+delta",
    value = df["Hospitalizados"].tail(1).values[0],
    domain = {'x': [0, 0.5], 'y': [0, 0.25]},
    delta = {'reference': df["Hospitalizados"].tail(2).values[0], 'position' : "bottom",'valueformat':'f',
            'increasing':{'color':'red'},'decreasing':{'color':'green'}},
    number = {'valueformat':'f'},
    title = "Total de hospitalizados"))

fig.add_trace(go.Indicator(
    mode = "number+delta",
    value = df["UCI"].tail(1).values[0],
    domain = {'x': [0.5, 1], 'y': [0, 0.25]},
    delta = {'reference': df["UCI"].tail(2).values[0], 'position' : "bottom",'valueformat':'f',
            'increasing':{'color':'red'},'decreasing':{'color':'green'}},
    number = {'valueformat':'f'},
    title = "Total UCIs"))

fig.write_html('./docs/total_cases.html')

layout=go.Layout(title = 'Evolución de nuevos casos en Galicia')
data = go.Scatter(x=df["Fecha"],y=df["Nuevos casos"],mode='lines',name="Evolución de nuevos casos")

fig = go.Figure(data,layout)

fig.write_html("./docs/historian_new_cases_galicia.html")

