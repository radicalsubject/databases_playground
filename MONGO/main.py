import logging
from modules.db.mongodb import MongoDriver

# Enable logging
logging.basicConfig(
    # filename='my_runtime_log.log', # saving log to filename
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO  # DEBUG
)
logging.info('logger started')
logger = logging.getLogger(__name__)

db_dict = {
    'DATABASE_NAME':'vendorbotdb',
    'DATABASE_HOST':'mongodb://127.0.0.1:27018/bot_container',
    'DATABASE_ADMIN_USERNAME':'labaggregator',
    'DATABASE_ADMIN_PASSWORD':'password'
}

def main():
    db = MongoDriver(db_dict)
    client = db.client

if __name__ == '__main__':
    main()
