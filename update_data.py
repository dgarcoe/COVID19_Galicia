import os
import requests
from datetime import date, timedelta, datetime
import pandas as pd
import numpy as np

data = './data_galicia_covid.csv'

df = pd.read_csv(data)

#Data is updated at 6PM so we are going to download data from the previous day
today = date.today()
yesterday = today-timedelta(days=1)

print('Beginning files download')

url = 'https://coronavirus.sergas.gal/infodatos/'+str(yesterday)+'_COVID19_Web_CifrasTotais_PDIA.csv'
filename = './'+str(today)+'_Total.csv'
print(url)
r = requests.get(url)
with open(filename, 'wb') as f:
    f.write(r.content)
    print(filename+' downloaded')

print('Files saved')

print('Adding new data')

df_day = pd.read_csv(filename,thousands='.')

#Days since the beginning
new_days = df['Dias'].tail(1).values[0]+1

#Today's date
new_date = today.strftime("%m/%d/%Y")

#Data from Galicia
df_day_galicia = df_day[df_day['Area_Sanitaria']=='GALICIA']
new_total_cases = df_day_galicia['Casos_Totais'].values[0]
new_total_recovered = df_day_galicia['Pacientes_Con_Alta'].values[0]
new_total_deaths = df_day_galicia['Exitus'].values[0]
new_pcr = df_day_galicia['Novos_Casos_Abertos_Ultimas24h'].values[0]
new_cases = new_total_cases-df['Total casos'].tail(1).values[0]
new_deaths = new_total_deaths-df['Total fallecidos'].tail(1).values[0]
new_letality_rate = new_total_deaths*100/new_total_cases
new_total_in_hospital = df_day_galicia['Camas_Ocupadas_HOS'].values[0]
new_total_intensive_care =  df_day_galicia['Camas_Ocupadas_UCI'].values[0]
new_in_hospital = new_total_in_hospital-df['Hospitalizados'].tail(1).values[0]
new_intensive_care = new_total_intensive_care-df['UCI'].tail(1).values[0]
new_IA_14 = (new_total_cases-df['Total casos'].tail(14).values[0])*100000/df['Poblacion Galicia'].tail(1).values[0]
new_IA_7 = (new_total_cases-df['Total casos'].tail(7).values[0])*100000/df['Poblacion Galicia'].tail(1).values[0]

#Data from A Coruna
df_day_coruna = df_day[df_day['Area_Sanitaria']=='A.S. A CORUÑA E CEE']
new_total_cases_coruna = df_day_coruna['Casos_Totais'].values[0]
new_total_recovered_coruna = df_day_coruna['Pacientes_Con_Alta'].values[0]
new_total_deaths_coruna = df_day_coruna['Exitus'].values[0]
new_total_in_hospital_coruna = df_day_coruna['Camas_Ocupadas_HOS'].values[0]
new_total_intensive_care_coruna = df_day_coruna['Camas_Ocupadas_UCI'].values[0]
new_total_pcr_coruna = df_day_coruna['Probas_Realizadas_PCR'].values[0]
new_IA_14_coru = (new_total_cases_coruna-df['Total Casos A Coruna'].tail(14).values[0])*100000/df['Poblacion A Coruna'].tail(1).values[0]
new_IA_7_coru = (new_total_cases_coruna-df['Total Casos A Coruna'].tail(7).values[0])*100000/df['Poblacion A Coruna'].tail(1).values[0]

#Data from Ferrol
df_day_ferrol = df_day[df_day['Area_Sanitaria']=='A.S. FERROL']
new_total_cases_ferrol = df_day_ferrol['Casos_Totais'].values[0]
new_total_recovered_ferrol = df_day_ferrol['Pacientes_Con_Alta'].values[0]
new_total_deaths_ferrol = df_day_ferrol['Exitus'].values[0]
new_total_in_hospital_ferrol = df_day_ferrol['Camas_Ocupadas_HOS'].values[0]
new_total_intensive_care_ferrol = df_day_ferrol['Camas_Ocupadas_UCI'].values[0]
new_total_pcr_ferrol = df_day_ferrol['Probas_Realizadas_PCR'].values[0]
new_IA_14_ferrol = (new_total_cases_ferrol-df['Total Casos Ferrol'].tail(14).values[0])*100000/df['Poblacion Ferrol'].tail(1).values[0]
new_IA_7_ferrol = (new_total_cases_ferrol-df['Total Casos Ferrol'].tail(7).values[0])*100000/df['Poblacion Ferrol'].tail(1).values[0]


