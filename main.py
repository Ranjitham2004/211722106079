from fastapi import FastAPI
from collections import deque
import httpx
import time
app = FastAPI()
WINDOW_SIZE = 10
number_window = deque(maxlen=WINDOW_SIZE)
URL_MAP = {
    "p": "http://20.244.56.144/evaluation-service/primes",
    "f": "http://20.244.56.144/evaluation-service/fibo",
    "e": "http://20.244.56.144/evaluation-service/even",
    "r": "http://20.244.56.144/evaluation-service/rand"
}
@app.get("/numbers/{numberid}")
async def get_numbers(numberid: str):
    url = URL_MAP.get(numberid)
    if not url:
        return{"error": "Invalid number id"}
    prev_window = list(number_window)

    try:
        async with httpx.AsyncClient(timeout=0.5) as client:
            start_time = time.time()
            response=await client.get(url)
            elapsed=time.time() - start_time
        if response.status_code != 200 or elapsed > 0.5:
            return{
                "windowPrevState": prev_window,
                "windowCurrState": list(number_window),
                "numbers": [],
                "avg":round(sum(number_window) / len(number_window),2)
if number_window else 0
            }
        
            new_numbers=response.json().get("numbers",[])
            for num in new_numbers:
                if num not in number_window:
                    number_window.append(num)
            curr_window=list(number_window)
            return{
                "windowPrevState": prev_window,
                "windowCurrState": curr_window,
                "numbers": new_numbers,
                "avg":round(sum(curr_window) / len(curr_window),2)
if curr_window else 0
            }
        
    except Exception:
        return{
            "windowPrevState": prev_window,
            "windowCurrState": list(number_window),
            "numbers": [],
            "avg":round(sum(number_window) / len(number_window),2)
if number_window else 0
        }                     