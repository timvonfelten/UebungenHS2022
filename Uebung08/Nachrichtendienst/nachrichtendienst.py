import uvicorn
from fastapi import FastAPI, Depends, status, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi.templating import Jinja2Templates
from jinja2 import Template
import databases
from fastapi import FastAPI, Request, Form
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData
from jinja2 import Environment, FileSystemLoader



# Datenbank
database = databases.Database("sqlite:///datenbank.db")
engine = create_engine("sqlite:///datenbank.db", connect_args={"check_same_thread": False})

metadata = MetaData()
notes = Table(
    "notes", metadata,
    Column("id", Integer, primary_key = True),
    Column("user", String),
    Column("title", String),
    Column("text", String)
)
metadata.create_all(engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates/")
environment = Environment(loader=FileSystemLoader("templates/"))


manager = LoginManager("gkiuzgftzifztffgouguoguvukvgzuv", token_url="auth/login", use_cookie = True)
manager.cookie_name = "ch.fhnw.test"

DB = {
    "luuk": {"name": "Luuk", "email": "luuk.musig@fhnw.ch", "password": "eiszwöi"}, 
    "sgb": {"name": "Sara", "email": "sara.rap@fhnw.ch", "password": "eiszwöi"},
    "knäck": {"name": "David Lukas Kohler", "email": "k.nack@fhnw.ch", "password": "eiszwöi"}}

@app.on_event("startup")

async def startup():
    print("Verbinde Datenbank")
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    print("Beende DB Verbindung")
    await database.disconnect()


@manager.user_loader()
def load_user(username: str):
    user = DB.get(username)
    return user

@app.post("/auth/login")
def login(data: OAuth2PasswordRequestForm = Depends()):
    username = data.username
    password = data.password

    user = load_user(username)

    if not user:
        raise InvalidCredentialsException

    elif password != user['password']:
        raise InvalidCredentialsException

    access_token = manager.create_access_token(data={"sub":username})
    global currentUser
    currentUser = username

    resp = RedirectResponse(url="/new",status_code=status.HTTP_302_FOUND)
    manager.set_cookie(resp, access_token)

    return resp

@app.get("/login")
def login():
    file = open("templates/login.html", encoding="utf-8")
    data = file.read()
    file.close()
    return HTMLResponse(content=data)

@app.get("/notes")
async def read_notes():

    s = notes.select()
    result = engine.execute(s)
    list = []
    for zeile in result:
        #print(zeile)
        list.append(zeile)
    l = reversed(list)
    template = environment.get_template("notes.html")
    output = template.render(test="löu", notes=l)
    return HTMLResponse(content=output)

@app.get("/new", response_class=HTMLResponse)
async def create_note(request: Request, user=Depends(manager)):
    return templates.TemplateResponse("form.html", context={"request": request})

@app.post("/new")
async def post_note(title=Form(),text=Form(),user=Depends(manager)):
    query = notes.insert().values(title=title, text=text, user=currentUser)
    myid = await database.execute(query)
    #return templates.TemplateResponse("form.html", context={"request": request})
    #return {"id": myid, "user": currentUser, "titel": title, "text": text}
    resp = RedirectResponse(url="/new",status_code=status.HTTP_302_FOUND)
    return resp

@app.get("/private", response_class=HTMLResponse)
def getPrivateendpoint(user=Depends(manager)):
    return "Hello " + str(user["name"]) 

@app.get("/login",response_class=HTMLResponse)
def loginwithCreds():
    with open("templates/login.html") as f:
        return HTMLResponse(content=f.read()) 

@app.get("/users")
def display_users():
    template = environment.get_template("users.html")
    output = template.render(test="löu", users=DB)
    print(output)
    return HTMLResponse(content=output) 


for user in DB:
    @app.get("/users/"+user)
    async def read_notes(user=user):
   
        ##query = notes.select().where(notes.c.user == user)
        #return await database.fetch_all(query)

        s = notes.select().where(notes.c.user == user)
        result = engine.execute(s)
        list = []
        for zeile in result:
            #print(zeile)
            list.append(zeile)
        l = reversed(list)
        template = environment.get_template("user.html")
        output = template.render(notes=l)
        return HTMLResponse(content=output)
    


uvicorn.run(app, host="127.0.0.1", port=8000) 