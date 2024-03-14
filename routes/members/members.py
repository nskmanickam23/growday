import hashlib
from random import randbytes

from fastapi import HTTPException, status, APIRouter, Request, Cookie, Depends
from routes.members.members_models import *
from database.database import database
from routes.authentication import val_token
from routes.user_registration import user_utils

members_router = APIRouter()
members_collection = database.get_collection('members')


@members_router.post("/member/register")
async def add_member_to_tenant(member: Members, token: str = Depends(val_token)):
    if token[0] is True:
        payload = token[1]
        from database.database import mongo_conn
        conn = mongo_conn()
        db = conn['growday']
        register = db.users
        members = db.members
        user = await register.find_one({'email': payload["email"]})
        if user:
            details = member.dict()
            details['password'] = user_utils.hash_password(details['password'])
            details['tenant_id'] = user['_id']
            print(details['email'])
            existing_data = await members.find_one({'email': details['email']})
            print(existing_data)
            if existing_data:
                raise HTTPException(status_code=409, detail=f"User {details['name']} Exists")
            else:
                result = await members.insert_one(details)
                if result.inserted_id:
                    return {"member": details['name']}
                else:
                    raise HTTPException(status_code=500, detail="Failed to insert data")
        else:
            raise HTTPException(status_code=404, detail="User not found")
    else:
        raise HTTPException(status_code=401, detail=token)
