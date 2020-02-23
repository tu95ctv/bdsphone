# -*- coding: utf-8 -*-
from time import sleep
import sys
VERSION_INFO   = sys.version_info[0]
try:
    import urllib.request as url_lib
except:
    import urllib2 as url_lib


def request_html(url):
    headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36' }
    count_fail = 0
    while 1:
        try:
            if VERSION_INFO == 3:
                req = url_lib.Request(url, None, headers)
                rp= url_lib.urlopen(req)
                mybytes = rp.read()
                html = mybytes.decode("utf8")
            elif VERSION_INFO ==2:
                req = url_lib.Request(url, None, headers)
                html = url_lib.urlopen(req).read()
            return html
        except Exception as e:
            count_fail +=1
            sleep(5)
            if count_fail ==5:
                raise ValueError(u'Lỗi get html')
            
            
def request_and_write_to_disk():
    url = 'https://muaban.net/nha-hem-ngo-ho-chi-minh-l59-c3202'
    my_html = request_html(url)
    file = open('C:\D4\html\html.html','w')
    file.write(my_html)
    file.close()
    
if __name__== '__main__':
    request_and_write_to_disk()
    print 'ok'