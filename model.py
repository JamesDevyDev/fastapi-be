from pydantic import BaseModel

class Product(BaseModel): 
    id :int
    name: str
    description: str
    
class ProductCreate(BaseModel):
    name: str
    description: str

class ProductUpdate(BaseModel):
    name: str
    description: str