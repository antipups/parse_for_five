import os
import random
import time
import requests
import re
import openpyxl
import threading
import parse_proxy


headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
           'ctaapi-version': '1.1'}
wb = openpyxl.load_workbook(filename='books.xlsx')  # октрываем excel для работы
sheet = wb['Лист1']
proxy = parse_proxy.parse_proxy()   # берем рабочие прокси (чтоб не забанил сайт)
user_agents = open('user_agents.txt', 'r').read()
user_agents = user_agents.split('\n')


def start_download(page, row):
    # headers['user-agent'] = user_agents[random.randint(0, len(user_agents) - 1)]
    mark = 0
    while True:
        temp_proxy = proxy[random.randint(0, len(proxy) - 1)]
        try:
            html = requests.get(
                'https://www.ces.tech/api/Exhibitors?searchTerm=&sortBy=alpha&filter=&pageNo=' + str(page) + '&pageSize=30',
                headers=headers,
                # proxies={'https': temp_proxy}
            )
            print('sex')
            break
        except OSError:
            print('Прокси сосать', temp_proxy)
            if mark == 0:
                mark = 1
            else:
                with open('test.txt', 'w') as f:
                    f.write('Ряд' + str(row) + 'Страница' + str(page))
                os.system("shutdown -s -t 60")
            temp_proxy = proxy[random.randint(0, len(proxy) - 1)]
            continue
    # print(html.text)
    html = html.text[html.text.find('"exhibitors":') + 13:]
    while html.find('{"companyName"') > -1:
        html = html[html.find('{"companyName"'):]
        # print(html)
        current_company = html[:html.find(',{"companyName":"')]  # теперь current company - эта вся рассматриваемая компания\

        name_company = re.search(r'{\"companyName\":.*"alpha"', current_company).group()[16:-9]

        html = html[15:]
        # print(name_company)

        description_company = re.search(r'\"description\":[^:]*', current_company).group()[15:-15]
        description_company = re.sub(r'\\\w', '', description_company)

        companyLink = re.search(r'\"companyLink\":.*\",\"isCategorySponsor\":', current_company).group()[15:-22]
        # companyLink = 'https://ces20.mapyourshow.com/8_0/exhibitor/exhibitor-details.cfm?ExhID=T0012439'
        about_company = requests.get(companyLink)  # html страница компании (для того чтоб парсить больше инфы)
        if about_company.status_code != 200:
            html = html[html.find('{"companyName"'):]
            print('Ошибка')
            continue

        about_company = about_company.text

        address = about_company[
                  about_company.find('<div class="dtc  pa0  pl2">') + 27: about_company.find('<p class="mb0">')]
        address = re.sub(r'(\s{2,}|<.*>)', '', address)
        address += ' ' + re.search(r'<span class="break-word  lh-list">.*</span>', about_company).group()[34:-7]
        phone = booth = url = ''

        if about_company.find('<span class="break-word  lh-list  muted  pr2">(p):</span>') > -1:
            phone = about_company[about_company.find('<span class="break-word  lh-list  muted  pr2">(p):</span>') + 56:]
            phone = re.search(r'>.*<', phone).group()[1:-1]

        if about_company.find('<p class="lh-copy  ma0">') > -1:
            url = about_company[about_company.find('<p class="lh-copy  ma0">') + 24:]
            url = re.search(r'href=\".*\"', url[:url.find('</a')]).group()[6:-1]

        if about_company.find('class="mys-floorPlanLink" style="">') > -1:
            booth = about_company[about_company.find('class="mys-floorPlanLink" style="">') + 35:]
            booth = booth[:booth.find('</a>')]

        contacts = tuple()
        if about_company.find('Company Contacts') > -1:
            contacts = about_company[about_company.find('Company Contacts') + 35:]
            contacts = contacts[:contacts.find('</section>')]
            contacts = re.findall(r'<li>.*<\/li>', contacts, flags=re.DOTALL)
            contacts = ''.join(map(lambda x: re.sub(r'\s*(</?li>|<.{0,2}br.{0,2}>)\s*', ' ', x), contacts))[1:-1].split('  ')
            contacts = tuple(map(lambda x: (x[:x.rfind(' ')], x[x.rfind(' '):]), contacts))
            all_contacts = list()
            for persona in contacts:
                for i in persona:
                    all_contacts.append(i)
            contacts = tuple(all_contacts)
        # print(row, name_company, description_company, address)
        # print(phone, url, booth, contacts)

        for i in enumerate((name_company, description_company, address, phone, url, booth) + contacts):
            sheet.cell(row, i[0] + 1, i[1])
        wb.save('books.xlsx')
        row += 1


if __name__ == '__main__':
    page = 1  # страница по счёту которую мы парсим
    row = 2  # какая по счёту запись
    while page < 151:
        # threading.Thread(target=start_download, args=(page, row, )).start()
        start_download(page, row)
        # time.sleep(3)
        # if page % 20 == 0:
        #     time.sleep(5)
        row += 31
        page += 1
