
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Calculator API")

# allow backend to access frontend if hosted on different domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# input class type for average calculation
class StockInput(BaseModel): 
    numbers: List[float]
#input class type for statistics calculation
class PricesInput(BaseModel):
    prices: List[float]

# API endpoint for average calculation of the stock prices
@app.post("/average_stock_prices")
async def calculate_average(stock_data: StockInput):
    
    # Validate input data
    if not stock_data.numbers:
        raise HTTPException(status_code=400, detail="Input data is empty")
    
    # Calculate average of the input stock prices
    sum_of_numbers = sum(stock_data.numbers)
    average = sum_of_numbers / len(stock_data.numbers)
    
    # Return the average as the result
    return {
        "input": stock_data.numbers,
        "result": average,
        "count": len(stock_data.numbers),
        "success": True # success flag
    }

# API endpoint for calculating the overall statistics of the stock prices
@app.post("/statistics")
async def calculate_statistics(stock_data: PricesInput):
    
    # Validate input data
    if not stock_data.prices:
        raise HTTPException(status_code=400, detail="Input data is empty")
    
    # Calculate statistics like average, min, max, count, and SD 
    prices = stock_data.prices
    average = sum(prices) / len(prices)
    min_price = min(prices)
    max_price = max(prices)
    
    # Calculate variance and SD
    variance_price = sum((x - average) ** 2 for x in prices) / len(prices)
    sd_price = variance_price ** 0.5
    
    return {
        "average": average,
        "min": min_price,
        "max": max_price,
        "stdDev": sd_price,
        "count": len(prices),
        "success": True # success flag
    }

