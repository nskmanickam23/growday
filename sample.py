import hashlib
from random import randbytes

token = randbytes(10)
hashedCode = hashlib.sha256()
hashedCode.update(token)
verification_code = hashedCode.hexdigest()
print(verification_code)
print(token.hex())
hashedCode = hashlib.sha256()
hashedCode.update(bytes.fromhex(token.hex()))
verification_code = hashedCode.hexdigest()
hashed_code = hashlib.sha1(hashedCode).hexdigest()  # Example hashed code
digits = int(hashed_code, 16)  # Convert hexadecimal to integer
print(digits)
print(verification_code)