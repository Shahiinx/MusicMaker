import os
from os import getenv
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from OWNER import BOT_TOKEN, OWNER, OWNER_ID, infophoto, OWNER_NAME, DATABASE, CHANNEL, GROUP, LOGS, PHOTO, VIDEO

if os.path.exists("local.env"):
    load_dotenv("local.env")

load_dotenv()
admins = {}
user = {}
appp = {}
call = {}
logger = {}
logger_mode = {}
botname = {}
helper = {} 
mo = AsyncIOMotorClient(DATABASE)
moo = mo["data"] 
Bots = moo.yousef  
db = moo  
botdb = db.botdb 
blockdb = db.blocked  


API_ID = int(getenv("API_ID", "17490746"))
API_HASH = getenv("API_HASH", "ed923c3d59d699018e79254c6f8b6671")
BOT_TOKEN = BOT_TOKEN
MONGO_DB_URL = DATABASE
OWNER = OWNER
OWNER_ID = OWNER_ID
infophoto = infophoto
OWNER_NAME = OWNER_NAME
CHANNEL = CHANNEL
GROUP = GROUP
PHOTO = PHOTO
LOGS = LOGS
VIDEO = VIDEO
