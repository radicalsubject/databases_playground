import os
MONGO_URL = os.environ["MONGO_URL"]
MONGO_INITDB_ROOT_USERNAME = os.environ["MONGO_INITDB_ROOT_USERNAME"]
MONGO_INITDB_ROOT_PASSWORD = os.environ["MONGO_INITDB_ROOT_PASSWORD"]
DATABASE_NAME = os.environ["MONGO_INITDB_DATABASE"]

vendorbot_credentials = dict(
    DATABASE_NAME = DATABASE_NAME, 
    DATABASE_HOST = MONGO_URL, #"mongodb://mongodb_api:27027/bot" 
    DATABASE_ADMIN_USERNAME = MONGO_INITDB_ROOT_USERNAME, # oikura
    DATABASE_ADMIN_PASSWORD = MONGO_INITDB_ROOT_PASSWORD  # dr5[gnhn
)

vendorbot_collections = ("users_collection", "vendors_collection", "crude_vendors_data")

rdkit_credentials = dict(
    DATABASE_NAME = "rdkit_db", 
    DATABASE_HOST = MONGO_URL, #"mongodb://mongodb_api:27027/bot" 
    DATABASE_ADMIN_USERNAME = MONGO_INITDB_ROOT_USERNAME, # oikura
    DATABASE_ADMIN_PASSWORD = MONGO_INITDB_ROOT_PASSWORD  # dr5[gnhn
)

rdkit_collections = ("molecules", "mfp_counts", "permutations")

