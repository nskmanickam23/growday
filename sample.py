# import hashlib
# from random import randbytes
#
# token = randbytes(10)
# hashedCode = hashlib.sha256()
# hashedCode.update(token)
# verification_code = hashedCode.hexdigest()
# print(verification_code)
# print(token.hex())
# hashedCode = hashlib.sha256()
# hashedCode.update(bytes.fromhex(token.hex()))
# verification_code = hashedCode.hexdigest()
# hashed_code = hashlib.sha1(hashedCode).hexdigest()  # Example hashed code
# digits = int(hashed_code, 16)  # Convert hexadecimal to integer
# print(digits)
# print(verification_code)
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Your endpoints go here
@app.get("/")
async def read_root():
    return {"message": "Hello, CORS enabled!"}


if __name__ == "__main__":
    uvicorn.run(app, port=8005)
