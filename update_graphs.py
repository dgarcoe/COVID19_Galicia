from plotly.offline import init_notebook_mode, iplot
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import geojson
import locale
from datetime import date

locale.setlocale(locale.LC_ALL,'es_ES.UTF-8')


#Read datasets
data = './data_galicia_covid.csv'

df = pd.read_csv(data)

df["Fecha"] = pd.to_datetime(df["Fecha"],format="%d/%m/%Y")

df["Día semana"] = df["Fecha"].dt.day_name()
df["Semana"] = df["Fecha"].dt.week
df["Mes"] = df["Fecha"].dt.month_name()

#Plot key indicators
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
    value = df["Total casos"].tail(1).values[0]-df["Total altas"].tail(1).values[0]-df["Total fallecidos"].tail(2).values[0],
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

#Plot evolution of new cases
layout=go.Layout(title = 'Evolución de nuevos casos en Galicia')
data = go.Scatter(x=df["Fecha"],y=df["Nuevos casos"],mode='lines',name="Evolución de nuevos casos")

fig = go.Figure(data,layout)

fig.update_xaxes(
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    )
)

fig.write_html("./docs/historian_new_cases_galicia.html")


#Plot evolution of active cases
layout=go.Layout(title = 'Evolución de casos activos en Galicia')
data = go.Scatter(x=df["Fecha"],y=df["Total casos"]-df["Total altas"]-df["Total fallecidos"],mode='lines',name="Evolución de casos activos")

fig = go.Figure(data,layout)

fig.update_xaxes(
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    )
)

fig.write_html("./docs/historian_active_cases_galicia.html")

#Plot evolution of letality rate
layout=go.Layout(title = 'Evolución de la tasa de letalidad en Galicia (%)')
data = go.Scatter(x=df["Fecha"],y=df["Tasa de letalidad"],mode='lines',name="Evolución de la tasa de letalidad")

fig = go.Figure(data,layout)

fig.update_xaxes(
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    )
)

fig.write_html("./docs/letality_rate_evolution.html")

#Plot new cases and cured per region
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

#Plot evolution of hospital occupation
fig = go.Figure()

fig.add_trace(go.Scatter(x=df["Fecha"],y=df["Hospitalizados"],mode='lines',name="Hospitalizados",fill='tonexty'))
fig.add_trace(go.Scatter(x=df["Fecha"],y=df["UCI"],mode='lines',name="UCI",fill='tozeroy'))

fig.update_layout( title="Evolución de la ocupación hospitalaria",
    xaxis_title="",
    yaxis_title="")

fig.update_xaxes(
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    )
)

fig.write_html("./docs/evolution_hospital_occupation.html")

#Plot incidence rate indicators
fig = go.Figure()

