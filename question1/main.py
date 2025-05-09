
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import datetime

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
    prices: List[float]
#using asynchronous function to handle requests concurrently
# API endpoint for average calculation of the stock prices
@app.post("/average_stock_prices")
async def calculate_average(stock_data: StockInput):
    
    # Validate input data
    if not stock_data.prices or len(stock_data.prices) == 10000:
        # check if the input data is empty or has 10000 elements
        raise HTTPException(status_code=400, detail="Input data is empty")
    for price in stock_data.prices:
        if price < 0:
            raise HTTPException(status_code=400, detail="Negative price found in input data")
        
    
    # Calculate average of the input stock prices
    sum_of_numbers = sum(stock_data.prices)
    average = sum_of_numbers / len(stock_data.prices)
    
    # Return the average as the result
    return {
        "input": stock_data.prices,
        "result": average,
        "count": len(stock_data.prices),
        "timestamp": datetime.now(),
        "success": True # success flag
    }

# API endpoint for calculating the overall statistics of the stock prices
@app.post("/statistics_stock_prices")
async def calculate_statistics(stock_data: StockInput):
    
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
        "timestamp": datetime.now(),
        "success": True # success flag
    }

