from fastapi import FastAPI, HTTPException
from typing import List
import httpx

app = FastAPI()
window_size = 10
window: List[int] = []

VALID_IDS = {'p', 'f', 'e', 'r'}
API_ENDPOINTS = {
    'p': "http://20.244.56.144/evaluation-service/primes",
    'f': "http://20.244.56.144/evaluation-service/fibo",
    'e': "http://20.244.56.144/evaluation-service/even",
    'r': "http://20.244.56.144/evaluation-service/rand"
}

@app.get("/numbers/{numberid}")
async def get_numbers(numberid: str):
    if numberid not in VALID_IDS:
        raise HTTPException(status_code=400, detail="Invalid number ID")

    global window
    prev_state = window.copy()

    numbers = await fetch_numbers(numberid)

    for num in numbers:
        if num not in window:
            window.append(num)
            if len(window) > window_size:
                window.pop(0)

    avg = round(sum(window) / len(window), 2) if window else 0.0

    return {
        "windowPrevState": prev_state,
        "windowCurrState": window,
        "numbers": numbers,
        "avg": avg
    }

async def fetch_numbers(numberid: str) -> List[int]:
    url = API_ENDPOINTS[numberid]
    try:
        async with httpx.AsyncClient(timeout=0.5) as client:
            response = await client.get(url)
            if response.status_code == 200:
                return response.json().get("numbers", [])
    except httpx.RequestError:
        pass
    return []