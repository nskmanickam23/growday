import hashlib
from random import randbytes

from fastapi import HTTPException, status, APIRouter, Request, Cookie, Depends

from routes.business.business_register import user_collection
from routes.members.members_models import *
from database.database import database
from routes.authentication import val_token
from routes.user_registration import user_utils

members_router = APIRouter()
members_collection = database.get_collection('members')


#
# @members_router.post("/member/register")
# async def add_member_to_tenant(member: Members, token: str = Depends(val_token)):
#     if token[0] is True:
#         payload = token[1]
#         from database.database import mongo_conn
#         conn = mongo_conn()
#         db = conn['growday']
#         register = db.users
#         members = db.members
#         user = await register.find_one({'email': payload["email"]})
#         if user:
#             details = member.dict()
#             details['password'] = user_utils.hash_password(details['password'])
#             details['tenant_id'] = user['_id']
#             print(details['email'])
#             existing_data = await members.find_one({'email': details['email']})
#             print(existing_data)
#             if existing_data:
#                 raise HTTPException(status_code=409, detail=f"User {details['name']} Exists")
#             else:
#                 result = await members.insert_one(details)
#                 if result.inserted_id:
#                     return {"member": details['name']}
#                 else:
#                     raise HTTPException(status_code=500, detail="Failed to insert data")
#         else:
#             raise HTTPException(status_code=404, detail="User not found")
#     else:
#         raise HTTPException(status_code=401, detail=token)


@members_router.post("/member/register")
async def create_member(member: Members, token: str = Depends(val_token)):
    if token[0] is True:
        details = member.dict()
        customer_collection = database.get_collection('members')
        print(customer_collection)
        member = members_collection.find_one({'email': details["email"]})
        if not member:
            result = members_collection.insert_one(details)
            if result.inserted_id:
                update_user = user_collection.update_one({'email': token[1]['email']}, {
                    '$push': {'members': {'member_id': result.inserted_id, 'member_name': details['name']}}},
                                                         upsert=True)

                if update_user:
                    update_business_users = members_collection.update_one({'_id': ObjectId(result.inserted_id)}, {
                        '$push': {'User_ids': [result.inserted_id]}
                    }, upsert=True)
                    return {"status": f"New member- {details['name']} added"}
            else:
                raise HTTPException(status_code=500, detail="Failed to insert data")
        else:
            raise HTTPException(status_code=409, detail=f"Member {member['email']} Exists")

    else:
        raise HTTPException(status_code=401, detail=token)


@members_router.post("/edit/member")
async def edit_member(member: Members, token: str = Depends(val_token)):
    if token[0] is True:
        details = member.dict()
        # members_collection = database.get_collection('members')
        member = members_collection.find_one({'email': details["email"]})
        details['updated_time'] = datetime.utcnow()
        if member:
            if member['role'] == 'admin':
                result = members_collection.update_one({"_id": member["_id"]}, {"$set": details})
                print(result)
                if result:
                    return {"message": "Member updated successfully"}
                else:
                    raise HTTPException(status_code=500, detail="Failed to insert data")
            else:
                raise HTTPException(status_code=401, detail='User does not have permission to update')
        else:
            raise HTTPException(status_code=409, detail=f"{member['email']} does not  Exists")

    else:
        raise HTTPException(status_code=401, detail=token)
