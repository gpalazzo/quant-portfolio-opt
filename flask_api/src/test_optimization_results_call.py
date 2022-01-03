import requests


url = "http://localhost:5000/optimization_results"
tickers = {"uuid": "740e263e-f07c-445c-b722-f5cb663740a8"}

post_response = requests.post(url, json=tickers)

print(f"Response Code: {post_response.status_code}")
print(f"Response Text:\n{post_response.text}")
