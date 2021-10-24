from fastapi import FastAPI
import requests
import httpx
from httpx import HTTPError
from decouple import config

app = FastAPI()

TOKEN = config('TOKEN')


@app.post('/sendMessage')
async def send_message(req: dict):
    try:
        chat_id = req["chat_id"]
        text = req["message"]
        tg_message = {
            "chat_id": chat_id,
            "text": text
        }
        API_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        async with httpx.AsyncClient() as client:
            await client.post(API_URL, json=tg_message)

        res = f"Message '{text}' sent"
        return res
    except Exception as e:
        print(e)
        raise HTTPError("Send message error")


@app.get('/getChatId')
async def get_chat_id():
    try:
        API_URL = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
        async with httpx.AsyncClient() as client:
            request = await client.get(API_URL)
            response = request.json()
            result_length = len(response["result"])
            latest_message = response["result"][result_length - 1]
            sender_chat_id = latest_message["message"]["from"]["id"]
            return sender_chat_id

    except Exception as e:
        print(e)
        raise HTTPError("Send message error")


@app.get('/getFPLUpdates')
async def get_fpl_updates():
    try:
        request = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/")
        response = request.json()
        fpl_details = response['events'][3]
        deadline_time = fpl_details['deadline_time']
        print(deadline_time)
        return fpl_details
    except Exception as e:
        print(e)
        raise HTTPError("Send message error")

