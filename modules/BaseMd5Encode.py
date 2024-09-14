from hashlib import md5

def base_md5_endcode(value):
    return md5(str(value).encode('utf-8')).hexdigest()

