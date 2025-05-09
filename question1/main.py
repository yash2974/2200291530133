from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import datetime
from collections import defaultdict

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
class StockPrice(BaseModel): 
    symbol: str
    price: float
    timestamp: datetime
    
class StockInput(BaseModel):
    data: List[StockPrice]
#using asynchronous function to handle requests concurrently
# API endpoint for average calculation of the stock prices
@app.post("/average_stock_prices")
async def calculate_average(stock_data: StockInput):
    
    # Validate input data
    if not stock_data.data:
        # check if the input data is empty 
        raise HTTPException(status_code=400, detail="Input data is empty")
    
    prices = []

    for price_stock in stock_data.data:
        if price_stock.price < 0:
            raise HTTPException(status_code=400, detail="Negative price found in input data")
        prices.append(price_stock.price)
        
        
    
    # Calculate average of the input stock prices
    sum_of_numbers = sum(prices)
    average = sum_of_numbers / len(prices)
    
    # Return the average as the result
    return {
        "input": prices,
        "result": average,
        "count": len(prices),
        "timestamp": datetime.now(),
        "success": True # success flag
    }

# API endpoint for calculating the overall statistics of the stock prices
@app.post("/statistics_stock_prices")
async def calculate_statistics(stock_data: StockInput):
    
    # Validate input data
    if not stock_data.data:
        raise HTTPException(status_code=400, detail="Input data is empty")
    
    prices = [entry.price for entry in stock_data.data]

    # Calculate statistics like average, min, max, count, and SD 
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
        "std": sd_price,
        "count": len(prices),
        "timestamp": datetime.now(),
        "success": True # success flag
    }

# API endpoint for calculating the average stock prices by symbol
@app.post("/average_by_symbol")
async def average_by_symbol(stock_data: StockInput):

    symbol_prices = defaultdict(list)
    # Validate input data
    for entry in stock_data.data:
        if entry.price < 0:
            raise HTTPException(status_code=400, detail="Negative price found")
        symbol_prices[entry.symbol].append(entry.price)

    result = {}
    # Calculate average for each symbol
    for symbol, prices in symbol_prices.items():
        result[symbol] = {
            "average": sum(prices) / len(prices),
            "count": len(prices)
        }

    return {
        "result": result,
        "timestamp": datetime.now(),
        "success": True
    }

# Various functionalities of the stock aggregation API like  Time-Based Aggregation (e.g., Daily Average can be handled by using multiple endpoints

