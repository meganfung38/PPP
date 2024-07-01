import requests

url = 'https://ppp-bep6a98dk-megan-fungs-projects.vercel.app'
files = {'file': open(r'C:\Users\megan.fung\Downloads\Medium Excel Sample (1).xlsx', 'rb')}
data = {'pg': None}

response = requests.post(url, files=files, data=data)
print(response.json)
