import bcrypt

passwords = ["password", "password", "password"]
for pw in passwords:
    print(bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt()).decode())
