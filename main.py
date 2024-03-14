import hashlib
from random import randbytes

import uvicorn
from fastapi import Depends, FastAPI

from routes.authentication import val_token
from routes.user_registration.user_models import *
from routes import authentication
from routes.user_registration import user_actions
from routes.customer import customer
from routes.business import business_register
from routes.members import members
from routes.emails import *
from database.database import database
# auth
from fastapi.security import (OAuth2PasswordBearer)

# templates
from fastapi.templating import Jinja2Templates

# upload images
from fastapi.staticfiles import StaticFiles
# CORS headers
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS url
origins = [
    'http://localhost:3000'
]

# adding middleware
app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=['*'],
                   allow_headers=['*']
                   )

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

# config for static files
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(authentication.auth_router,  tags=["authentication"])
app.include_router(user_actions.user_router, tags=["users"])
app.include_router(members.members_router,  tags=["members"])
app.include_router(customer.customer_router,  tags=["customer"])
app.include_router(business_register.business_router, tags=["business"])


@app.get("/<collection_name>/list")
def list_customers(collection_name, token: str = Depends(val_token)):
    if token[0] is True:
        print(collection_name)
        if database.collection_exists(collection_name):
            list_collections = database.get_collection(collection_name)
            # Retrieve all documents from the collection
            records = []
            for document in list_collections.find({}):
                document.pop('_id')
                records.append(document)
            return {"records": records}
        else:
            raise HTTPException(status_code=404, detail='Collection Not Found')
    else:
        raise HTTPException(status_code=401, detail=token)


@app.get("/health")
def index():
    return {"Message": "Service is Up"}


if __name__ == "__main__":
    uvicorn.run(app, port=8004)