fig.add_trace(go.Indicator(
    mode = "number+gauge+delta",
    gauge = {'shape': "bullet", 'axis': {'range': [None, 600]},
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
    gauge = {'shape': "bullet", 'axis': {'range': [None, 600]},
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

#Plot incidence rate by region
with open('Areas_sanitarias.geojson',encoding='utf-8') as f:
    gj_regions = geojson.load(f)

data = [["A Coruña y Cee",df["IA 14 Coruna"].tail(1).values[0],df["IA 7 Coruna"].tail(1).values[0]],
       ["Ferrol",df["IA 14 Ferrol"].tail(1).values[0],df["IA 7 Ferrol"].tail(1).values[0]],
       ["Lugo, A Mariña y Monforte de Lemos",df["IA 14 Lugo"].tail(1).values[0],df["IA 7 Lugo"].tail(1).values[0]],
        ["Ourense, Verín y O Barco de Valdeorras",df["IA 14 Ourense"].tail(1).values[0],df["IA 7 Ourense"].tail(1).values[0]],
       ["Pontevedra y O Salnés",df["IA 14 Pontevedra"].tail(1).values[0],df["IA 7 Pontevedra"].tail(1).values[0]],
       ["Santiago de Compostela y Barbanza",df["IA 14 Santiago"].tail(1).values[0],df["IA 7 Santiago"].tail(1).values[0]],
       ["Vigo",df["IA 14 Vigo"].tail(1).values[0],df["IA 7 Vigo"].tail(1).values[0]]]

df_areas = pd.DataFrame(data,columns=['Area','IA 14','IA 7'])

df_areas["Riesgo IA 14"] = pd.cut(x=df_areas["IA 14"],bins = [0,25,50,150,250,5000],
                                  labels=['Normal','Bajo','Medio','Alto','Extremo'])


df_areas["Riesgo IA 7"] = pd.cut(x=df_areas["IA 7"],bins = [0,10,25,75,125,5000],
                                  labels=['Normal','Bajo','Medio','Alto','Extremo'])

colour_discrete_scale = {'Normal':'lightgreen','Bajo':'khaki','Medio':'orange','Alto':'orangered','Extremo':'darkred'}
categories = {'Riesgo IA 14': ['Extremo','Alto','Medio','Normal','Bajo']}


#fig = px.choropleth_mapbox(df_areas, geojson=gj_regions, locations='Area', featureidkey='properties.nom_area',
#                           color='Riesgo IA 14',#
#                           color_discrete_map=colo#ur_discrete_scale,
#                           category_orders=categorie#s,
#                           mapbox_style="white-bg",
#                           zoom=7.1, height = 800, center = {"lat": 42.789886, "lon": -8.003869},
#                           opacity=1,
#                           hover_name='Area',
#                           hover_data={"Area":False,"Riesgo IA 14":False,"IA 14":True}
#                          )

#fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

#fig.write_html("./docs/risk_region_IA14.html")

#fig = px.choropleth_mapbox(df_areas, geojson=gj_regions, locations='Area', featureidkey='properties.nom_area',
#                           color='Riesgo IA 7',
#                           color_discrete_map=colour_discrete_scale,
#                           category_orders=categories,
#                           mapbox_style="white-bg",
#                           zoom=7.1, height = 600, center = {"lat": 42.789886, "lon": -8.003869},
#                           opacity=1,
#			   hover_name='Area',
#			   hover_data={"Area":False,"Riesgo IA 7":False,"IA 7":True}
#                          )
#fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

#fig.write_html("./docs/risk_region_IA7.html")

#Plot 2020 heatmap of new cases
df_year = df[df['Fecha'].dt.year == 2020]

order_heatmap = ['Sunday','Saturday','Friday','Thursday','Wednesday','Tuesday','Monday']

fig = go.Figure(data=go.Heatmap(
        z=df_year["Nuevos casos"],
        x=df_year["Semana"],
        y=df_year["Día semana"],
        colorscale='YlOrRd',hoverongaps = False))

fig.update_layout(
    title='Nuevos casos por semana y día de la semana',
    yaxis={'categoryarray':order_heatmap,'showgrid':False},
    xaxis={'showgrid':False},
    xaxis_title="Semana",
    yaxis_title="Día dela semana")

fig.write_html("./docs/heatmap_new_cases_2020.html")

#Plot 2020 boxplot of new cases
order_boxplot = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

fig = go.Figure()
fig.add_trace(go.Box(y=df_year["Nuevos casos"],x=df_year["Mes"],boxmean=True,fillcolor='rgba(255, 65, 54, 0.5)'))
fig.update_layout(
    title='Distribución de nuevos casos por mes',
    xaxis={'categoryarray':order_boxplot},
    )

fig.write_html("./docs/boxplot_new_cases_month_2020.html")

#Plot 2021 heatmap of new cases
df_year = df[df['Fecha'].dt.year == 2021]

order_heatmap = ['Sunday','Saturday','Friday','Thursday','Wednesday','Tuesday','Monday']

fig = go.Figure(data=go.Heatmap(
        z=df_year["Nuevos casos"],
        x=df_year["Semana"],
        y=df_year["Día semana"],
        colorscale='YlOrRd',hoverongaps = False))

fig.update_layout(
    title='Nuevos casos por semana y día de la semana',
    yaxis={'categoryarray':order_heatmap,'showgrid':False},
    xaxis={'showgrid':False},
    xaxis_title="Semana",
    yaxis_title="Día dela semana")

fig.write_html("./docs/heatmap_new_cases_2021.html")

#Plot 2021 boxplot of new cases
order_boxplot = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

fig = go.Figure()
fig.add_trace(go.Box(y=df_year["Nuevos casos"],x=df_year["Mes"],boxmean=True,fillcolor='rgba(255, 65, 54, 0.5)'))
fig.update_layout(
    title='Distribución de nuevos casos por mes',
    xaxis={'categoryarray':order_boxplot},
    )

fig.write_html("./docs/boxplot_new_cases_month_2021.html")

#Plot distribution of cases by region

death_values = [df["Total Fallecidos Vigo"].tail(1).values[0],
               df["Total Fallecidos Santiago"].tail(1).values[0],
               df["Total Fallecidos Pontevedra"].tail(1).values[0],
               df["Total Fallecidos Ourense"].tail(1).values[0],
               df["Total Fallecidos Lugo"].tail(1).values[0],
               df["Total Fallecidos Ferrol"].tail(1).values[0],
               df["Total Fallecidos A Coruna"].tail(1).values[0]]

cured_values = [df["Total Altas Vigo"].tail(1).values[0],
               df["Total Altas Santiago"].tail(1).values[0],
               df["Total Altas Pontevedra"].tail(1).values[0],
               df["Total Altas Ourense"].tail(1).values[0],
               df["Total Altas Lugo"].tail(1).values[0],
               df["Total Altas Ferrol"].tail(1).values[0],
               df["Total Altas A Coruna"].tail(1).values[0]]

active_values = [df["Total Casos Vigo"].tail(1).values[0]-cured_values[0]-death_values[0],
               df["Total Casos Santiago"].tail(1).values[0]-cured_values[1]-death_values[1],
               df["Total Casos Pontevedra"].tail(1).values[0]-cured_values[2]-death_values[2],
               df["Total Casos Ourense"].tail(1).values[0]-cured_values[3]-death_values[3],
               df["Total Casos Lugo"].tail(1).values[0]-cured_values[4]-death_values[4],
               df["Total Casos Ferrol"].tail(1).values[0]-cured_values[5]-death_values[5],
               df["Total Casos A Coruna"].tail(1).values[0]-cured_values[6]]

fig = go.Figure()

fig.add_trace(go.Bar(x=death_values, y=["Vigo","Santiago","Pontevedra","Ourense","Lugo","Ferrol","A Coruña"], orientation='h',
                     name='Fallecidos', marker_color='indianred'))

fig.add_trace(go.Bar(x=active_values, y=["Vigo","Santiago","Pontevedra","Ourense","Lugo","Ferrol","A Coruña"], orientation='h',
                    name='Casos activos',marker_color='coral'))

fig.add_trace(go.Bar(x=cured_values, y=["Vigo","Santiago","Pontevedra","Ourense","Lugo","Ferrol","A Coruña"], orientation='h',
                    name='Curados',marker_color='forestgreen'))

fig.update_layout( title="Reparto de estadísticas por área sanitaria",
    xaxis_title="",
    yaxis_title="",barmode='stack')
fig.write_html('./docs/case_distribution_region.html')

#Plot IA 7 by region
fig = go.Figure()

data = [df["IA 7 Vigo"].tail(1).values[0],df["IA 7 Santiago"].tail(1).values[0],df["IA 7 Pontevedra"].tail(1).values[0],
       df["IA 7 Ourense"].tail(1).values[0],df["IA 7 Lugo"].tail(1).values[0],df["IA 7 Ferrol"].tail(1).values[0],
       df["IA 7 Coruna"].tail(1).values[0]]

fig = make_subplots(specs=[[{"secondary_y": True}]], print_grid=False)

fig.add_trace(go.Bar(x=data, y=["Vigo","Santiago","Pontevedra","Ourense","Lugo","Ferrol","A Coruña"], orientation='h',
                     marker_color='darkblue',showlegend= False),secondary_y=False)
fig.add_trace(go.Scatter(y= [0, 1],
                  x= [125, 125],
                  mode= 'lines',
                  showlegend= False,
                  hoverinfo='none',marker_color='indianred'),secondary_y=True)

fig.add_trace(go.Scatter(y= [0, 1],
                  x= [10, 10],
                  mode= 'lines',
                  showlegend= False,
                  hoverinfo='none',marker_color='lightgreen'),secondary_y=True)

fig.update_layout( title="IA a 7 días por área sanitaria",
    xaxis_title="",
    yaxis_title="",yaxis2= dict(fixedrange= True,range= [0, 1],visible= False))

fig.write_html("./docs/IA7_regions.html")


#Plot IA 14 by regions
fig = go.Figure()

data = [df["IA 14 Vigo"].tail(1).values[0],df["IA 14 Santiago"].tail(1).values[0],df["IA 14 Pontevedra"].tail(1).values[0],
       df["IA 14 Ourense"].tail(1).values[0],df["IA 14 Lugo"].tail(1).values[0],df["IA 14 Ferrol"].tail(1).values[0],
       df["IA 14 Coruna"].tail(1).values[0]]

fig = make_subplots(specs=[[{"secondary_y": True}]], print_grid=False)

fig.add_trace(go.Bar(x=data, y=["Vigo","Santiago","Pontevedra","Ourense","Lugo","Ferrol","A Coruña"], orientation='h',
                     marker_color='darkblue',showlegend= False),secondary_y=False)
fig.add_trace(go.Scatter(y= [0, 1],
                  x= [250, 250],
                  mode= 'lines',
                  showlegend= False,
                  hoverinfo='none',marker_color='indianred'),secondary_y=True)

fig.add_trace(go.Scatter(y= [0, 1],
                  x= [25, 25],
                  mode= 'lines',
                  showlegend= False,
                  hoverinfo='none',marker_color='lightgreen'),secondary_y=True)

fig.update_layout( title="IA a 14 días por área sanitaria",
    xaxis_title="",
    yaxis_title="",yaxis2= dict(fixedrange= True,range= [0, 1],visible= False))

fig.write_html('./docs/IA14_regions.html')

#Plot case evolution by region
fig = go.Figure()

fig.add_trace(go.Scatter(x=df["Fecha"],y=(df["Total Casos A Coruna"]-df["Total Altas A Coruna"]-df["Total Fallecidos A Coruna"]),mode='lines',name="Casos activos A Coruña"))
fig.add_trace(go.Scatter(x=df["Fecha"],y=(df["Total Casos Ferrol"]-df["Total Altas Ferrol"]-df["Total Fallecidos Ferrol"]),mode='lines',name="Casos activos Ferrol"))
fig.add_trace(go.Scatter(x=df["Fecha"],y=(df["Total Casos Lugo"]-df["Total Altas Lugo"]-df["Total Fallecidos Lugo"]),mode='lines',name="Casos activos Lugo"))
fig.add_trace(go.Scatter(x=df["Fecha"],y=(df["Total Casos Ourense"]-df["Total Altas Ourense"]-df["Total Fallecidos Ourense"]),mode='lines',name="Casos activos Ourense"))
fig.add_trace(go.Scatter(x=df["Fecha"],y=(df["Total Casos Pontevedra"]-df["Total Altas Pontevedra"]-df["Total Fallecidos Pontevedra"]),mode='lines',name="Casos activos Pontevedra"))
fig.add_trace(go.Scatter(x=df["Fecha"],y=(df["Total Casos Santiago"]-df["Total Altas Santiago"]-df["Total Fallecidos Santiago"]),mode='lines',name="Casos activos Santiago"))
fig.add_trace(go.Scatter(x=df["Fecha"],y=(df["Total Casos Vigo"]-df["Total Altas Vigo"]-df["Total Fallecidos Vigo"]),mode='lines',name="Casos activos Vigo"))

fig.update_layout( title="Evolución de casos activos por área sanitaria",
    xaxis_title="",
    yaxis_title="")

fig.update_xaxes(range=["2020-06-04", date.today()])

fig.update_xaxes(
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    )
)

fig.write_html("./docs/evolution_active_cases_region.html")
