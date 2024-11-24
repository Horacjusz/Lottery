from settings.tokens import *
from models.models import User, Item
from services.database import datasession
from services.file_service import get_all_ids

def get_free_id(kind) :
    ids = get_all_ids(kind)
    if len(ids) == 0 : return 1
    for i in range(1, len(ids)) :
        if ids[i] - ids[i - 1] > 1 :
            return ids[i - 1] + 1
    return ids[-1] + 1