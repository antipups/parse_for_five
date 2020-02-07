import requests
import pprint


headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
           'ctaapi-version': '1.1'}


html = requests.get('https://www.ces.tech/api/Exhibitors?searchTerm=&sortBy=alpha&filter=&pageNo=1&pageSize=30',
                    headers=headers)
print(html)

