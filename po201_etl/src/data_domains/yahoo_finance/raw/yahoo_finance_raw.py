from utils import dump_data_pgsql,
import yfinance as yf


DATABASE = "raw"


for i, stock in enumerate(stocks, 1):
    print(f"Parsing data for stock: {stock}")
    print(f"Stock {i} out of {len(stocks)} stocks")
    df = yf.download(stock, period="max")["Adj Close"].reset_index()
    df.loc[:, "yf_stock_name"] = stock
    dump_data_pgsql(df=df, database="raw", yf_stock_name=stock)
