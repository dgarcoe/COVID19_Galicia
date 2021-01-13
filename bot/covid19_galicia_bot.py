import pandas as pd
import telebot
from telebot import types

data = '../data_galicia_covid.csv'

commands = { 
    'help'        : 'Devolve información dos comandos dispoñibles',
    'getKpis'     : 'Devolve o estado dos indicadores principais no último día (casos totais, casos activos, altas e falecidos)',
    'getIA'       : 'Devolve o estado actual da Incidencia Acumulada a 7 e 14 días en toda Galicia'
}

emojis = {
    'ok':'\U0001F7E2',
    'nok':'\U0001F534',
    'up':'\U00002B06',
    'down':'\U00002B07',
    'same':'\U00002194'
}

bot = telebot.TeleBot("", parse_mode=None)

def response_main_kpis():
    df = pd.read_csv(data)
    kpi_text = ""

    new_cases = df['Total casos'].tail(1).values[0]-df['Total casos'].tail(2).values[0]
    if (new_cases>0):
        kpi_text += emojis['nok']+' Casos totales: '+str(df['Total casos'].tail(1).values[0])+' '+emojis['up']+' Nuevos casos: '+str(new_cases)+'\n'
    elif (new_cases==0):
        kpi_text += emojis['ok']+' Casos totales: '+str(df['Total casos'].tail(1).values[0])+' '+emojis['same']+' Nuevos casos: '+str(new_cases)+'\n'

    kpi_text += '\n'        
    active_cases = df["Total casos"].tail(1).values[0]-df["Total altas"].tail(1).values[0]-df["Total fallecidos"].tail(1).values[0]
    new_active_cases = active_cases-(df["Total casos"].tail(2).values[0]-df["Total altas"].tail(2).values[0]-df["Total fallecidos"].tail(2).values[0])

    if (new_active_cases>0):
        kpi_text += emojis['nok']+' Casos activos: '+str(active_cases)+' '+emojis['up']+' Incremento activos: '+str(new_active_cases)+'\n'
    elif (new_active_cases<=0):
        kpi_text += emojis['ok']+' Casos activos: '+str(active_cases)+' '+emojis['down']+' Decremento activos: '+str(new_active_cases)+'\n'

    kpi_text += '\n'
    cured = df["Total altas"].tail(1).values[0]
    new_cured = df["Total altas"].tail(1).values[0]-df["Total altas"].tail(2).values[0]

    if (new_cured>0):
        kpi_text += emojis['ok']+' Altas: '+str(cured)+' '+emojis['up']+' Nuevas altas: '+str(new_cured)+'\n'
    elif(new_cured<=0):
        kpi_text += emojis['nok']+' Altas: '+str(cured)+' '+emojis['up']+' Nuevas altas: '+str(new_cured)+'\n'
    
    kpi_text += '\n'
    deceased = df["Total fallecidos"].tail(1).values[0]
    new_deceased = df["Total fallecidos"].tail(1).values[0]-df["Total fallecidos"].tail(2).values[0]

    if (new_deceased>0):
        kpi_text += emojis['nok']+' Fallecidos: '+str(deceased)+' '+emojis['up']+' Nuevos fallecidos: '+str(new_deceased)+'\n'
    elif(new_deceased==0):
        kpi_text += emojis['ok']+' Fallecidos: '+str(deceased)+' '+emojis['same']+' Nuevos fallecidos: '+str(new_deceased)+'\n'

    return kpi_text

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

print('COVID-19 Telegram Bot started and waiting for messages!')
bot.polling()
