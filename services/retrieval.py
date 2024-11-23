import os
from settings.settings import USERS_PATH, ITEMS_PATH
from settings.tokens import *
from models.models import User, Item
from services.file_service import datasession

def get_all_ids(kind, include_zero=False):
    """
    Get all IDs from the database for the specified kind (USERS or ITEMS).
    
    Args:
        kind (str): The type of objects to query ('USERS' or 'ITEMS').
        include_zero (bool): Whether to include ID 0 in the results.

    Returns:
        list: A sorted list of IDs.
    """
    ids = []
    try:
        if kind == USERS:
            query = datasession.query(User.user_id)
        elif kind == ITEMS:
            query = datasession.query(Item.item_id)
        else:
            raise ValueError("Invalid kind specified. Must be USERS or ITEMS.")
        
        # Fetch all IDs
        ids = [row[0] for row in query.all()]
        
        # Filter out zero if include_zero is False
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