#Data from Lugo
df_day_lugo = df_day[df_day['Area_Sanitaria']=='A.S. LUGO, A MARIÑA E MONFORTE']
new_total_cases_lugo = df_day_lugo['Casos_Totais'].values[0]
new_total_recovered_lugo = df_day_lugo['Pacientes_Con_Alta'].values[0]
new_total_deaths_lugo = df_day_lugo['Exitus'].values[0]
new_total_in_hospital_lugo = df_day_lugo['Camas_Ocupadas_HOS'].values[0]
new_total_intensive_care_lugo = df_day_lugo['Camas_Ocupadas_UCI'].values[0]
new_total_pcr_lugo = df_day_lugo['Probas_Realizadas_PCR'].values[0]
new_IA_14_lugo = (new_total_cases_lugo-df['Total Casos Lugo'].tail(14).values[0])*100000/df['Poblacion Lugo'].tail(1).values[0]
new_IA_7_lugo = (new_total_cases_lugo-df['Total Casos Lugo'].tail(7).values[0])*100000/df['Poblacion Lugo'].tail(1).values[0]

#Data from Ourense
df_day_ourense = df_day[df_day['Area_Sanitaria']=='A.S. OURENSE, VERÍN E O BARCO']
new_total_cases_ourense = df_day_ourense['Casos_Totais'].values[0]
new_total_recovered_ourense = df_day_ourense['Pacientes_Con_Alta'].values[0]
new_total_deaths_ourense = df_day_ourense['Exitus'].values[0]
new_total_in_hospital_ourense = df_day_ourense['Camas_Ocupadas_HOS'].values[0]
new_total_intensive_care_ourense = df_day_ourense['Camas_Ocupadas_UCI'].values[0]
new_total_pcr_ourense = df_day_ourense['Probas_Realizadas_PCR'].values[0]
new_IA_14_ourense = (new_total_cases_ourense-df['Total Casos Ourense'].tail(14).values[0])*100000/df['Poblacion Ourense'].tail(1).values[0]
new_IA_7_ourense = (new_total_cases_ourense-df['Total Casos Ourense'].tail(7).values[0])*100000/df['Poblacion Ourense'].tail(1).values[0]

#Data from Pontevedra
df_day_ponte = df_day[df_day['Area_Sanitaria']=='A.S. PONTEVEDRA E O SALNÉS']
new_total_cases_ponte = df_day_ponte['Casos_Totais'].values[0]
new_total_recovered_ponte = df_day_ponte['Pacientes_Con_Alta'].values[0]
new_total_deaths_ponte = df_day_ponte['Exitus'].values[0]
new_total_in_hospital_ponte = df_day_ponte['Camas_Ocupadas_HOS'].values[0]
new_total_intensive_care_ponte = df_day_ponte['Camas_Ocupadas_UCI'].values[0]
new_total_pcr_ponte = df_day_ponte['Probas_Realizadas_PCR'].values[0]
new_IA_14_ponte = (new_total_cases_ponte-df['Total Casos Pontevedra'].tail(14).values[0])*100000/df['Poblacion Pontevedra'].tail(1).values[0]
new_IA_7_ponte = (new_total_cases_ponte-df['Total Casos Pontevedra'].tail(7).values[0])*100000/df['Poblacion Pontevedra'].tail(1).values[0]

#Data from Santiago
df_day_sant = df_day[df_day['Area_Sanitaria']=='A.S. SANTIAGO E BARBANZA']
new_total_cases_sant = df_day_sant['Casos_Totais'].values[0]
new_total_recovered_sant = df_day_sant['Pacientes_Con_Alta'].values[0]
new_total_deaths_sant = df_day_sant['Exitus'].values[0]
new_total_in_hospital_sant = df_day_sant['Camas_Ocupadas_HOS'].values[0]
new_total_intensive_care_sant = df_day_sant['Camas_Ocupadas_UCI'].values[0]
new_total_pcr_sant = df_day_sant['Probas_Realizadas_PCR'].values[0]
new_IA_14_sant = (new_total_cases_sant-df['Total Casos Santiago'].tail(14).values[0])*100000/df['Poblacion Santiago'].tail(1).values[0]
new_IA_7_sant = (new_total_cases_sant-df['Total Casos Santiago'].tail(7).values[0])*100000/df['Poblacion Santiago'].tail(1).values[0]

