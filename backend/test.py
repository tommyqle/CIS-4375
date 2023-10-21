import hashlib

password = input("Enter string to hash:\n")
hashedPassword = hashlib.sha256(password.encode()).hexdigest()
print(hashedPassword)
