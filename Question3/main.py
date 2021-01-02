import hashlib

# encode it to bytes using UTF-8 encoding

message = "My name is Erick".encode()


# hash with SHA-3
print("SHA-3-256:", hashlib.sha3_256(message).hexdigest())

print("SHA-3-512:", hashlib.sha3_512(message).hexdigest())