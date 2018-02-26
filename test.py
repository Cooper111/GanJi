import re

fuck = '<a href="/rirongbaihuo/" target="_blank">海淀</a>'

you = re.compile(r'<[^>]+>',re.S)
mother = you.sub('',fuck)
print(mother)

url = 'fuck'
url = url + 'o'+'/'
print(url)

for i in range(10):
    print(i)