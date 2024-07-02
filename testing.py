import requests

url = 'https://ppp-ahowny142-megan-fungs-projects.vercel.app/run_python'
files = {'file': open('Medium Excel Sample.xlsx', 'rb')}
data = {'pg': None}
headers = {'x-vercel-protection-bypass': 'UmZ9Iux92fppn1pOAwuMTKFglDmA0PC2'}

response = requests.post(url, files=files, data=data, headers=headers)
print('Response status code:', response.status_code)
print('Response text:', response.text)

try:
    json_response = response.json()
    print("JSON Response:", json_response)
except requests.exceptions.JSONDecodeError:
    print("Failed to decode JSON response")
