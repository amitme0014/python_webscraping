from fastapi import FastAPI
from pydantic import BaseModel #yeh pojo class ki tarah kaam aata
import urllib
import os

#Fast api comes automatically with swagger '/docs daalo bas ya fir /redoc'
app = FastAPI()

#Connecting postgres db
host_server=os.environ.get('host_server','localhost')
db_server_port=urllib.parse.quote_plus(str(os.environ.get('db_server_port','5432')))
database_name=os.environ.get('database_name','fastapi_crud')
db_username=urllib.parse.quote_plus(str(os.environ.get('db_username','postgres')))
db_password=urllib.parse.quote_plus(str(os.environ.get('db_password','postgres')))
ssl_mode=urllib.parse.quote_plus(str(os.environ.get('ssl_mode','prefer')))
DATABASE_URL='postgresql://{}:{}@{}:{}/{}?sslmode={}'.format(db_username,db_password,host_server,db_server_port,database_name,ssl_mode)

import sqlalchemy

metadata=sqlalchemy.MetaData()

notes=sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("completed", sqlalchemy.Boolean),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, pool_size=3, max_overflow=0, echo=True
)

#Below command will create the schema if it doesn't exist 
metadata.create_all(engine)

from pydantic import BaseModel

class NoteIn(BaseModel):
    text: str
    completed: bool

class Note(BaseModel):
    id: int
    text: str
    completed: bool

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List

app=FastAPI(title="REST API using FastAPI Postgresql Async Endpoints")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

import databases

database=databases.Database(DATABASE_URL)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/notes/", response_model=Note)
async def create_note(note: NoteIn):
    query = notes.insert().values(text= note.text, completed=note.completed)
    last_record_id = await database.execute(query)
    return {**note.dict(), "id": last_record_id}

#https://www.youtube.com/watch?v=kCggyi_7pHg


db=[]

class City(BaseModel):
    name: str
    timezone: str
     

@app.get('/create')
def index():
    return{'key':'value'}
'''
@app.get('/gitlab_hit')
def hitApi():
    
    return{"client_host":resp_recvd}

@app.get('/index')
def index():
    return{'key':'index_value'}

@app.get('/cities')
def get_cities():
    return db

#@app.get('/cities/{city_id}')

#iska matlab isko City type ka object chahiye
#db.append mein city type k object ko dictionary mein convert kiya gaya aur phir db list mein store kara diya
#db[-1] returns last item from list
@app.post('/cities')
def create_city(city: City):
    db.append(city.dict())
    return db[-1]

@app.delete('/cities/{city_id}')
def delete_city(city_id: int):
    db.pop(city_id-1)
    return "deleted"
    '''