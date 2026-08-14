import requests

url = "https://api.carbonintensity.org.uk/intensity/"
url2 = "https://api.carbonintensity.org.uk/intensity/factors"
response = requests.get(url)
response2 = requests.get(url2)

print(response.status_code)
print(response.json())
print(response2.status_code)
print(response2.json())
print(response2.url)