import hashlib

# Run this to get the hashed password, then add that hash to the SQL database's users table as the password value

password = input("Enter password to hash:\n")
hashedPassword = hashlib.sha256(password.encode()).hexdigest()
print(hashedPassword)

"""
References
    CIS3368 Code
"""