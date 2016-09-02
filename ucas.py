import gzip
import re
import http.cookiejar
import urllib.request
import urllib.parse
 
def ungzip(data):
    try:        # 尝试解压
        print('正在解压.....')
        data = gzip.decompress(data)
        print('解压完毕!')
    except:
        print('未经压缩, 无需解压')
    return data
 
 
def getOpener(head):
    # deal with the Cookies
    cj = http.cookiejar.CookieJar()
    pro = urllib.request.HTTPCookieProcessor(cj)
    opener = urllib.request.build_opener(pro)
    header = []
    for key, value in head.items():
        elem = (key, value)
        header.append(elem)
    opener.addheaders = header
    return opener
 
header = {
    'Proxy-Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
}
 
url = 'http://sep.ucas.ac.cn/slogin'
opener = getOpener(header)
'''
op = opener.open(url)
data = op.read()
data = ungzip(data)     # 解压
data = data.decode('utf-8')
'''
#print(data)

id = ''
password = ''

postDict = {
        'userName': id,
        'pwd': password,
        'sb': 'sb'
}
postData = urllib.parse.urlencode(postDict).encode()
op = opener.open(url, postData)
url = "http://sep.ucas.ac.cn/portal/site/226"
op = opener.open(url)
data = op.read()
data = ungzip(data).decode('utf-8')

linkre = re.compile("href=\'(.+?)\'")
for x in linkre.findall(data):
    url = x
print(url)
op = opener.open(url)
url = "http://jwxk.ucas.ac.cn/courseManage/main"
op = opener.open(url)
data = ungzip(op.read()).decode('utf-8')

linkre = re.compile('action=\"(.+?)\"')
for x in linkre.findall(data):
    url = x
url = "http://jwxk.ucas.ac.cn" + url.replace("select","save")
course = ["125752"]
degree = [1]
for i in range(len(course)):
    postDict.clear()
    postDict["sids"] = course[i]
    if degree[i]==1:
        postDict["did_"+course[i]] = course[i]
    op = opener.open(url,urllib.parse.urlencode(postDict).encode())
#print(ungzip(op.read()).decode('utf-8'))
print("done")
