import hashlib
from random import randbytes

import uvicorn
from fastapi import Depends, FastAPI
from bson import json_util
import json
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
from bson.json_util import dumps, loads

# templates
from fastapi.templating import Jinja2Templates

# upload images
from fastapi.staticfiles import StaticFiles
# CORS headers
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder

app = FastAPI()

# CORS url
origins = [
    '*'
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

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, datetime):
            return obj.isoformat()
        else:
            return super().default(obj)


@app.get("/<collection_name>/list")
def list_customers(collection_name, token: str = Depends(val_token)):
    if token[0] is True:
        print(collection_name)
        print(database)
        if database.collection_exists(collection_name):
            list_collections = database.get_collection(collection_name)
            # Retrieve all documents from the collection
            user_collection = database.get_collection('users')
            find_user = user_collection.find_one({'email': token[1]['email']})
            if find_user:
                search_criteria = {
                    "User_ids": {
                        "$elemMatch": {
                            "$elemMatch": {
                                "$in": [
                                    find_user['_id']
                                ]
                            }
                        }
                    }
                }
                print(search_criteria)

                # Find documents matching the search criteria
                cursor = list_collections.find(search_criteria)
                # # Iterate over the results
                # document_list = []
                # for document in cursor:
                #     document_list.append(document)
                # # print(list_collections)
                # records = []
                # for document in list_collections.find({}):
                #     document = json.loads(json_util.dumps(document))
                #     records.append(document)
                # print("---",business_list)
                # print(list(cursor))
                documents_list = list(cursor)
                from fastapi.responses import JSONResponse

                return json.loads(json_util.dumps(documents_list))
        else:
            raise HTTPException(status_code=404, detail='Collection Not Found')
    else:
        raise HTTPException(status_code=401, detail=token)


@app.get("/health")
def index():
    return {"Message": "Service is Up"}


if __name__ == "__main__":
    uvicorn.run(app, port=8004)
