import requests


url = "http://localhost:5000/optimization_results"
tickers = {"uuid": "bd54469a-9a25-4a31-a4f0-ca3f4c906899"}

post_response = requests.post(url, json=tickers)

print(f"Response Code: {post_response.status_code}")
print(f"Response Text:\n{post_response.text}")
