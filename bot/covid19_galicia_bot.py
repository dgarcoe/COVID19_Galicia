import pandas as pd
import telebot
from telebot import types
from dotenv import load_dotenv
import os
import logging

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

load_dotenv()

data = os.getenv('DATA_FILE')
token = os.getenv('TOKEN')

emojis = {
    'ok':'\U0001F7E2',
    'nok':'\U0001F534',
    'up':'\U00002B06',
    'down':'\U00002B07',
    'same':'\U00002194',
    'danger':'\U0001F7E0',
    'warning':'\U0001F7E1',
    'calendar':'\U0001F4C5',
    'cured': '\U0001F49A',
    'ill': '\U0001F912',
    'death': '\U00002620',
    'hospital': '\U0001F6CC',
    'uci': '\U0001F6A8'
}

commands = { 
    'help'        : 'Devolve información dos comandos dispoñibles',
    'getKpis'     : 'Devolve o estado dos indicadores principais no último día (casos totais, casos activos, altas e falecidos)',
    'getIA'       : 'Devolve o estado actual da Incidencia Acumulada a 7 e 14 días en toda Galicia',
    'getHosp'     : 'Devolve o estado da ocupación hospitalaria no conxunto de Galicia',
    'getDate'     : 'Devolve a data na que se fixo a última actualización de datos',
    'getAreas'    : 'Devolve os datos de cada área sanitaria no último dia ('+emojis["cured"]+' incremento curados, '+emojis["ill"]+' incremento casos, '+emojis["death"]+' incremento falecidos, '+emojis["hospital"]+' total hospitalizados, '+emojis["uci"]+' total UCIs)'
}

bot = telebot.TeleBot(token, parse_mode=None)

def response_main_kpis():

    df = pd.read_csv(data)
    kpi_text = ""

    new_cases = df['Total casos'].tail(1).values[0]-df['Total casos'].tail(2).values[0]
    if (new_cases>0):
        kpi_text += emojis['nok']+' Casos totais: '+str(df['Total casos'].tail(1).values[0])+' '+emojis['up']+' Novos casos: '+str(new_cases)+'\n'
    elif (new_cases==0):
        kpi_text += emojis['ok']+' Casos totais: '+str(df['Total casos'].tail(1).values[0])+' '+emojis['same']+' Novos casos: '+str(new_cases)+'\n'

    kpi_text += '\n'        
    active_cases = df["Total casos"].tail(1).values[0]-df["Total altas"].tail(1).values[0]-df["Total fallecidos"].tail(1).values[0]
    new_active_cases = active_cases-(df["Total casos"].tail(2).values[0]-df["Total altas"].tail(2).values[0]-df["Total fallecidos"].tail(2).values[0])

    if (new_active_cases>0):
        kpi_text += emojis['nok']+' Casos activos: '+str(active_cases)+' '+emojis['up']+' Incremento activos: '+str(new_active_cases)+'\n'
    elif (new_active_cases<=0):
        kpi_text += emojis['ok']+' Casos activos: '+str(active_cases)+' '+emojis['down']+' Descenso activos: '+str(new_active_cases)+'\n'

    kpi_text += '\n'
    cured = df["Total altas"].tail(1).values[0]
    new_cured = df["Total altas"].tail(1).values[0]-df["Total altas"].tail(2).values[0]

    if (new_cured>0):
        kpi_text += emojis['ok']+' Altas: '+str(cured)+' '+emojis['up']+' Novas altas: '+str(new_cured)+'\n'
    elif(new_cured<=0):
        kpi_text += emojis['nok']+' Altas: '+str(cured)+' '+emojis['up']+' Novas altas: '+str(new_cured)+'\n'
    
    kpi_text += '\n'
    deceased = df["Total fallecidos"].tail(1).values[0]
    new_deceased = df["Total fallecidos"].tail(1).values[0]-df["Total fallecidos"].tail(2).values[0]

    if (new_deceased>0):
        kpi_text += emojis['nok']+' Falecidos: '+str(deceased)+' '+emojis['up']+' Novos falecidos: '+str(new_deceased)+'\n'
    elif(new_deceased==0):
        kpi_text += emojis['ok']+' Falecidos: '+str(deceased)+' '+emojis['same']+' Novos falecidos: '+str(new_deceased)+'\n'

    return kpi_text

def response_IA():

    df = pd.read_csv(data)
    ia_text = ""

    ia_14 = round(df['IA 14'].tail(1).values[0],2)
    ia_7 = round(df['IA 7'].tail(1).values[0],2)

    if (ia_14>250):
        ia_text += emojis['nok']+' IA 14: '+str(ia_14)
    elif (ia_14>50):
        ia_text += emojis['danger']+' IA 14: '+str(ia_14)
    elif (ia_14>25):
        ia_text += emojis['warning']+' IA 14: '+str(ia_14)
    elif (ia_14>0):
        ia_text += emojis['ok']+' IA 14: '+str(ia_14)

    ia_text += '\n\n'

    if (ia_7>125):
        ia_text += emojis['nok']+' IA 7: '+str(ia_7)
    elif (ia_7>25):
        ia_text += emojis['danger']+' IA 7: '+str(ia_7)
    elif (ia_7>10):
        ia_text += emojis['warning']+' IA 7: '+str(ia_7)
    elif (ia_7>0):
        ia_text += emojis['ok']+' IA 7: '+str(ia_7)


    return ia_text

