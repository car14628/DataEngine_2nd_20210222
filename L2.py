import requests
from bs4 import BeautifulSoup
import pandas as pd

url_base = 'http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-0-0-0-0-0-1.shtml'
total = int(input('输入需要翻页的次数:'))
pages = []

for i in range(total):
    url = url_base[:-7] + str(i+1) + '.shtml'
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    html = requests.get(url, headers=headers, timeout=100)
    content = html.text
    soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
    temp = soup.find('div', class_="tslb_b")
    tr_list = temp.find_all('tr')
    tr_list_th = tr_list[0]
    th_list = tr_list_th.find_all('th')
    head = [];
    for th in th_list:
        value = th.contents[0]
        head = head + [value]
    tr_list_td = tr_list[1:]
    content = []
    for tr in tr_list_td:
        td_list = tr.find_all('td')
        record = []
        for i in range(len(td_list)):
            td = td_list[i]
            value = td.contents[0]
            if i in [4]:
                value = value.contents[0]
            if i in [7]:
                value = value['title']
            record = record + [value]
        content = content + [record]
    pages = pages + content

df = pd.DataFrame(data=pages, columns=head)
df.to_excel('car_spider.xlsx')