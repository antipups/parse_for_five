import requests
import re


headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
           'ctaapi-version': '1.1'}


html = requests.get('https://www.ces.tech/api/Exhibitors?searchTerm=&sortBy=alpha&filter=&pageNo=1&pageSize=30',
                    headers=headers).text
html = html[html.find('"exhibitors":') + 13:]


while True:

    current_company = html[:html.find(',{"companyName"')]   # теперь current company - эта вся рассматриваемая компания
    print(current_company)
    name_company = re.search(r'\"companyName\":[^:]*', current_company).group()[15:-9]
    description_company = re.search(r'\"description\":[^:]*', current_company).group()[15:-15]
    companyLink = re.search(r'\"companyLink\":.*\",\"isCategorySponsor\":', current_company).group()[15:-22]
    about_company = requests.get(companyLink).text  # html страница компании (для того чтоб парсить больше инфы)
    address = about_company[about_company.find('<div class="dtc  pa0  pl2">') + 27: about_company.find('<p class="mb0">')]
    address = ''.join(tuple(x if not x.isspace() else '' for x in re.sub(r'(/?<br.*/>)', '', address)))
    address += ' ' + re.search(r'<span class="break-word  lh-list">.*</span>', about_company).group()[34:-7]
    phone = about_company[about_company.find('<span class="break-word  lh-list  muted  pr2">(p):</span>') + 56:]
    phone = re.search(r'>.*<', phone).group()[1:-1]
    url = about_company[about_company.find('<p class="lh-copy  ma0">') + 24:]
    url = re.search(r'href=\".*\"', url[:url.find('</a')]).group()[6:-1]
    
    break
    if html.find('{"companyName"') > -1:
        html = html[html.find('{"companyName"') + 1:]
    else:
        break