def response_date():

    df = pd.read_csv(data)

    return emojis['calendar']+' '+df["Fecha"].tail(1).values[0]

def response_hospital():

    df = pd.read_csv(data)
    hosp_text =""

    hosp = df['Hospitalizados'].tail(1).values[0]
    dif_hosp = df['Hospitalizados'].tail(1).values[0]-df['Hospitalizados'].tail(2).values[0]
    uci = df['UCI'].tail(1).values[0]
    dif_uci = df['UCI'].tail(1).values[0]-df['UCI'].tail(2).values[0]

    if (dif_hosp>0):
        hosp_text += emojis['nok']+" Hospitalizados: "+str(hosp)+' '+emojis['up']+' Incremento hospitalizados: '+str(dif_hosp)
    elif(dif_hosp<=0):
        hosp_text += emojis['ok']+" Hospitalizados: "+str(hosp)+' '+emojis['down']+' Descenso hospitalizados: '+str(dif_hosp)

    hosp_text += '\n\n'

    if (dif_uci>0):
        hosp_text += emojis['nok']+" UCI: "+str(hosp)+' '+emojis['up']+' Incremento UCIs: '+str(dif_uci)
    elif(dif_uci<=0):
        hosp_text += emojis['ok']+" UCI: "+str(hosp)+' '+emojis['down']+' Descenso UCIs: '+str(dif_uci)

    return hosp_text

