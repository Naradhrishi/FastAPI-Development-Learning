from pwdlib import PasswordHash


password_hash = PasswordHash.recommended()

# function to hash the plain password
def hash_password(password: str):
    return password_hash.hash(password)

# function to verify hash password with plane password
def verify_password(password: str,  hashed_password: str):
    return password_hash.verify(password, hashed_password)





