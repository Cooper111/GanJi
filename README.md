# GanJi
爬取赶集网二手商品资料
<hr>
1.没有(先到ip网抓取ip，再使用代理ip),待改进
<hr>
2.断点续传：
db_urls = [item['url'] for item in url_list.find()]
index_urls = [item['url'] for item in item_info.find()]
x = set(db_urls)
y = set(index_urls)
rest_of_urls = x-y

然后把main的那个函数注释掉，底下POOL的channel_list.split()替换成rest_of_urls.split()
