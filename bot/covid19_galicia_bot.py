import pandas as pd
import telebot
from telebot import types

data = '../data_galicia_covid.csv'

commands = { 
    'help'        : 'Devolve información dos comandos dispoñibles',
    'getKpis'     : 'Devolve o estado dos indicadores principais no último día (casos totais, casos activos, altas e falecidos)',
    'getIA'       : 'Devolve o estado actual da Incidencia Acumulada a 7 e 14 días en toda Galicia',
    'getHosp' : 'Devolve o estado da ocupación hospitalaria no conxunto de Galicia',
    'getDate'     : 'Devolve a data na que se fixo a última actualización de datos'
}

emojis = {
    'ok':'\U0001F7E2',
    'nok':'\U0001F534',
    'up':'\U00002B06',
    'down':'\U00002B07',
    'same':'\U00002194',
    'danger':'\U0001F7E0',
    'warning':'\U0001F7E1',
    'calendar':'\U0001F4C5'
}

bot = telebot.TeleBot("", parse_mode=None)

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


# help page
@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "Os seguintes comandos están dispoñibles: \n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)  # send the generated help page

# kpis page
@bot.message_handler(commands=['getKpis'])
def command_help(m):
    cid = m.chat.id
    bot.send_message(cid, response_main_kpis()) 

# IA page
@bot.message_handler(commands=['getIA'])
def command_help(m):
    cid = m.chat.id
    bot.send_message(cid, response_IA()) 

# Date page
@bot.message_handler(commands=['getDate'])
def command_help(m):
    cid = m.chat.id
    bot.send_message(cid, response_date()) 

# Hospital page
@bot.message_handler(commands=['getHosp'])
def command_help(m):
    cid = m.chat.id
    bot.send_message(cid, response_hospital()) 


print('COVID-19 Galicia Telegram Bot started and waiting for messages!')
bot.polling()
