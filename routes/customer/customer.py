import hashlib
from random import randbytes

from fastapi import HTTPException, status, APIRouter, Request, Cookie, Depends
from routes.customer.customer_models import *
from database.database import database
from routes.authentication import val_token
from routes.emails import Email
from routes.user_registration import user_utils

customer_router = APIRouter()
customers_collection = database.get_collection('customers')
user_collection = database.get_collection('users')


@customer_router.post("/customer/register")
async def create_customer(customer: Customer, token: str = Depends(val_token)):
    if token[0] is True:
        details = customer.dict()
        customer_collection = database.get_collection('customers')
        print(customer_collection)
        customer = customers_collection.find_one({'phone': details["phone"]})
        find_user = user_collection.find_one({'email': token[1]['email']})
        if not customer:
            token = randbytes(10)
            hashedCode = hashlib.sha256()
            hashedCode.update(token)
            password = hashedCode.hexdigest()
            details['password'] = user_utils.hash_password(password)
            details['User_ids'] = [find_user['_id']]
            result = customer_collection.insert_one(details)
            await Email(token.hex(), details['email'], 'customer_register').send_email()
            if result.inserted_id:
                return {"status": f"New Customer- {details['name']} added",'message': 'Temporary password successfully sent to your email'}
            else:
                raise HTTPException(status_code=500, detail="Failed to insert data")
        else:
            raise HTTPException(status_code=409, detail=f"Customer {customer['name']} Exists")

    else:
        raise HTTPException(status_code=401, detail=token)


@customer_router.post("/edit/customer")
async def update_customer(edit_customer: EditCustomer, token: str = Depends(val_token)):
    from pymongo import ReturnDocument
    if token[0] is True:
        edit_customer = edit_customer.dict(exclude_none=True)
        customer_collection = database.get_collection('customers')
        customer = customers_collection.find_one({'phone': edit_customer["phone"]})
        if customer:
            edit_customer['updated_at']= datetime.utcnow()
            result = customer_collection.find_one_and_update({'_id': customer['_id']}, {'$set': edit_customer}, return_document=ReturnDocument.AFTER)

            if not result:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'Unable to Update for this Customer - {result}')
        else:
            raise HTTPException(status_code=409, detail=f"Customer {customer['phone']} does not Exists")

    else:
        raise HTTPException(status_code=401, detail=token)

    return {'status':f'Updated Customer Successfully- {customer["name"]}'}
