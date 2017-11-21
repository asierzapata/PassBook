#!/usr/bin/env python
# coding=utf-8

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

import logging
import json
import passbook.db as db
import passbook.encrypt as encrypt

data = json.load(open('settings.json'))

# For the CBC mode, the init vector must be equal to AES.block_size, which is 16
initvector = data["initVector"]

loggerFormat = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

logging.basicConfig(format=loggerFormat,level=logging.INFO,filename='logPassBook.txt',filemode='w')

logger = logging.getLogger(__name__)

# define a new Handler to log to console as well
console = logging.StreamHandler()
# optional, set the logging level
console.setLevel(logging.INFO)
# set a format which is the same for console use
formatter = logging.Formatter(loggerFormat)
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)

connection = db.connect()

ADD, GET, UPD, STOP = range(4)


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='La lista de comandos actualmente soportados son:',
                    parse_mode=telegram.ParseMode.HTML)
    bot.sendMessage(update.message.chat_id, text='<b>/add_psw || /get_psw || /update_psw || /list</b>',
                    parse_mode=telegram.ParseMode.HTML)
    return True


def add_psw(bot, update):
    bot.sendMessage(update.message.chat_id, text='Para añadir una contraseña a una aplicación debes enviarla '
                                                 'con el siguiente formato:'
                                                 '<b>AppName,EncryptionKey,Password</b>',
                    parse_mode = telegram.ParseMode.HTML)

    bot.sendMessage(update.message.chat_id,
                    text='La única restricción es que la password y la encription key sean de 16'
                         ' carácteres de longitud',parse_mode=telegram.ParseMode.HTML)

    return ADD


def add_psw_response(bot, update):
    msg = (update.message.text).split(',')
    encripted_psw = encrypt.crypto(msg[2], msg[1], initvector, 1)
    if db.insertPsw(connection, update.message.from_user.id, msg[0], encripted_psw.encode('hex')) is True:
        bot.sendMessage(update.message.chat_id, text='La inserción se ha realizado con exito')
    else:
        bot.sendMessage(update.message.chat_id, text='Se ha producido un error')

    logger.info("User %s | %s inserted/modified a new password." % (update.message.from_user.first_name, str(update.message.from_user.id)))
    return ConversationHandler.END


def update_psw(bot, update):
    bot.sendMessage(update.message.chat_id, text='Indica que aplicación quieres modificar la contraseña')
    list(bot, update)
    bot.sendMessage(update.message.chat_id, text='El formato debe ser: <b>Application,NewEncryptionKey,NewPassword</b>'
                    , parse_mode=telegram.ParseMode.HTML)
    return UPD


def get_psw(bot, update):
    bot.sendMessage(update.message.chat_id, text='Indica que aplicación quieres recuperar la contraseña con su '
                                                 'respectiva encription key.')
    list(bot, update)
    bot.sendMessage(update.message.chat_id, text='El formato debe ser: <b>Application,Encryptionkey</b>'
                    ,parse_mode=telegram.ParseMode.HTML)
    return GET


def get_psw_response(bot, update):
    msg = (update.message.text).split(',')
    res = db.findPsw(connection, update.message.from_user.id, msg[0])
    try:
        bot.sendMessage(update.message.chat_id, text=encrypt.crypto(res.decode('hex'),msg[1],initvector,0))
    except UnicodeDecodeError:
        bot.sendMessage(update.message.chat_id, text = 'La encription key es erronea, intenta de nuevo')
        return GET
    logger.info("User %s | %s requested password for %s." % (update.message.from_user.first_name,str(update.message.from_user.id),str(msg[0])))
    return ConversationHandler.END

def list(bot,update):

    bot.sendMessage(update.message.chat_id, text="Tu lista de aplicaciones con una contraseña asignada es la siguiente:"
                        , parse_mode=telegram.ParseMode.HTML)
    for i in db.collectionApps(connection,update.message.from_user.id):
        bot.sendMessage(update.message.chat_id,
                        text="<b>"+i.encode('ascii')+"</b>"
                        ,parse_mode=telegram.ParseMode.HTML)
    logging.info("User %s | %s requested the list of apps." % (update.message.from_user.first_name,str(update.message.from_user.id)))
    return True


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s | %s canceled the conversation." % (user.first_name,str(update.message.from_user.id)))
    bot.sendMessage(update.message.chat_id,
                    text='Bye!')

    return ConversationHandler.END


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    updater = Updater(data["telegramToken"])
    dp = updater.dispatcher

    add_psw_handler = ConversationHandler(
        entry_points=[CommandHandler('add_psw', add_psw)],

        states={
            ADD: [MessageHandler(Filters.text, add_psw_response)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )
    update_psw_handler = ConversationHandler(
        entry_points=[CommandHandler('update_psw', update_psw)],

        states={
            UPD: [MessageHandler(Filters.text, add_psw_response)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    get_psw_handler = ConversationHandler(
        entry_points=[CommandHandler('get_psw', get_psw)],

        states={
            GET: [MessageHandler(Filters.text, get_psw_response)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    list_of_apps = CommandHandler('list', list)

    help_handler = CommandHandler('help', help)

    start_handler = CommandHandler('start',help)

    dp.add_handler(add_psw_handler)
    dp.add_handler(update_psw_handler)
    dp.add_handler(get_psw_handler)
    dp.add_handler(list_of_apps)
    dp.add_handler(help_handler)
    dp.add_handler(start_handler)

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()
