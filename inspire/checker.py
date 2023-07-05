from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from random import randint

def valid_password(p):
    rules = [
        lambda s: any(x.isupper() for x in p),
        lambda s: any(x.islower() for x in p),  
        lambda s: any(x.isdigit() for x in p),  
        lambda s: not any(x == " " for x in p),
        lambda s: len(s) >= 8     
    ]
    
    if all(rule(p) for rule in rules):
        return True
    else:
        return False
    
def valid_username(u):
    prohibited = "\"\'\\/-@"
    rules = [
        lambda s: not any(x in prohibited for x in u),
        lambda s: not any(x == " " for x in u),
        lambda s: len(s) > 0 and len(s) < 30
    ]

    if all(rule(u) for rule in rules):
        return True
    else:
        return False
    
def valid_email(em):
    try:
        validate_email(em)
    except ValidationError:
        return False
    else:
        return True
    
def random_code():
    code = ""
    for i in range(6):
        code += str(randint(0,9))

    return code
