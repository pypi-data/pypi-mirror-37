import hashlib
import base64

def _char_filter(password, unavailable_char):
    for char in unavailable_char:
        password = password.replace(char, '')
    return password
    
def generate(site, user, master_password, max_length=0, unavailable_char=''):
    password = _char_filter(base64.b64encode(hashlib.sha512(site + user + master_password).hexdigest()), unavailable_char)
    if max_length == 0:
        return password
    else:
        return password[0:max_length]
        
