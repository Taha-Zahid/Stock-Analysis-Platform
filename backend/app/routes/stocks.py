from fastapi import APIRouter, HTTPException
import yfinance as yf
from pydantic import BaseModel # defines a base response model
from typing import Optional    # used if field is none

router = APIRouter()

@router.get("/price/{symbol}")
def get_stock_price(symbol: str):
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="1d")

    if data.empty:
        return {"error": "Invalid ticker symbol"}

    price = data["Close"].iloc[-1]

    return {
        "symbol": symbol.upper(),
        "price": float(price)
    }

# Adding in a company details endpoint
class CompanyInfo(BaseModel):
    symbol: str
    shortName: Optional[str] = None
    longName: Optional[str] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    longBusinessSummary: Optional[str] = None
    marketCap: Optional[float] = None
    exchange: Optional[str] = None
    currency: Optional[str] = None

@router.get("/info/{symbol}", response_model=CompanyInfo)
def get_company_info(symbol: str):
    ticker = yf.Ticker(symbol)
    info = ticker.info #returns a dict of the companies data

    if not info or ("shortName" not in info and "longName" not in info):
        raise HTTPException(status_code=404, detail = "Company info was not found")
    
    # Building response using keys:

    result = {
        "symbol": symbol.upper(),
        "shortName": info.get("shortName"),
        "longName": info.get("longName"),
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "longBusinessSummary": info.get("longBusinessSummary"),
        "marketCap": info.get("marketCap"),
        "exchange": info.get("exchange"),
        "currency": info.get("currency")       
    }
    return result
