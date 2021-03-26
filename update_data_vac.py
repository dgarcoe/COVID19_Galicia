import os
import requests
from datetime import date, timedelta, datetime
import pandas as pd
import numpy as np

data = './data_galicia_vaccination.csv'

df = pd.read_csv(data)

today = date.today()

print('Beginning files download')

url = 'https://www.mscbs.gob.es/profesionales/saludPublica/ccayes/alertasActual/nCov/documentos/Informe_Comunicacion_'+str(today).replace('-','')+'.ods'
filename = './'+str(today)+'_Vac.ods'
r = requests.get(url)
with open(filename, 'wb') as f:
    f.write(r.content)
    print(filename+' downloaded')

print('Files saved')

df_day = pd.read_excel(filename, engine="odf")

galicia_vac = df_day.iloc[11,:]

last_day = galicia_vac.loc["Fecha de la última vacuna registrada (2)"].date()

new_date = last_day.strftime('%d/%m/%Y')
new_delivered = galicia_vac.loc["Total Dosis entregadas (1)"]
new_adm = galicia_vac.loc["Dosis administradas (2)"]
new_pfizer = galicia_vac.loc["Dosis entregadas Pfizer (1)"]
new_moderna = galicia_vac.loc["Dosis entregadas Moderna (1)"]
new_astra = galicia_vac.loc["Dosis entregadas AstraZeneca (1)"]
new_tot_vac = galicia_vac.loc["Nº Personas vacunadas(pauta completada)"]

df_new_row = pd.DataFrame([[new_date,new_delivered,new_adm,new_pfizer,new_moderna,new_astra,new_tot_vac]],columns=df.keys())


df = df.append(df_new_row)

df.to_csv(data,index=False)

print('Dataset updated')

os.remove(filename)
