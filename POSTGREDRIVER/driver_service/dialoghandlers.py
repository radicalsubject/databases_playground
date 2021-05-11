from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler, CallbackQueryHandler)
import handlers
from handlers import YUP, NOPE, RDKIT_PURGE, PURGING
import CGRtools
import dbmodel

purge_dialog = ConversationHandler(
    entry_points=[CommandHandler('purge', handlers.purge_handler)],
    states={
        PURGING:[CallbackQueryHandler(handlers.purge, pattern='^{}$'.format(str(YUP))),
                CallbackQueryHandler(handlers.exit, pattern='^{}$'.format(str(NOPE))),
                CallbackQueryHandler(handlers.rdkit_purge, pattern='^{}$'.format(str(RDKIT_PURGE)))
        ]
    },
    fallbacks=[MessageHandler(Filters.regex('^Done$'), handlers.exit)]
)








mol = None

def sim_search(update, context):
    update.message.reply_text('Введите СМАЙЛЗ(ДЭВИС)')
    return 1


def first_response(update, context): 
    
    inp = CGRtools.smiles(update.message.text)
    # add SMILES validation
    if not isinstance(inp, CGRtools.containers.molecule.MoleculeContainer):
        # raise ValueError(f'{SMILES_input} - invalid SMILES!')
        update.message.reply_text('Это какой-то мусор, а не СМАЙЛЗ, попробуй ещё раз')
        return 1
    
    update.message.reply_text('Это хороший СМАЙЛЗ, а сколько молекул хочешь?')
    mol = inp
    return 2


def second_response(update, context):
    try:
        n_mol = int(update.message.text)
    except:
        update.message.reply_text('Что-то это не очень похоже на число, попробуй еще раз')
        return 2
    else:
        update.message.reply_text('Вот твои молекулы')
        dbmodel.

        return ConversationHandler.END

def 
    
def stop(update, context):
    update.message.reply_text('Вот и поговорили')
    return ConversationHandler.END


similarity_search = ConversationHandler(
    entry_points=[CommandHandler('sim_search', sim_search)],
    states={
        1: [MessageHandler(Filters.text, first_response, pass_user_data=True)],

        2: [MessageHandler(Filters.text, second_response, pass_user_data=True)]
    },
    fallbacks=[CommandHandler('stop', stop)]
)