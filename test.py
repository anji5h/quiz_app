import bcrypt
print(bcrypt.hashpw("admin".encode(), bcrypt.gensalt()).decode())