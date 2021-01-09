from plotly.offline import init_notebook_mode, iplot
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import geojson

data = './data_galicia_covid.csv'
data_vac = './data_galicia_vaccination.csv'

df = pd.read_csv(data)
df_vac = pd.read_csv(data_vac)

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

fig = go.Figure()

fig.add_trace(go.Scatter(x=df_vac["Fecha"],y=df_vac["Dosis entregadas"],mode='lines',name="Dosis entregadas",fill='tonexty'))
fig.add_trace(go.Scatter(x=df_vac["Fecha"],y=df_vac["Dosis administradas"],mode='lines',name="Dosis administradas",fill='tozeroy',marker_color='lightgreen'))

fig.update_layout( title="Evolución de la vacunación en Galicia",
    xaxis_title="",
    yaxis_title="")

fig.write_html("./docs/vaccination_evolution_galicia.html")


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

df_areas["Riesgo IA 14"] = pd.cut(x=df_areas["IA 14"],bins = [0,25,50,150,250,1000], 
                                  labels=['Normal','Bajo','Medio','Alto','Extremo'])

df_areas["Riesgo IA 7"] = pd.cut(x=df_areas["IA 7"],bins = [0,10,25,75,125,1000], 
                                  labels=['Normal','Bajo','Medio','Alto','Extremo'])

colour_discrete_scale = {'Normal':'lightgreen','Bajo':'khaki','Medio':'orange','Alto':'orangered','Extremo':'darkred'}
categories = {'Riesgo IA 14': ['Extremo','Alto','Medio','Normal','Bajo']}

    
fig = px.choropleth_mapbox(df_areas, geojson=gj_regions, locations='Area', featureidkey='properties.nom_area', 
                           color='Riesgo IA 14',
                           color_discrete_map=colour_discrete_scale,
                           category_orders=categories,
                           mapbox_style="white-bg",
                           zoom=7.1, height = 600, center = {"lat": 42.789886, "lon": -8.003869},
                           opacity=1,
                           hover_name='Area',
                           hover_data={"Area":False,"Riesgo IA 14":False,"IA 14":True}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

fig.write_html("./docs/risk_region_IA14.html")

fig = px.choropleth_mapbox(df_areas, geojson=gj_regions, locations='Area', featureidkey='properties.nom_area',
                           color='Riesgo IA 7',
                           color_discrete_map=colour_discrete_scale,
                           category_orders=categories,
                           mapbox_style="white-bg",
                           zoom=7.1, height = 600, center = {"lat": 42.789886, "lon": -8.003869},
                           opacity=1,
			   hover_name='Area',
			   hover_data={"Area":False,"Riesgo IA 7":False,"IA 7":True}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

fig.write_html("./docs/risk_region_IA7.html")
