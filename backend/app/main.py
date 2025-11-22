from fastapi import FastAPI
from app.routes import stocks

app = FastAPI(
    title="Stock Analysis Platform API",
    version="1.0.0"
)

app.include_router(stocks.router, prefix="/stocks", tags=["Stocks"])

@app.get("/")
def root():
    return {"message": "Stock Analysis API is running"}