def response_areas():
    
    df = pd.read_csv(data)
    area_text =""

    inc_cured_coru = str(df["Total Altas A Coruna"].tail(1).values[0]-df["Total Altas A Coruna"].tail(2).values[0])
    inc_dead_coru = str(df["Total Fallecidos A Coruna"].tail(1).values[0]-df["Total Fallecidos A Coruna"].tail(2).values[0])
    inc_cases_coru = str(df["Total Casos A Coruna"].tail(1).values[0]-df["Total Casos A Coruna"].tail(2).values[0])
    hosp_coru = str(df["Total Hospitalizados A Coruna"].tail(1).values[0])
    uci_coru = str(df["Total UCI A Coruna"].tail(1).values[0])

    area_text += "A Coruña - "+emojis["ill"]+inc_cases_coru+" "+emojis["cured"]+inc_cured_coru+" "+emojis["death"]+inc_dead_coru+" "+emojis["hospital"]+hosp_coru+" "+emojis["uci"]+uci_coru
    area_text += "\n\n"

    inc_cured_fer = str(df["Total Altas Ferrol"].tail(1).values[0]-df["Total Altas Ferrol"].tail(2).values[0])
    inc_dead_fer = str(df["Total Fallecidos Ferrol"].tail(1).values[0]-df["Total Fallecidos Ferrol"].tail(2).values[0])
    inc_cases_fer = str(df["Total Casos Ferrol"].tail(1).values[0]-df["Total Casos Ferrol"].tail(2).values[0])
    hosp_fer = str(df["Total Hospitalizados Ferrol"].tail(1).values[0])
    uci_fer = str(df["Total UCI Ferrol"].tail(1).values[0])

    area_text += "Ferrol - "+emojis["ill"]+inc_cases_fer+" "+emojis["cured"]+inc_cured_fer+" "+emojis["death"]+inc_dead_fer+" "+emojis["hospital"]+hosp_fer+" "+emojis["uci"]+uci_fer
    area_text += "\n\n"

    inc_cured_lugo = str(df["Total Altas Lugo"].tail(1).values[0]-df["Total Altas Lugo"].tail(2).values[0])
    inc_dead_lugo = str(df["Total Fallecidos Lugo"].tail(1).values[0]-df["Total Fallecidos Lugo"].tail(2).values[0])
    inc_cases_lugo = str(df["Total Casos Lugo"].tail(1).values[0]-df["Total Casos Lugo"].tail(2).values[0])
    hosp_lugo = str(df["Total Hospitalizados Lugo"].tail(1).values[0])
    uci_lugo = str(df["Total UCI Lugo"].tail(1).values[0])

    area_text += "Lugo - "+emojis["ill"]+inc_cases_lugo+" "+emojis["cured"]+inc_cured_lugo+" "+emojis["death"]+inc_dead_lugo+" "+emojis["hospital"]+hosp_lugo+" "+emojis["uci"]+uci_lugo
    area_text += "\n\n"

    inc_cured_pont = str(df["Total Altas Pontevedra"].tail(1).values[0]-df["Total Altas Pontevedra"].tail(2).values[0])
    inc_dead_pont = str(df["Total Fallecidos Pontevedra"].tail(1).values[0]-df["Total Fallecidos Pontevedra"].tail(2).values[0])
    inc_cases_pont = str(df["Total Casos Pontevedra"].tail(1).values[0]-df["Total Casos Pontevedra"].tail(2).values[0])
    hosp_pont = str(df["Total Hospitalizados Pontevedra"].tail(1).values[0])
    uci_pont = str(df["Total UCI Pontevedra"].tail(1).values[0])

    area_text += "Pontevedra - "+emojis["ill"]+inc_cases_pont+" "+emojis["cured"]+inc_cured_pont+" "+emojis["death"]+inc_dead_pont+" "+emojis["hospital"]+hosp_pont+" "+emojis["uci"]+uci_pont
    area_text += "\n\n"

    inc_cured_ou = str(df["Total Altas Ourense"].tail(1).values[0]-df["Total Altas Ourense"].tail(2).values[0])
    inc_dead_ou = str(df["Total Fallecidos Ourense"].tail(1).values[0]-df["Total Fallecidos Ourense"].tail(2).values[0])
    inc_cases_ou = str(df["Total Casos Ourense"].tail(1).values[0]-df["Total Casos Ourense"].tail(2).values[0])
    hosp_ou = str(df["Total Hospitalizados Ourense"].tail(1).values[0])
    uci_ou = str(df["Total UCI Ourense"].tail(1).values[0])

    area_text += "Ourense - "+emojis["ill"]+inc_cases_ou+" "+emojis["cured"]+inc_cured_ou+" "+emojis["death"]+inc_dead_ou+" "+emojis["hospital"]+hosp_ou+" "+emojis["uci"]+uci_ou
    area_text += "\n\n"

    inc_cured_sant = str(df["Total Altas Santiago"].tail(1).values[0]-df["Total Altas Santiago"].tail(2).values[0])
    inc_dead_sant = str(df["Total Fallecidos Santiago"].tail(1).values[0]-df["Total Fallecidos Santiago"].tail(2).values[0])
    inc_cases_sant = str(df["Total Casos Santiago"].tail(1).values[0]-df["Total Casos Santiago"].tail(2).values[0])
    hosp_sant = str(df["Total Hospitalizados Santiago"].tail(1).values[0])
    uci_sant = str(df["Total UCI Santiago"].tail(1).values[0])

    area_text += "Santiago - "+emojis["ill"]+inc_cases_sant+" "+emojis["cured"]+inc_cured_sant+" "+emojis["death"]+inc_dead_sant+" "+emojis["hospital"]+hosp_sant+" "+emojis["uci"]+uci_sant
    area_text += "\n\n"

    inc_cured_vigo = str(df["Total Altas Vigo"].tail(1).values[0]-df["Total Altas Vigo"].tail(2).values[0])
    inc_dead_vigo = str(df["Total Fallecidos Vigo"].tail(1).values[0]-df["Total Fallecidos Vigo"].tail(2).values[0])
    inc_cases_vigo = str(df["Total Casos Vigo"].tail(1).values[0]-df["Total Casos Vigo"].tail(2).values[0])
    hosp_vigo = str(df["Total Hospitalizados Vigo"].tail(1).values[0])
    uci_vigo = str(df["Total UCI Vigo"].tail(1).values[0])

    area_text += "Vigo - "+emojis["ill"]+inc_cases_vigo+" "+emojis["cured"]+inc_cured_vigo+" "+emojis["death"]+inc_dead_vigo+" "+emojis["hospital"]+hosp_vigo+" "+emojis["uci"]+uci_vigo

    return area_text


# help page
@bot.message_handler(commands=['help'])
def command_help(m):
    logger.info("/help command from "+str(m.from_user.id)+" "+m.from_user.first_name)
    cid = m.chat.id
    help_text = "Os seguintes comandos están dispoñibles: \n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)  # send the generated help page

# kpis page
@bot.message_handler(commands=['getKpis'])
def command_kpis(m):
    logger.info("/getKpis command from "+str(m.from_user.id)+" "+m.from_user.first_name)
    cid = m.chat.id
    bot.send_message(cid, response_main_kpis()) 

# IA page
@bot.message_handler(commands=['getIA'])
def command_ia(m):
    logger.info("/getIA command from "+str(m.from_user.id)+" "+m.from_user.first_name)
    cid = m.chat.id
    bot.send_message(cid, response_IA()) 

# Date page
@bot.message_handler(commands=['getDate'])
def command_date(m):
    logger.info("/getDate command from "+str(m.from_user.id)+" "+m.from_user.first_name)
    cid = m.chat.id
    bot.send_message(cid, response_date()) 

# Hospital page
@bot.message_handler(commands=['getHosp'])
def command_hosp(m):
    logger.info("/getHosp command from "+str(m.from_user.id)+" "+m.from_user.first_name)
    cid = m.chat.id
    bot.send_message(cid, response_hospital()) 

# Areas page
@bot.message_handler(commands=['getAreas'])
def command_areas(m):
    logger.info("/getAreas command from "+str(m.from_user.id)+" "+m.from_user.first_name)
    cid = m.chat.id
    bot.send_message(cid, response_areas())


print('COVID-19 Galicia Telegram Bot started and waiting for messages!')
bot.polling()
