from plotly.offline import init_notebook_mode, iplot
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import locale
from datetime import date

locale.setlocale(locale.LC_ALL,'es_ES.UTF-8')

#Read dataset
data_vac = './data_galicia_vaccination.csv'
df_vac = pd.read_csv(data_vac)

data = './data_galicia_covid.csv'
df = pd.read_csv(data)


df_vac["Fecha"] = pd.to_datetime(df_vac["Fecha"],format="%d/%m/%Y")

#Plot vaccination data
fig = go.Figure()

fig.add_trace(go.Indicator(
    mode = "number+delta",
    value = df_vac["Personas vacunadas"].tail(1).values[0],
    domain = {'x': [0, 0.5], 'y': [0, 1]},
    delta = {'reference': df_vac["Personas vacunadas"].tail(2).values[0], 'position' : "bottom",'valueformat':'f',
            'increasing':{'color':'green'}},
    number = {'valueformat':'f'},
    title = "Total de personas vacunadas"))

fig.add_trace(go.Indicator(
    mode = "number+delta",
    value = df_vac["Personas vacunadas"].tail(1).values[0]/df["Poblacion Galicia"].tail(1).values[0],
    domain = {'x': [0.5, 1], 'y': [0, 1]},
    delta = {'reference': df_vac["Personas vacunadas"].tail(2).values[0]/df["Poblacion Galicia"].tail(2).values[0],
             'position' : "bottom",'valueformat':'.2%',
            'increasing':{'color':'green'}},
    number = {'valueformat':'.2%'},
    title = "Porcentaje de población vacunada"))

fig.write_html("./docs/total_vaccinated.html")

fig = go.Figure()

fig.add_trace(go.Scatter(x=df_vac["Fecha"],y=df_vac["Personas vacunadas"],mode='lines',name="Personas vacunadas",marker_color='forestgreen',fill='tozeroy'))
fig.add_trace(go.Scatter(x=df_vac["Fecha"],y=df_vac["Dosis administradas"],mode='lines',name="Dosis administradas",marker_color='lightgreen',fill='tonexty'))
fig.add_trace(go.Scatter(x=df_vac["Fecha"],y=df_vac["Dosis entregadas"],mode='lines',name="Dosis entregadas",marker_color='dodgerblue',fill='tonexty'))

fig.update_layout( title="Evolución de la vacunación en Galicia",
    xaxis_title="",
    yaxis_title="")

fig.write_html("./docs/vaccination_evolution_galicia.html")

fig = go.Figure([go.Bar(y=["Pfizer","AstraZeneca","Moderna","Janssen"], x=[df_vac["Dosis entregadas Pfizer"].tail(1).values[0],df_vac["Dosis entregadas AstraZeneca"].tail(1).values[0],df_vac["Dosis entregadas Moderna"].tail(1).values[0],df_vac["Dosis entregadas Janssen"].tail(1).values[0]], orientation='h')])
fig.update_layout( title="Dosis entregadas de vacunas por empresa farmacéutica")

fig.write_html("./docs/vaccination_distribution_by_company.html")
