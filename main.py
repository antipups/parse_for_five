import requests


# функция резалка, string - какую строку режем, afterstring - с какого мента режем
cut = lambda string, afterstring: string[string.find(afterstring) + len(afterstring) + 2:]




headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
           'ctaapi-version': '1.1'}


html = requests.get('https://www.ces.tech/api/Exhibitors?searchTerm=&sortBy=alpha&filter=&pageNo=1&pageSize=30',
                    headers=headers).text
html = html[html.find('"exhibitors":') + 13:]


while True:

    current_company = html[:html.find(',{"companyName"')]   # теперь current company - эта вся рассматриваемая компания
    print(current_company)
    name_company = current_company[current_company.find('"companyName":"') + 15:current_company.find('","')]
    current_company = cut(current_company, name_company)
    # print(current_company)
    # description_company =
    break

    if html.find('{"companyName"') > -1:
        html = html[html.find('{"companyName"') + 1:]
    else:
        break

