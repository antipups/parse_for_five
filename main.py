import requests
import re
import openpyxl


def write_to_excel(row, *tuple_of_data):
    wb = openpyxl.load_workbook(filename='book.xlsx')
    sheet = wb['Лист1']
    print(row)
    if row == 0:
        name_of_coloms = ('Название', 'Описание', 'Адрес', 'Номер', 'Ссылка', 'Booth')
        for i in enumerate(name_of_coloms):
            sheet.cell(row, i[0] + 1, i[1])
    row += 1
    for i in enumerate(tuple_of_data):
        sheet.cell(row, i[0] + 1, i[1])
    wb.save("book.xlsx")


headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
           'ctaapi-version': '1.1'}


html = requests.get('https://www.ces.tech/api/Exhibitors?searchTerm=&sortBy=alpha&filter=&pageNo=1&pageSize=30',
                    headers=headers).text
html = html[html.find('"exhibitors":') + 13:]


i = 1
while True:

    while True:
        current_company = html[:html.find(',{"companyName"')]   # теперь current company - эта вся рассматриваемая компания\
        html = html[15:]
        name_company = re.search(r'\"companyName\":[^:]*', current_company).group()[15:-9]
        description_company = re.search(r'\"description\":[^:]*', current_company).group()[15:-15]
        companyLink = re.search(r'\"companyLink\":.*\",\"isCategorySponsor\":', current_company).group()[15:-22]
        about_company = requests.get(companyLink).text  # html страница компании (для того чтоб парсить больше инфы)
        address = about_company[about_company.find('<div class="dtc  pa0  pl2">') + 27: about_company.find('<p class="mb0">')]
        address = ''.join(tuple(x if not x.isspace() else '' for x in re.sub(r'(/?<br.*/>)', '', address)))
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
        # print(booth)
        print(i, name_company, description_company, address, phone, url, booth)
        write_to_excel(i, name_company, description_company, address, phone, url, booth)
        i += 1  # для excel
        if html.find('{"companyName"') > -1:
            html = html[html.find('{"companyName"') + 1:]
        else:
            break


# import openpyxl
# wb = openpyxl.load_workbook(filename='book.xlsx')
# sheet = wb['Лист1']
# sheet.cell(3, 3, 'лох')
# wb.save('book.xlsx')
# # print()