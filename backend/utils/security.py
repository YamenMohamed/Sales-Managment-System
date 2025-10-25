import bcrypt

def hash_password(plain_password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


# from utils.security import verify_password

# if verify_password(input_password, stored_user.password):
    # print("✅ Login successful")
# else:
    # print("❌ Invalid password")