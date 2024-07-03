import requests

url = 'https://ppp-hi03zaoki-megan-fungs-projects.vercel.app/run_python'
files = {'file': open('Medium Excel Sample.xlsx', 'rb')}
data = {'pg': None}
headers = {'x-vercel-protection-bypass': '<get from vercel>'}

response = requests.post(url, files=files, data=data, headers=headers)
print('Response status code:', response.status_code)
try:
    json_response = response.json()
    print("JSON Response:", json_response)
except requests.exceptions.JSONDecodeError:
    print("Failed to decode JSON response")
