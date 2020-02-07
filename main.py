import requests
import pprint


headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
           'cookie':'CMSPreferredCulture=en-US; CMSCsrfCookie=KFLFcJDRdnykLMQLQy8fRE4oSO0B0vHG1GFGhglq; ASP.NET_SessionId=ip2wnpwvrkgfxroalgin30qz; CMSCurrentTheme=Blank_1; _ga=GA1.2.1019347103.1581084835; _gid=GA1.2.2038245465.1581084835; _gcl_au=1.1.2102565660.1581084835; _fbp=fb.1.1581084836060.1362877307; cookiescriptaccept=visit; _gat_gtag_UA_3975226_4=1; __atuvc=1%7C6; __atuvs=5e3d756afd6703ba000',
           'sec-fetch-site': 'same-origin',
           'sec-fetch-mode': 'cors',
           'referer': 'https://www.ces.tech/Show-Floor/Exhibitor-Directory.aspx',
           'ctaapi-version': '1.1'}


html = requests.get('https://www.ces.tech/api/Exhibitors?searchTerm=&sortBy=alpha&filter=&pageNo=1&pageSize=30',
                    headers=headers).text
# print(html)

