from fastapi import FastAPI
import requests
import httpx
from httpx import HTTPError
from decouple import config

app = FastAPI()

TOKEN = config('TOKEN')
FAQIH_CHAT_ID = config('FAQIH_CHAT_ID')
SANDEEP_CHAT_ID = config('SANDEEP_CHAT_ID')


@app.post('/sendMessage')
async def send_message(req: dict):
    try:
        text = req["message"]
        tg_faqih_message = {
            "chat_id": FAQIH_CHAT_ID,
            "text": text
        }
        tg_sandeep_message = {
            "chat_id": SANDEEP_CHAT_ID,
            "text": text
        }
        API_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        async with httpx.AsyncClient() as client:
            await client.post(API_URL, json=tg_faqih_message)
            # await client.post(API_URL, json=tg_sandeep_message)

        res = f"Message '{text}' sent"
        return res
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

