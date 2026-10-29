from fastapi import FastAPI
from utility.database import engine, Base
from models.user.model import User

# Routes
from routes.auth import router as auth_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get('/')
def main():
    return {"Backend API is running."}

app.include_router(auth_router)



# @app.get('/products')
# def get_products(db: Session = Depends(get_db)):
    
#     result = db.execute(
#         text("""SELECT * FROM products""")
#     )

#     return result.mappings().all()