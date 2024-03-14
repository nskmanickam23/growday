from datetime import date, datetime, time, timedelta
from typing import List, Optional
from typing import List
from pydantic import BaseModel, EmailStr, constr
from bson.objectid import ObjectId


class Customer(BaseModel):
    name: str
    email: str
    password: str
    phone: str
    business_ids: list[str]
    created_at: datetime


class EditCustomer(BaseModel):
    name: str or None = None
    email: str or None = None
    phone: str or None = None


