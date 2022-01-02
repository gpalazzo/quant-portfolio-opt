import requests
import sys


host = str(sys.argv[1])
if host == "remote":
    url = "http://18.230.21.6:5000/optimization_results"
else:
    url = "http://localhost:5000/optimization_results"

tickers = {"uuid": "f9a47a4c-50e9-4606-9c8e-f17cc6477b6e"}

post_response = requests.post(url, json=tickers)

print(f"Response Code: {post_response.status_code}")
print(f"Response Text:\n{post_response.text}")
