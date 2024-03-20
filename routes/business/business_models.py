from datetime import date, datetime, time, timedelta
from typing import List, Optional
from typing import List
from pydantic import BaseModel, EmailStr, constr
from bson.objectid import ObjectId


class Domain(BaseModel):
    subdomain_url:  Optional[str] = None
    custom_domain:  Optional[str] = None


class Business(BaseModel):
    name: str
    bussiness_type: str
    desctription: Optional[str] = None
    created_date: datetime or None = None
    address: str
    domain_url:  Optional[str] = None
    business_url:  Optional[str] = None
    created_by: str or None = None


class EditBusiness(BaseModel):
    name: str
    email: str or None = None
    phone: str or None = None
    address: str or None = None
    business_url: Domain or None = None
    bussiness_type:  Optional[str] = None
    desctription:  Optional[str] = None
