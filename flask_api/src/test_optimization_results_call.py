import requests
import sys


host = str(sys.argv[1])
if host == "remote":
    url = "http://18.230.21.6:5000/optimization_results"
else:
    url = "http://localhost:5000/optimization_results"

tickers = {"uuid": "6c5f8f19-ebb0-4662-882b-ac3fd883e50b"}
# tickers = {
#     "uuid": "6c5f8f19-ebb0-4662-882b-ac3fd883e50b, 3cd05bac-5bc8-4870-89f7-7730f4f69d60"
# }

post_response = requests.post(url, json=tickers)

print(f"Response Code: {post_response.status_code}")
print(f"Response Text:\n{post_response.text}")
