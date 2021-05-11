import pymongo, logging


class MongoDriver:
    client = None

    def __init__(self, db_dict: dict):
        try:
            self.DATABASE_HOST = db_dict.get('DATABASE_HOST')
            self.DATABASE_ADMIN_USERNAME = db_dict.get('DATABASE_ADMIN_USERNAME')
            self.DATABASE_ADMIN_PASSWORD = db_dict.get('DATABASE_ADMIN_PASSWORD')
            self.client = pymongo.MongoClient(self.DATABASE_HOST)
            self.client.admin.authenticate(self.DATABASE_ADMIN_USERNAME, self.DATABASE_ADMIN_PASSWORD)
            logging.info("[+] Database connected!")
        except Exception as e:
            logging.info("[-] Database connection error!")
            raise e
