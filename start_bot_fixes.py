# Fix bug on line 195 of start_bot.py

import os

def log_trade(symbol, side, amount, price, order_id):
    """Log trade details to file"""
    import datetime
    
    # FIX: Change exist_okay to exist_ok
    os.makedirs("data", exist_ok=True)  # CORRECT
    
    with open("data/trade_history.csv", "a") as f:
        if os.path.getsize("data/trade_history.csv") == 0:
            # Write header if file is empty
            f.write("timestamp,symbol,side,amount,price,order_id\n")
            
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{timestamp},{symbol},{side},{amount},{price},{order_id}\n")