#Data from Vigo
df_day_vigo = df_day[df_day['Area_Sanitaria']=='A.S. VIGO']
new_total_cases_vigo = df_day_vigo['Casos_Totais'].values[0]
new_total_recovered_vigo = df_day_vigo['Pacientes_Con_Alta'].values[0]
new_total_deaths_vigo = df_day_vigo['Exitus'].values[0]
new_total_in_hospital_vigo = df_day_vigo['Camas_Ocupadas_HOS'].values[0]
new_total_intensive_care_vigo = df_day_vigo['Camas_Ocupadas_UCI'].values[0]
new_total_pcr_vigo = df_day_vigo['Probas_Realizadas_PCR'].values[0]
new_IA_14_vigo = (new_total_cases_vigo-df['Total Casos Vigo'].tail(14).values[0])*100000/df['Poblacion Vigo'].tail(1).values[0]
new_IA_7_vigo = (new_total_cases_vigo-df['Total Casos Vigo'].tail(7).values[0])*100000/df['Poblacion Vigo'].tail(1).values[0]

#Repeat population data
new_pop_galicia = df["Poblacion Galicia"].tail(1).values[0]
new_pop_coru = df["Poblacion A Coruna"].tail(1).values[0]
new_pop_ferrol = df["Poblacion Ferrol"].tail(1).values[0]
new_pop_lugo = df["Poblacion Lugo"].tail(1).values[0]
new_pop_ourense = df["Poblacion Ourense"].tail(1).values[0]
new_pop_ponte = df["Poblacion Pontevedra"].tail(1).values[0]
new_pop_sant = df["Poblacion Santiago"].tail(1).values[0]
new_pop_vigo = df["Poblacion Vigo"].tail(1).values[0]

df_new_row = pd.DataFrame([[new_days, today.strftime("%d/%m/%Y"), new_total_cases, new_total_recovered, new_total_deaths,
                           new_pcr, new_cases, new_deaths, new_letality_rate, new_total_in_hospital, new_total_intensive_care,
                           new_in_hospital, new_intensive_care, new_IA_14, new_IA_7, new_total_cases_coruna, new_total_recovered_coruna,
                           new_total_deaths_coruna, new_total_in_hospital_coruna, new_total_intensive_care_coruna,
                           new_total_pcr_coruna, new_IA_14_coru, new_IA_7_coru, new_total_cases_ferrol,
                            new_total_recovered_ferrol, new_total_deaths_ferrol,
                           new_total_in_hospital_ferrol, new_total_intensive_care_ferrol, new_total_pcr_ferrol,
                            new_IA_14_ferrol, new_IA_7_ferrol,
                           new_total_cases_lugo, new_total_recovered_lugo, new_total_deaths_lugo, new_total_in_hospital_lugo,
                           new_total_intensive_care_lugo, new_total_pcr_lugo, new_IA_14_lugo, new_IA_7_lugo,
                            new_total_cases_ourense, new_total_recovered_ourense,
                           new_total_deaths_ourense, new_total_in_hospital_ourense, new_total_intensive_care_ourense,
                           new_total_pcr_ourense, new_IA_14_ourense, new_IA_7_ourense,
                            new_total_cases_ponte, new_total_recovered_ponte, new_total_deaths_ponte,
                           new_total_in_hospital_ponte, new_total_intensive_care_ponte, new_total_pcr_ponte,
                            new_IA_14_ponte, new_IA_7_ponte, new_total_cases_sant,
                           new_total_recovered_sant, new_total_deaths_sant, new_total_in_hospital_sant, new_total_intensive_care_sant,
                           new_total_pcr_sant, new_IA_14_sant, new_IA_7_sant,
                            new_total_cases_vigo, new_total_recovered_vigo, new_total_deaths_vigo,
                           new_total_in_hospital_vigo, new_total_intensive_care_vigo, new_total_pcr_vigo,
                           new_IA_14_vigo, new_IA_7_vigo, new_pop_galicia, new_pop_coru, new_pop_ferrol, new_pop_lugo,
                           new_pop_ourense, new_pop_ponte, new_pop_sant, new_pop_vigo]],columns=df.keys(),
                         index=[new_days])


print('New data added')

df = df.append(df_new_row)

df.to_csv(data,index=False)

print('Dataset updated')

os.remove(filename)
