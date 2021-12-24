import requests
import sys


host = str(sys.argv[1])
if host == "remote":
    url = "http://18.230.21.6:5000/portfolio_optimize"
else:
    url = "http://localhost:5000/portfolio_optimize"

tickers = {"tickers": "AMER3.SA, ANIM3.SA, APER3.SA"}

post_response = requests.post(url, json=tickers)

print(f"Response Code: {post_response.status_code}")
print(f"Response Text:\n{post_response.text}")
