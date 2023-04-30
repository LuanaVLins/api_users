from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

class User(BaseModel):
    id: int
    nome: str
    login: str
    senha: str

users_db = []

@app.post("/users", status_code=201)
async def create_user(user: User):
    # Verifica se o login já existe
    for u in users_db:
        if u.login == user.login:
            raise HTTPException(status_code=400, detail="Login já cadastrado")
    users_db.append(user)
    return user


@app.put("/users/{login}")
async def update_user(login: str, user: User):
    for i, u in enumerate(users_db):
        if u.login == login:
            users_db[i] = user
            return user
    raise HTTPException(status_code=404, detail="Usuário não encontrado")


@app.delete("/users/{login}")
async def delete_user(login: str):
    for i, u in enumerate(users_db):
        if u.login == login:
            users_db.pop(i)
            return {"message": "Usuário excluído com sucesso"}
    raise HTTPException(status_code=404, detail="Usuário não encontrado")

@app.get("/users", response_model=List[User])
async def get_all_users():
    return users_db

@app.get("/users/{login}", response_model=User)
async def get_user_by_login(login: str):
    for u in users_db:
        if u.login == login:
            return u
    raise HTTPException(status_code=404, detail="Usuário não encontrado")
