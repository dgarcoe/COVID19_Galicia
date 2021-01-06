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

layout=go.Layout(title = 'Evolución de casos activos en Galicia')
data = go.Scatter(x=df["Fecha"],y=df["Total casos"]-df["Total altas"]-df['Total fallecidos'],mode='lines',name="Evolución de casos activos")

fig = go.Figure(data,layout)

fig.write_html("./docs/historian_active_cases_galicia.html")

layout=go.Layout(title = 'Evolución de la tasa de letalidad en Galicia (%)')
data = go.Scatter(x=df["Fecha"],y=df["Tasa de letalidad"],mode='lines',name="Evolución de la tasa de letalidad")

fig = go.Figure(data,layout)

fig.write_html("./docs/letality_rate_evolution.html")

last_values = [df["Total Casos Vigo"].tail(1).values[0]-df["Total Casos Vigo"].tail(2).values[0],
               df["Total Casos Santiago"].tail(1).values[0]-df["Total Casos Santiago"].tail(2).values[0],
               df["Total Casos Pontevedra"].tail(1).values[0]-df["Total Casos Pontevedra"].tail(2).values[0],
               df["Total Casos Ourense"].tail(1).values[0]-df["Total Casos Ourense"].tail(2).values[0],
               df["Total Casos Lugo"].tail(1).values[0]-df["Total Casos Lugo"].tail(2).values[0],
               df["Total Casos Ferrol"].tail(1).values[0]-df["Total Casos Ferrol"].tail(2).values[0],
               df["Total Casos A Coruna"].tail(1).values[0]-df["Total Casos A Coruna"].tail(2).values[0]]

last_cured_values = [df["Total Altas Vigo"].tail(1).values[0]-df["Total Altas Vigo"].tail(2).values[0],
               df["Total Altas Santiago"].tail(1).values[0]-df["Total Altas Santiago"].tail(2).values[0],
               df["Total Altas Pontevedra"].tail(1).values[0]-df["Total Altas Pontevedra"].tail(2).values[0],
               df["Total Altas Ourense"].tail(1).values[0]-df["Total Altas Ourense"].tail(2).values[0],
               df["Total Altas Lugo"].tail(1).values[0]-df["Total Altas Lugo"].tail(2).values[0],
               df["Total Altas Ferrol"].tail(1).values[0]-df["Total Altas Ferrol"].tail(2).values[0],
               df["Total Altas A Coruna"].tail(1).values[0]-df["Total Altas A Coruna"].tail(2).values[0]]

fig = go.Figure()

fig.add_trace(go.Bar(x=last_values, y=["Vigo","Santiago","Pontevedra","Ourense","Lugo","Ferrol","A Coruña"], orientation='h', 
                     name='Nuevos casos',text=last_values, textposition='inside',marker_color='indianred'))

fig.add_trace(go.Bar(x=last_cured_values, y=["Vigo","Santiago","Pontevedra","Ourense","Lugo","Ferrol","A Coruña"], orientation='h',
                    name='Altas',text=last_cured_values, textposition='inside',marker_color='forestgreen'))

fig.update_layout( title="Nuevos casos y altas por área sanitaria",
    xaxis_title="",
    yaxis_title="")

fig.write_html("./docs/bars_new_cases_cured.html")

fig = go.Figure()

fig.add_trace(go.Scatter(x=df["Fecha"],y=df["Hospitalizados"],mode='lines',name="Hospitalizados",fill='tonexty'))
fig.add_trace(go.Scatter(x=df["Fecha"],y=df["UCI"],mode='lines',name="UCI",fill='tozeroy'))

fig.update_layout( title="Evolución de la ocupación hospitalaria",
    xaxis_title="",
    yaxis_title="")

fig.write_html("./docs/evolution_hospital_occupation.html")

fig = go.Figure()

fig.add_trace(go.Indicator(
    mode = "number+gauge+delta",
    gauge = {'shape': "bullet", 'axis': {'range': [None, 400]},
             'threshold': {
                'line': {'color': "red", 'width': 2},
                'thickness': 0.75,
                'value': 250},
            'bar': {'color': "darkblue"},
             'steps': [
                {'range': [0, 25], 'color': "lightgreen"}]},
    delta = {'reference': df["IA 14"].tail(2).values[0],'increasing':{'color':'red'},'decreasing':{'color':'green'}},
    value = df["IA 14"].tail(1).values[0],
    domain = {'x': [0.1, 1], 'y': [0.5, 0.8]},
    title = {'text': "IA a 14 días"}))

fig.add_trace(go.Indicator(
    mode = "number+gauge+delta",
    gauge = {'shape': "bullet", 'axis': {'range': [None, 400]},
             'threshold': {
                'line': {'color': "red", 'width': 2},
                'thickness': 0.75,
                'value': 125},
            'bar': {'color': "darkblue"},
             'steps': [
                {'range': [0, 10], 'color': "lightgreen"}]},
    delta = {'reference': df["IA 7"].tail(2).values[0],'increasing':{'color':'red'},'decreasing':{'color':'green'}},
    value = df["IA 7"].tail(1).values[0],
    domain = {'x': [0.1, 1], 'y': [0, 0.3]},
    title = {'text': "IA a 7 días"}))

fig.update_layout( title="Incidencia Acumulada en Galicia")

fig.write_html("./docs/incidence_rate_galicia.html")
