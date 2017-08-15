import random
#Some User Agents
hds=[{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
    {'User-Agent':'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},
    {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},
    {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'},
    {'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},
    {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},
    {'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'},
    {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},
    {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'},
    {'User-Agent':'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'},
    {'User-Agent':'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'}]


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': hds[random.randint(0, len(hds)-1)]}


#host url
host_url = u'http://land.fang.com'

#parser step
parser_steps= {
    'Begin_Parser': 0,
    'End_Parser': -1,
    'Parser_Privince_Level_URL': '01',
    'Insert_Privince_Level_URL':'11',
    'Parser_City_Level_URL': '02',
    'Parser_District_Level_URL': '03'

}

#SQL Settings
SQL_INFO = {
    'host':     'localhost',
    'user':     'root',
    'passwd':   'root',
    'db':       'test',
    'port':     3306,
    'charset':  'utf8'
            }


#raw cookies
cookies ='global_cookie=55vzvuu34k60mzdwcl8kpecun1vir8qhz65; bdshare_firstime=1469856394887; city=hz; ASP.NET_SessionId=uzrlg0jsrxwaxv55z4yxn245; Hm_lvt_9e45c915a52098cc2e351c0e70fe1900=1486390342; Hm_lpvt_9e45c915a52098cc2e351c0e70fe1900=1486390342; token=ab7ef33b8db6474e95d159b8493260b0; unique_cookie=U_54w5kwfqw3m8flvrw7ms5jr8q3iiyu6fzyx*2; __utmt_t0=1; __utmt_t1=1; __utma=147393320.1361387444.1469856316.1485321586.1486390430.15; __utmb=147393320.2.10.1486390430; __utmc=147393320; __utmz=147393320.1469856316.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); sfut=ECDAFA06B208F93C80B17B70393D10511921A128D2860307550819E423F9C96C6F38D3F8B7B919934BEEE0F3D7162A5FC1D820FE7E293F0D8404CEC2876FAB04EEC0A7C7AD5A9D0AC319C4B6A5CF46F6614D55069098926E'

