from fastapi import HTTPException
from fastapi import APIRouter, Response
from config.db import con
from models.user import users
from schemas.user import User
from cryptography.fernet import Fernet
from starlette.status import HTTP_204_NO_CONTENT
from typing import List
Access-Control-Allow-Origin: <origin> | *

user = APIRouter()
key = Fernet.generate_key()
f = Fernet(key)


@user.get("/pruebas", response_model=List[User])
def get_users():
    # devuelme todos los usuarios sin su ID
    return con.execute(users.select()).fetchall()

# -----------------------------------------------------------------------------INFORMACION-GENERAL-------------------------------------------------------------------


@user.get("/")
def get_informacion():
    info_list = [
        "INFORMACION SOBRE LA RUTAS ESPECIFICAS DE TRABAJO",
        "'/allusers': Muetra todos los usuarios de la base de datos.",
        "'/addusers': Crea un nuevo usuario, debes enviar los datos, 'name','email', y una 'password.",
        "'/user/id': Consulta un usuario en especifico de la base de datos por su ID.",
        "'/delete/id': Elimina a un usuario de la base de datos por su ID",
        "'/update/id': Actualiza la informacion de un usuario por su ID"
    ]
    return info_list

# ----------------------------------------------------------------MOSTRAR-TODOS-------------------------------------------------------------------------------------------------


@user.get("/allusers")
def get_users():
    results = con.execute(users.select()).fetchall()
    # Convertir los resultados a una lista
    users_list = [
        {"id": row.id, "name": row.name, "email": row.email}
        for row in results
    ]
    return users_list
# ------------------------------------------------------------------AÑADIR-----------------------------------------------------------------------------------------


@user.post("/addusers")
def create_user(user: User):
    new_user = {"name": user.name, "email": user.email,
                "password": f.encrypt(user.password.encode("utf-8"))}
    datos = con.execute(users.insert().values(new_user))
    con.commit()
    user_id = datos.lastrowid
    created_user = con.execute(
        users.select().where(users.c.id == user_id)).first()

    return {"id": created_user.id, "name": created_user.name, "email": created_user.email}

# ------------------------------------------------------------------BUSCAR-X-ID-------------------------------------------------------------------------------------


@user.get("/user/{id}")
def mostrar(id: int):
    consulta = con.execute(users.select().where(users.c.id == id)).first()
    if consulta:
        user_dict = {"id": consulta.id,
                     "name": consulta.name, "email": consulta.email}
        return user_dict
    else:
        return {"message": "Usuario no encontrado"}

# -----------------------------------------------------------------ELIMINAR----------------------------------------------------------------------------------------


@user.delete("/delete/{id}")
def delete_user(id: int):
    eliminado = con.execute(users.delete().where(users.c.id == id))
    con.commit()
    return "Eliminado"
# -----------------------------------------------------------------ACTUALIZAR---------------------------------------------------------------------------------------


@user.put("/update/{id}")
def update_user(id: int, user: User):
    con.execute(users.update().values(
        name=user.name,
        email=user.email,
        password=f.encrypt(user.password.encode("utf-8")))
        .where(users.c.id == id))
    con.commit()
    return "updated"

#----------------------------------------------------------------CONSULTA POR CORREO Y CONTRASEÑA----------------------------------------------------------------------------

@user.get("/user")
def mostrar(email: str, password: str):
    encrypted_password = f.encrypt(password.encode("utf-8"))
    consulta = con.execute(users.select().where(users.c.email == email, users.c.password == encrypted_password)).first()
    if consulta:
        user_dict = {"id": consulta.id,
                     "name": consulta.name, "email": consulta.email}
        return user_dict
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
