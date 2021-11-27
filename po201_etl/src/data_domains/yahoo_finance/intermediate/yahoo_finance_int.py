from utils import parse_stocks_index, dump_data_pgsql
import yfinance as yf


DATABASE = "intm"
stocks = parse_stocks_index()


for i, stock in enumerate(stocks, 1):
    print(f"Parsing data for stock: {stock}")
    print(f"Stock {i} out of {len(stocks)} stocks")
    df = yf.download(stock, period="max")["Adj Close"].reset_index()
    df.loc[:, "yf_stock_name"] = stock
    dump_data_pgsql(df=df, database="raw", yf_stock_name=stock)
