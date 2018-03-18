import requests
from bs4 import BeautifulSoup
import time
import pymongo
import re
import datetime
from multiprocessing import Pool

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
    # http://bj.ganji.com/ershoubijibendiannao/o3/
    # http://zhuanzhuan.ganji.com/detail/971726746263273997z.shtml
    # o for personal a for merchant
    web_data = requests.get(url,headers=headers)
    soup = BeautifulSoup(web_data.text,'lxml')
    if(soup.find('ul','pageLink')):
        links = []
        for link in soup.select('td.t a.t'):
            item_link = link.get('href').split('?')[0]
            if 'zhuanzhuan' in item_link:
                pass
            else:
                links.append(item_link)
                url_list.insert_one({'url': item_link})
        print(links)

    else:
        pass
def get_pageInfo(link):
    try:
        if 'http' not in link:
            link = 'http:' + link
        web_data = requests.get(link,headers=headers)
        if(web_data.status_code !=404):
            try:
                soup = BeautifulSoup(web_data.text,'lxml')

                area_row = soup.select('ul > li:nth-of-type(3) > a:nth-of-type(2)')[0]
                p = re.compile(r'<[^>]+>', re.S)
                area = p.sub('', str(area_row))

                '''
                #wrapper > div.content.clearfix > div.leftBox > div:nth-child(2) > div > ul > li:nth-child(2) > a:nth-child(2)
                #wrapper > div.content.clearfix > div.leftBox > div:nth-child(2) > div > ul > li:nth-child(2) > a:nth-child(3)
                正则表达式中，“.”的作用是匹配除“\n”以外的任何字符，也就是说，它是在一行中进行匹配。这里的“行”是以“\n”进行区分的。a字符串有每行的末尾有一个“\n”，不过它不可见。
                如果不使用re.S参数，则只在每一行内进行匹配，如果一行没有，就换下一行重新开始，不会跨行。而使用re.S参数以后，正则表达式会将这个字符串作为一个整体，将“\n”当做一个普通的字符加入到这个字符串中，在整体中进行匹配。
                '''

                price = soup.select('.f22.fc-orange.f-type')[0].text.strip()
                row_time = soup.select('.pr-5')[0].text.strip().split(' ')[0][:6]
                if '时' not in row_time:
                    d2 = datetime.datetime.now()
                    pub_time = '2018-' + row_time[0] + row_time[1] + '-' + row_time[3] + row_time[4]
                    d1 = datetime.datetime.strptime(pub_time, '%Y-%m-%d')
                    last_time = d2 - d1
                    s = int(last_time.days)
                    if (s < 0):
                        s += 365
                else:
                    s = 'Unknow'
                info = {
                    'title':soup.title.text,
                    'area' :area,
                    'price':price,
                    'pub_date': row_time,
                    'cates1': link.split('/')[3],
                    'cate2': list(map(lambda x: x.text, soup.select('ul > li:nth-of-type(2) > a'))),
                    'url': link,
                    'last_time':s
                }
                '''
                    'cates': list(soup.select('ul.det-infor > li:nth-of-type(1) > span')[0].stripped_strings),
                    #wrapper > div.content.clearfix > div.leftBox > div:nth-child(2) > div > ul > li:nth-child(4) > span.fc-orange
                    
                '''
                item_info.insert_one(info)
                print(info)
            except AttributeError:
                print('fuck1')
            except IndexError:
                print('fuck2')
        else:
            print('fuck3')
    except:
        print('fuck4')

'''
get_pageInfo('http://bj.ganji.com/xuniwupin/2933252314x.htm')
'''

db_urls = [item['url'] for item in url_list.find()]
index_urls = [item['url'] for item in item_info.find()]
x = set(db_urls)
y = set(index_urls)
rest_of_urls = x - y
rest_of_urls = list(rest_of_urls)

'''
print(rest_of_urls)
'''

if __name__ == '__main__':
    pool = Pool()
    # pool = Pool(processes=6)
    pool.map(get_pageInfo, rest_of_urls)

    pool.close()
    pool.join()

