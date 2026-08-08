from fastapi import APIRouter
import yfinance as yf

router = APIRouter()

@router.get("/stocks")
def get_stocks():
    symbols = ['^GSPC', '^IXIC', '^NSEI', '^BSESN', 'BTC-USD']
    try:
        # Fetch data for multiple symbols
        tickers = yf.Tickers(' '.join(symbols))
        results = []
        for symbol in symbols:
            info = tickers.tickers[symbol].info
            # yfinance info can sometimes be empty, fallback to fast_info or history if needed
            # but usually info contains currentPrice and previousClose
            current_price = info.get('currentPrice') or info.get('regularMarketPrice')
            prev_close = info.get('previousClose') or info.get('regularMarketPreviousClose')
            
            if not current_price:
                # If info dict is empty, fetch history for last 2 days
                hist = tickers.tickers[symbol].history(period="2d")
                if len(hist) > 0:
                    current_price = hist['Close'].iloc[-1]
                    if len(hist) > 1:
                        prev_close = hist['Close'].iloc[-2]
                    else:
                        prev_close = current_price
            
            if current_price and prev_close:
                change_percent = ((current_price - prev_close) / prev_close) * 100
                results.append({
                    "symbol": symbol,
                    "regularMarketPrice": round(current_price, 2),
                    "regularMarketChangePercent": round(change_percent, 2)
                })
        
        return results
    except Exception as e:
        print(f"Error fetching stocks from yfinance: {e}")
        return []
