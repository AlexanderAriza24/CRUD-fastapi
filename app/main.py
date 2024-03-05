from fastapi import FastAPI, HTTPException
from typing import Optional, Union
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import firebase_admin
from firebase_admin import credentials, db

app = FastAPI()

cred = credentials.Certificate("/code/app/bd-prueba-persona-taller-firebase-adminsdk-1xt6v-6ac6a954ae.json")
firebase_admin.initialize_app(cred, {
    "databaseURL":"https://bd-prueba-persona-taller-default-rtdb.firebaseio.com/users"
})

class User(BaseModel):
    id: int
    nombre: str


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


# Ruta para crear un nuevo usuario en la base de datos
@app.post("/users/")
async def create_user(user: User):
    new_user_ref = db.reference('users').push()  # Generar una nueva referencia
    new_user_ref.set({"id": new_user_ref.key, "nombre": user.nombre})  # Guardar el nuevo usuario en la base de datos
    return {"message": "User created successfully"}


# Ruta para obtener un usuario específico de la base de datos
@app.get("/users/")
async def read_user():
    user_ref = db.reference('users')
    user = user_ref.get()
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")


# Ruta para actualizar un usuario en la base de datos
@app.put("/users/{id}/")
async def update_user(id: str, user: User):
    user_ref = db.reference('users').child(id)
    if user_ref.get():
        user_ref.set({"id": id, "nombre": user.nombre})  # Actualizar el usuario en la base de datos
        return {"message": "User updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")

# Ruta para eliminar un usuario de la base de datos
@app.delete("/users/{id}/")
async def delete_user(id: str):
    user_ref = db.reference('users').child(id)
    if user_ref.get():
        user_ref.delete()  # Eliminar el usuario de la base de datos
        return {"message": "User deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")