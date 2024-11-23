from settings.tokens import *
from models.models import User, Item
from services.file_service import datasession

def get_all_ids(kind, include_zero=False):
    ids = []
    try:
        if kind == USERS:
            query = datasession.query(User.user_id)
        elif kind == ITEMS:
            query = datasession.query(Item.item_id)
        else:
            raise ValueError("Invalid kind specified. Must be USERS or ITEMS.")
        
        ids = [row[0] for row in query.all()]
        
        if not include_zero:
            ids = [id for id in ids if id != 0]
    except Exception as e:
        print(f"Error querying IDs from the database: {e}")
    
    return sorted(ids)

def get_free_id(kind) :
    ids = get_all_ids(kind)
    if len(ids) == 0 : return 1
    for i in range(1, len(ids)) :
        if ids[i] - ids[i - 1] > 1 :
            return ids[i - 1] + 1
    return ids[-1] + 1

