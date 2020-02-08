import re
import requests


def parse_proxy():
    html = requests.get('https://www.ip-adress.com/proxy-list').text
    html = html[html.find('<table class="htable proxylist">'):]
    urls = list()
    html = html[html.find('<a href="'):]
    while re.search(r'title="More information about.*>.*</a>.*</td>', html) is not None:
        new_url = re.search(r'">.*</a>.*</td>', html).group()[2:-5]
        html = html[5:]
        new_url = new_url[:new_url.find('</a')] + new_url[new_url.rfind(':'):]
        urls.append(new_url)
        html = html[html.find('<a href'):]
    return urls


if __name__ == '__main__':
    print(parse_proxy())
