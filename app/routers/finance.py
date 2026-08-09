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
            try:
                # Use fast_info for real-time prices to avoid yfinance info caching
                ticker = yf.Ticker(symbol)
                fast_info = ticker.fast_info
                
                current_price = fast_info.last_price
                prev_close = fast_info.previous_close
                
                if current_price and prev_close:
                    change_percent = ((current_price - prev_close) / prev_close) * 100
                    results.append({
                        "symbol": symbol,
                        "regularMarketPrice": round(current_price, 2),
                        "regularMarketChangePercent": round(change_percent, 2)
                    })
            except Exception as e:
                print(f"Error fetching fast_info for {symbol}: {e}")
                pass
        
        return results
    except Exception as e:
        print(f"Error fetching stocks from yfinance: {e}")
        return []
