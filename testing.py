import requests

url = 'https://ppp-7mmz6amu7-megan-fungs-projects.vercel.app'
files = {'file': open('Medium Excel Sample.xlsx', 'rb')}
data = {'pg': None}

response = requests.post(url, files=files, data=data)
print(response.json)
