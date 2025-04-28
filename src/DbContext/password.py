import bcrypt

def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def check_password(stored_hash, password):
    return bcrypt.checkpw(password.encode('utf-8'), stored_hash)

