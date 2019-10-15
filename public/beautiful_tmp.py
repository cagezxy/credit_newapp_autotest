# coding=utf8
import csv

import requests
from bs4 import BeautifulSoup
import chardet

url = "https://hz.lianjia.com/ershoufang/103104154772.html"
my_header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}
h = requests.get(url, headers=my_header)
soup = BeautifulSoup(h.text)

file = open('house_info.csv','w', newline="")
csv_write = csv.writer(file)
csv_write.writerow([" 挂牌时间 "])
dics = {"挂牌时间": "无"}
base_info = soup.find("div", class_="transaction")
tmp = base_info.find_all("li")
for something in tmp:
    tmp_key = something.find("span", class_="label").string
    key = tmp_key.replace('\n', '').strip()
    tmp_val = something.find("span", class_="label").next_sibling.next_sibling.string
    val = tmp_val.replace('\n', '').strip()
    print(type(key), type(val))
    print(key, val)
    dics[key] = val
print(type(dics["挂牌时间"]), dics["挂牌时间"])
datas=[dics["挂牌时间"]]
csv_write.writerow(datas)
file.close()