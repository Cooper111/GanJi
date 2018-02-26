import requests
from bs4 import BeautifulSoup
import time
import pymongo
import re
'''
爬取第一页
'''
client = pymongo.MongoClient('localhost', 27017)
ganji = client['ganji']
url_list = ganji['url_list01']
item_info = ganji['item_info01']

headers={
    'Cookie':'citydomain=bj; ganji_xuuid=a76e460c-1577-4785-f7b0-fa61a830d5e1.1519558604238; ganji_uuid=7272416452539795966246; GANJISESSID=je7gpenjpcspd66ktaofkbp335; als=0; __utmt=1; ganji_login_act=1519560298002; _gl_tracker=%7B%22ca_source%22%3A%22-%22%2C%22ca_name%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_id%22%3A%22-%22%2C%22ca_s%22%3A%22self%22%2C%22ca_n%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22sid%22%3A70604308662%7D; __utma=32156897.649842909.1519558604.1519558604.1519558604.1; __utmb=32156897.4.10.1519558604; __utmc=32156897; __utmz=32156897.1519558604.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); xxzl_deviceid=JmgelkWfcHDiCVE6gvwOBmKDvJ3XT6ij39q2ZJfmI%2FP0PWi1BO3roskTNymY9cTi; 58uuid=61731e9a-52d4-47a2-a7ea-b48d13abdc0e; new_session=0; init_refer=; new_uv=1',
    'Referer':'http://bj.ganji.com/yingyouyunfu/',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'
}
def get_links(url,pages=1,who_sells='o'):
    url ='{}{}{}/'.format(url,str(who_sells),str(pages))

    web_data = requests.get(url,headers=headers)
    soup = BeautifulSoup(web_data.text,'lxml')
    if(soup.find('ul','pageLink')):
        links = []
        for link in soup.select('td.t a.t'):
            item_link = link.get('href').split('?')[0]
            links.append(item_link)
            url_list.insert_one({'url':item_link})
        print(links)
        for url in links:
            get_pageInfo(url)
    else:
        pass
def get_pageInfo(link):
    if 'http' in link:
        web_data = requests.get(link,headers=headers)
        if(web_data.status_code !=404):
            try:
                soup = BeautifulSoup(web_data.text,'lxml')
                area_row = soup.select('ul > li:nth-of-type(2) > a:nth-of-type(2)')[0]
                p = re.compile(r'<[^>]+>',re.S)
                area = p.sub('',str(area_row))
                price = soup.select('.f22.fc-orange.f-type')[0].text.strip()

                info = {
                    'title':soup.title.text,
                    'area':area,
                    'price':price
                }
                item_info.insert_one(info)
                print(info)
            except AttributeError:
                pass
            except IndexError:
                pass
        else:
            pass
    else:
        print('fuck')


