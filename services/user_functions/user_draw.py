from services.retrieval import get_all_ids
from services.file_service import load_user_file
from services.permutation_service import kth_permutation_fast, random_permutation
from math import factorial
from settings.tokens import *

def get_all_ch(oosers = True) :
    ids = get_all_ids(USERS)
    ch = []
    for ID in ids :
        user = load_user_file(ID)
        if user[CHOOSABLE] and user[VISIBLE] :
            check_val = user[ASSIGNED_TO]
            if oosers :
                check_val = user[ASSIGNMENT]
            if check_val is None :
                ch.append(user[USER_ID])
    return ch

def get_all_choosers() :
    return get_all_ch(oosers = True)

def get_all_choosable() :
    return get_all_ch(oosers = False)

def can_be_assigned(user_id, assignment_id) :
    user_spouse = load_user_file(user_id)[SPOUSE]
    assignment_spouse = load_user_file(assignment_id)[SPOUSE]
    
    identity_fail = user_id == assignment_id
    spouse_fail = user_id == assignment_spouse or user_spouse == assignment_id
    
    return not (identity_fail or spouse_fail)


def generate_valid_assignment(choosers = None, choosable = None) :
    
    if choosers is None :
        choosers = get_all_choosers()
    if choosable is None :
        choosable = get_all_choosable()
        
    for k in random_permutation(factorial(len(choosable))) :
        assignment = kth_permutation_fast(choosable, k)
        valid = True
        for i in range(len(choosers)) :
            if not can_be_assigned(choosers[i], assignment[i]) :
                valid = False
                break
        
        if valid :
            return assignment
    return None