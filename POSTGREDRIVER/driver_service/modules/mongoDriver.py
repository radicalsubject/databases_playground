import pymongo, logging
from modules.dbconfig import vendorbot_credentials, vendorbot_collections, rdkit_credentials, rdkit_collections


class MongoDriver:
  def __init__(self, *args, **kwargs):
    
    if args: # If args is not empty.
      self.args = args
    if kwargs:
      for key, value in kwargs.items():
        setattr(self, key, value)

  def connect(self):
    try:
      #engine and connection
      self.connection = pymongo.MongoClient(self.DATABASE_HOST)
      self.connection.admin.authenticate(self.DATABASE_ADMIN_USERNAME, self.DATABASE_ADMIN_PASSWORD)
      self.db = self.connection[self.DATABASE_NAME] #creating DB
      logging.info('[+] Database connected!')
    except Exception as e:
      logging.info("[+] Database connection error!")
      raise e

  def create_collections(self):
    dic = {}
    #dynamically assign variables on the fly: from the list of collection names create collections
    for arg in self.args:
        dic[f"{arg}"] = arg
    for k,v in dic.items():
        exec("self.%s=self.db['%s']" % (k,v))

DB_connection = MongoDriver(*vendorbot_collections, **vendorbot_credentials)
DB_connection.connect()
DB_connection.create_collections()

# i can use one more instance of driver object:

DB_rdkit_connection = MongoDriver(*rdkit_collections, **rdkit_credentials)
DB_rdkit_connection.connect()
DB_rdkit_connection.create_collections()
