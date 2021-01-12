import telebot
from telebot import types

commands = { 
    'help'        : 'Devolve información dos comandos dispoñibles',
    'getKpis'     : 'Devolve unha imaxe co estado dos indicadores principais no último día',
    'getIA'       : 'Devolve unha imaxe co estado actual da Incidencia Acumulada a 7 e 14 días en toda Galicia'
}

bot = telebot.TeleBot("***TOKEN***", parse_mode=None)

# help page
@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "Os seguintes comandos están dispoñibles: \n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)  # send the generated help page

bot.polling()
