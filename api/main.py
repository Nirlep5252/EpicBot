import os
from aiohttp import ClientSession, BasicAuth
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from icecream import ic

load_dotenv()
app = FastAPI()

API_ENDPOINT = "https://discord.com/api/v10"
REDIRECT_URI = "http://localhost:5173/oauth2/redirect"
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

if not CLIENT_ID or not CLIENT_SECRET:
    raise Exception("CLIENT_ID and CLIENT_SECRET must be set")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/token/{code}")
async def get_token(request: Request, code: str):
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    async with ClientSession() as session:
        async with session.post(
            f"{API_ENDPOINT}/oauth2/token",
            data=data,
            headers=headers,
            auth=BasicAuth(CLIENT_ID, CLIENT_SECRET),
        ) as resp:
            content = await resp.json()
            ic(content)
            return JSONResponse(status_code=resp.status, content=await resp.json())


@app.get("/user/{access_token}")
async def get_user(request: Request, access_token: str):
    headers = {"Authorization": f"Bearer {access_token}"}
    async with ClientSession() as session:
        async with session.get(f"{API_ENDPOINT}/users/@me", headers=headers) as resp:
            content = await resp.json()
            ic(content)
            return JSONResponse(status_code=resp.status, content=await resp.json())
