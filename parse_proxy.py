import re
import requests


def parse_proxy():
    html = requests.get('https://www.ip-adress.com/proxy-list').text
    urls = list()
    all_urls = re.findall(r'<a href="https:\/\/www\.ip-adress\.com\/ip-address\/.*<\/td>', html)
    for proxy in all_urls:
        urls.append(re.sub(r'</a>', '', re.search(r'">.*</td', proxy).group()[2:-4]))
    return urls


if __name__ == '__main__':
    print(parse_proxy())

