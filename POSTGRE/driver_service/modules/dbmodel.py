import json, time, os, logging
from modules.dbschema import dbclassobject
# import pymongo
import sys
sys.modules['__main__'].__file__ = None  # add-hoc for disable Pony interactive mode.

import pony.orm as pny
from pony.orm import db_session, select, Database

from CGRtools import RDFRead, ReactionContainer, SDFRead, SMILESRead, SDFWrite

import CGRdb
from CGRdb import load_schema, Reaction, Molecule
from CGRdbData import MoleculeClass, MoleculeProperties



def purge(DB_connection):
    """
    great power comes with great responsibility: func drops collections and even whole DB
    # DB_connection.users_collection.drop()
    """
    logging.info(f"list of all database names: {DB_connection.connection.list_database_names()}")
    DB_connection.connection.drop_database(DB_connection.DATABASE_NAME)
    logging.info(f"list of all database names: {DB_connection.connection.list_database_names()}")

def add_user_record(DB_connection, **kwargs):
	'''
	inserted data looks smth like this
	kwargs = {"username":'@oikura', "names":'Asya Vlasova', "userID":'12982928'}
	'''
	try:
		DB_connection.users_collection.insert_one(kwargs)
		return logging.info("User data inserted successfully")
	except pymongo.errors.DuplicateKeyError as e:
		logging.warning(e)

# #######################
# def update_user_record(SMILES, synonym, user_id):
#     data = {"SMILES" : SMILES,
#             "synonym" : synonym
#             }
#     myquery = {"_id": user_id}
#     newvalues = {'$push': {'verified_by_user_queries': data}}
#     users_collection.update_one(myquery, newvalues)

# @run_async
# def update_user_wishlist(SMILES, catNo, user_id):
#     price = scrape(catNo)
#     data = {"SMILES" : SMILES,
#             "price" : price
#             }
#     myquery = {"_id": user_id}
#     newvalues = {'$push': {'wishlist': data}}
#     users_collection.update_one(myquery, newvalues)

def update_with_cgrdb():
    # connect to cgrdb database
    db = load_schema('schema_name', password='secret', port=5432, host='postgredb_service', user='postgres')
    parts=os.listdir("/jupyter_scripts/sdf_sial") # list of sdf files with molecules
    for part in parts:
        mols = SDFRead(f'/jupyter_scripts/sdf_sial/{part}').read() # read every file 
        for molecule in mols:   # try to put molecule in our db
            try:    
                with db_session:
                    m = Molecule(molecule)
            except: # if molecule already in db, do nothing
                pass


def similarity_search(SMILES_input, n=10):
    '''
    input:
    SMILES_input - SMILES of molecule for search
    n - number of results (first n will be returned)
    return:
    list of CGRtools molecule-containers
    '''

    inp = CGRtools.smiles(SMILES_input)
    # add SMILES validation
    if not isinstance(inp, CGRtools.containers.molecule.MoleculeContainer):
        raise ValueError(f'{SMILES_input} - invalid SMILES!')

    with db_session:
        found = Molecule(inp)
        molecules = found.molecules(1, n)  # take first n molecules, sorted automatically by tanimoto
        structures = [mol.structure for mol in molecules]
    return structures


# def convert_to_smiles(resultssimilarity):
#     # print("imhere")
#     compound_dict = []
#     # range(len(resultssimilarity))
#     # print(resultssimilarity)
#     for i in range(len(resultssimilarity)):
#         if resultssimilarity[i][0] > 0.45:
#             myquery = { "index": "{}".format(resultssimilarity[i][1]) }
#             search_result = molecules.find(myquery)
#             for x in search_result:
#                 SMILES = x["smiles"]
#             compound_dict.append({ "SMILES": SMILES })
#         else: 
#             continue
#     return compound_dict


# def search_for_cat_no (SMILES):
#     m = rdkit.Chem.MolFromSmiles(SMILES)
#     rdkit.Chem.SanitizeMol(m)
#     SMILES = rdkit.Chem.MolToSmiles(m)
#     myquery = {"SMILES": "{}".format(SMILES)}
#     search_result = crude_vendors_data.find(myquery)
#     for i in search_result:
#         return i
