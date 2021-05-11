from telegram import (Bot, Update, InlineKeyboardMarkup, InlineKeyboardButton)
from telegram.ext import (CallbackContext, ConversationHandler)
import os, logging # for enhanced logging do not use print!!

# custom modules import
from modules import dbmodel   # gDriveModule, mongoDumpModule
# from modules.mongoDriver import DB_connection, DB_rdkit_connection
# import restrictions decorator
from modules.administration import restricted
from token_extractor import token

# logging.info(f'{token}')
bot = Bot(token)

# define states of bot
PURGING = range(1)
# Callback data states
YUP, NOPE, RDKIT_PURGE = range(3)

# restricted handlers for admins!
@restricted # decorator, that does restrictions!
def purge_handler(update, context):
    button_list = [
        [
            InlineKeyboardButton("✅ Yup", callback_data=str(YUP)),
            InlineKeyboardButton("🙅🏻‍♀️ Nope", callback_data=str(NOPE)),
            InlineKeyboardButton("RDKIT_PURGE", callback_data=str(RDKIT_PURGE))
        ]
        
        ]
    reply_markup = InlineKeyboardMarkup(button_list)
    update.message.reply_text(
        "👩🏻‍🦰 Do you really want to purge the database?\nБудь мужчиной, Марио!",
        reply_markup=reply_markup
    )
    return PURGING


# helper function that actually does purging 
def purge(update, context):
    query = update.callback_query
    query.answer()
    dbmodel.purge(DB_connection)
    reply_markup = InlineKeyboardMarkup([])
    query.edit_message_text(
            text='Да поможет тебе святой Франциск, {}! Database was purged.'.format(query.message.chat.first_name),
            reply_markup=reply_markup
        )
    context.chat_data.clear()
    context.user_data.clear()

    return ConversationHandler.END # only accessible if `user_id` is in `LIST_OF_ADMINS`.


def rdkit_purge(update, context):
    query = update.callback_query
    query.answer()
    dbmodel.purge(DB_rdkit_connection)
    reply_markup = InlineKeyboardMarkup([])
    query.edit_message_text(
            text='Да поможет тебе святой Франциск, {}! RDkit database was purged.'.format(query.message.chat.first_name),
            reply_markup=reply_markup
        )
    context.chat_data.clear()
    context.user_data.clear()

    return ConversationHandler.END # only accessible if `user_id` is in `LIST_OF_ADMINS`.

# Define a few regular command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.

def start(update, context):
    """
    welcome message and initialization of user by inserting his data into DB
    """
    # retrieving data from user message
    user_info = update.message.from_user
    chat_id = update.message.chat.id

    # приветственное сообщение юзеру
    update.message.reply_text(
    """Привет, {}! 👩🏻‍💻
    /start - приветствие 
    /purge - очистка бд
    /help - эхо-тест
    /dump - тестирование дампа базы данных (присылает в лс зип-дамп)
    /update - заполняет базу вендоров фрагментами
    /sim_search - реализует поиск по подобию по SMILES
    /struc_search - реализует поиск по структуре
    /test""".format(user_info.first_name))

    # запись данных юзера в БД 
    userdata_dict = {
        "_id": user_info.id,
        "user_id": user_info.id,
        "username": "@{}".format(user_info.username),
        "firstname": user_info.first_name,
        "lastname": user_info.last_name
    }
    # dbmodel.add_user_record(DB_connection, **userdata_dict)

