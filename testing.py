import requests

url = 'http://127.0.0.1:5000/run_python'
files = {'file': open('Medium Excel Sample.xlsx', 'rb')}
data = {'pg': None}

response = requests.post(url, files=files, data=data)
print('Response status code:', response.status_code)
print('Response text:', response.text)

try:
    json_response = response.json()
    print("JSON Response:", json_response)
except requests.exceptions.JSONDecodeError:
    print("Failed to decode JSON response")
