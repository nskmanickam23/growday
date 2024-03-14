from datetime import date, datetime, time, timedelta
from typing import List, Optional
from typing import List
from pydantic import BaseModel, EmailStr, constr
from bson.objectid import ObjectId


class Domain(BaseModel):
    subdomain_url: str or None = None
    custom_domain: str or None = None


class Business(BaseModel):
    name: str
    bussiness_type: str
    desctription: str
    created_date: datetime or None = None
    address: str
    domain_url: str or None = None
    business_url: Domain or None = None
    created_by: str or None = None


class EditBusiness(BaseModel):
    name: str or None = None
    email: str or None = None
    phone: str or None = None
    address: str or None = None
    business_url: Domain or None = None
    bussiness_type: str or None = None
    desctription: str or None = None
