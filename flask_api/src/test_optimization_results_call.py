import requests
import sys


host = str(sys.argv[1])
if host == "remote":
    url = "http://18.230.21.6:5000/optimization_results"
else:
    url = "http://localhost:5000/optimization_results"

tickers = {"uuid": "2a12eb9f-96bf-4e25-b133-e71b031f49a4"}

post_response = requests.post(url, json=tickers)

print(f"Response Code: {post_response.status_code}")
print(f"Response Text:\n{post_response.text}")
