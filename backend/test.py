import hashlib

password = "your_password"
hashedPassword = hashlib.sha256(password.encode()).hexdigest()
print(hashedPassword)
