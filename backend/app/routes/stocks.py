from fastapi import APIRouter
import yfinance as yf

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
