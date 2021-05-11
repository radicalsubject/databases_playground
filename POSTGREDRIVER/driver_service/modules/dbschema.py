import uuid, json 
import pickle, time, os
# import pymongo
"""
test_wallet = {
    "wallet_id": "1231241random uuid",
    "money": {
        "total": 1,
        "currency": "RUB"
    },
    "time": {
        "last_change_timestamp": "22.22.2020 14:00:35"
    },
    "ownership": {
        "list_of_owners": ["id1", "id2"]
    },
    "history_of_changes": [
        {
            "owner": "id1",
            "operation": [-2500, "RUB"],
            "timestamp": "22.22.2020 14:00:35"
        }
    ]
}
test = wallet(**test_wallet)
"""

class dbclassobject:
    """
    This is object for manipulating easily with wallet 
    attributes before sending updated data to database. 
    """
    pass