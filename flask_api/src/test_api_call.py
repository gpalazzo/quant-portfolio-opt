import requests

url = "http://18.230.21.6:5000/portfolio_opt"
tickers = {"tickers": "bbdc4, abev3"}

post_response = requests.post(url, json=tickers)

print(f"Response Code: {post_response.status_code}")
print(f"Response Text:\n{post_response.text}")
