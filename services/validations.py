from datetime import datetime
from utils.constants import STAGE_LOCKS

def is_stage_open(etapa: str) -> bool:
    lock_date=datetime.strptime(
        STAGE_LOCKS[etapa],
        "%Y-%m-%d %H:%M:%S"
    )

    return datetime.now() < lock_date

def validate_user_id(user_id:str):
    user_id = user_id.strip()

    if not user_id:
        return False, 'Debes ingresar tu número de celular.'
    
    if not user_id.isdigit():
        return False, 'El número celular solo debe contener dígitos.'
    
    if len(user_id) !=10:
        return False, 'El número de celular debe contener exactamente 10 dígitos.'
    
    return True, user_id

def validate_user_name(user_name):

    if not user_name.strip():

        return False, (
            "Debes ingresar tu nombre."
        )

    return True, user_name.strip()