# {
#     "_id": user_info.id,
#     "user_id": user_info.id,
#     "firstname": user_info.first_name,
#     "lastname": user_info.last_name,
#     "lab_id" : 123124123123123123, 
#     "lab_name" : "лаборатория номер 8 элементоорганических соединений dilman_lab",
#     "organization" : "ZIOC RAS, institute of organic chemistry"
#     "contacts" : {"email" : "test@mail.com", "phone" : "817263221"},
#     "wishlist" : [
#            {
#                 "vendor_name" : "sigma-aldrich",
#                 "vendor_contact" : "sigma@sales.com",
#                 "chemical_name" : "2-butanone",
#                 "CAS" : "123-24245-123",
#                 "catalog_number" : "SIAL123090",
#                 "SKU" : "1 g"
#             }, 
#             {
#                 "vendor_name" : "alfa-aesar",
#                 "vendor_contact" : "alfa@sales.com",
#                 "chemical_name" : "benzofenone",
#                 "CAS" : "123-25-123",
#                 "catalog_number" : "ALFA123090",
#                 "SKU" : "100 ml"
#             },
#             {...},
#             {...},
#             ...
#     ]
# }

    # associated with user chat and context stored data should be cleaned up to prevent mess
    context.chat_data.clear()
    user_data = context.user_data
    user_data.clear()

    # test logging module
    logging.info('user initialized by /start command.')
    return -1 # equivalent of ConversationHandler.END : to be able to end conversation with this /start function


def help_command(update: Update, context: CallbackContext) -> None:
    """
    Send a message when the command /help is issued.
    """
    update.message.reply_text('Потомок князей Бриндизи никогда не запятнает своих рук работой.')


@restricted # decorator, that does restrictions!
def dump(update, context):
    """
    dumps whole db, archives it, uploads .zip archive with data to Gdrive and sends user metadata
    """
    chat_id = update.message.chat.id
    path = mongoDumpModule.dump_database()[1] + ".zip"
    logging.info(f'{path}')
    files = os.listdir("./mongodumps")
    logging.info(f'{files}')
    # this bot cannot send more than 50 mb!!!
    # bot.sendDocument(chat_id=chat_id, document=open(f'{path}.zip', 'rb'), timeout=1000)
    
    # instantiate Connection Class
    GDriver = gDriveModule.GoogleDriver()
    # call connect method
    connect_result = GDriver.connect()
    assert connect_result != "True", "GDrive connection method failed!" #autotest
    # check
    if connect_result == True:
        update.message.reply_text('Марио, какое счастье, Лючия принесла тройню!\nGDrive auth successful')
    # take filename from full abspath
    name = os.path.basename(path)
    # call upload method on Driver object
    upload_result = GDriver.upload(name, path)
    if upload_result == True:
        update.message.reply_text(
            f"""Database dump uploaded to:
labaggregator.tests@gmail.com/GDrive
under tag {name}""")
    # now clear all cached data
    # clear assosiated with user data and custom context variables
    context.chat_data.clear()
    context.user_data.clear()

def exit(update, context):
    """
    handler for terminating all dialog sequences
    """
    try:
        query = update.callback_query
        if query != None:
            reply_markup = InlineKeyboardMarkup([])
            query.edit_message_text(
                text="You cancelled db removal. Да поможет тебе святой Януарий!",
                reply_markup=reply_markup
            )
        else:
            update.message.reply_text(f"""Выход из диалога. Да поможет тебе святой Антоний.""")
    except:
        update.message.reply_text(f"""Выход из диалога. Да поможет тебе святой Антоний.""") 
        pass
    # now clear all cached data
    # clear assosiated with user data and custom context variables
    context.chat_data.clear()
    context.user_data.clear()
    # equivalent of return ConversationHandler.END
    return ConversationHandler.END

@restricted
def update_vendors_db(update, context):
    """
    экспериментальный хендлер, который долго и упорно наполняет молекулами и фрагментами химическю базу данных
    """
    result = dbmodel.update_with_cgrdb()
    update.message.reply_text(result)


def sim_search(update, context):
    """
    Хендлер, который проводит поиск по подобию
    """
    update.message.reply_text('Введите SMILES')
    SMILES = update.message.text
    update.message.reply_text(f'{SMILES} is your smiles')


    #result = dbmodel.similarity_search(SMILES_input, n=10)


def struc_search(update, context):
    """
    Хендлер, который проводит структурный поиск
    """

    result = dbmodel.structure_search(SMILES_input)


# def gDriveTest(update: Update, context: CallbackContext) -> None:
#     """
#     bla-bla-bla
#     """
#     name = "yoga.jpg"
#     filepath = './tmp/yoga.jpg'
#     GDriver = gDriveModule.GoogleDriver()
#     result = GDriver.connect(name, filepath)
#     update.message.reply_text(f'{result}')