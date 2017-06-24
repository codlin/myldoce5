import urllib2
import cookielib
import re

# head: dict of header
def makeMyOpener(head = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
	'Connection':'close',
	'Referer':'http://dict.eudic.net/'
}):
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    header = []
    for key, value in head.items():
        elem = (key, value)
        header.append(elem)
    opener.addheaders = header
    return opener

#Write List to file
def writeListToFile(FileHandle, List):
    for item in List:
        #item.toString()
        FileHandle.write(item.toString())

#--------------------#Youdao-----------------------------------------
YdUrl = "http://dict.youdao.com/search?le=eng&q="
YdPhonetic = re.compile(r'>.*?\[(.{1,25}?)\]</span>', re.DOTALL)
#--------------------#Youdao-----------------------------------------
Oper = makeMyOpener()
def build_phonetic(word):
    phonetic = ""
    url = YdUrl + word
    print(url)
    pipe = Oper.open(url, timeout = 1000)
    data = pipe.read()
    YdHtml = data.decode("utf-8")
    match = YdPhonetic.search(YdHtml)
    if match:
        phonetic = match.group(1)
        print(phonetic)
    return (match, phonetic)