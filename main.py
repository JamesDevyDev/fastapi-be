from fastapi import FastAPI, Depends, HTTPException
from model import Product
from database import session, engine
import database_models
from sqlalchemy.orm import Session
from sqlalchemy import text

app = FastAPI()

database_models.Base.metadata.create_all(bind=engine)

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

    
@app.get('/')
def main():
    return {"All is working"}

@app.get('/products')
def get_products(db: Session = Depends(get_db)):
    
    result = db.execute(
        text("""SELECT * FROM products""")
    )

    return result.mappings().all()
     
@app.get("/product/{id}")
def get_queried_products(id: int, db: Session = Depends(get_db)):

    result = db.execute(
        text("""
            SELECT *
            FROM products
            WHERE id = :id
        """),
        {"id": id}
    )

    product = result.mappings().first()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found."
        )

    return product

@app.post('/product/add')
def add_product(name:str, description:str, db: Session = Depends(get_db)):
    
    if not name:
        raise HTTPException(status_code=400, detail="Name is required.")

    if not description:
        raise HTTPException(status_code=400, detail="Description is required.")

    db.execute(
                text("""
                        INSERT INTO products(name, description)
                        VALUES(:name, :description)
                    """
                    ),{"name" :name, "description" : description})
    
    db.commit()
    return {"success": {"message": "Product has been added successfully."}}
    
@app.delete('/product/{id}')
def delete_product(id:int, db: Session = Depends(get_db)):
    
    if not id:
        raise HTTPException(status_code=400, detail="id is required.")
    
    
    result = db.execute(
                text("""
                    DELETE FROM products
                    WHERE id = :id
                    RETURNING id
                    """),{"id" : id}
            )
    
    if result.first() is None:
        raise HTTPException(
            status_code=400,
            detail="id does not exist"
        )
    
    db.commit()
   
    return {"success": {"message": "Product has been deleted successfully."}}
        
@app.patch('/product/{id}')
def update_product(id:int, name:str, description:str, db: Session = Depends(get_db)):
    
    db.execute(
        text("""
             UPDATE products
             SET name = :name,
             description = :description
             WHERE id = :id
             RETURNING id
             """),{"id":id, "name":name, "description":description}
    )
    
    db.commit()
    return {"success" : "product has been updated."}