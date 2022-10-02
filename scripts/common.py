import base64
import hashlib

def filename_for(prompt, number):
    hash_key = ('{}-{}'.format(prompt, number)).encode('ascii')
    b64 = base64.urlsafe_b64encode(hashlib.sha256(hash_key).digest())
    return b64.decode('ascii')