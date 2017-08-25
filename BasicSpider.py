# coding=utf-8
import sys

import requests
from bs4 import BeautifulSoup

import settings
from model.LandInfo import LandInfo
from SQLWrapper import SQLWrapper
reload(sys)
sys.setdefaultencoding('utf-8')


class BasicSpider:
    def __init__(self, url, step):
        self.url = url
        self.cookies = settings.cookies
        self.step = step

    def get_html_beautiful_soup_with_cookies(self, url, cookies):
        url = settings.host_url + url
        try:
            base_session = requests.session()
            base_session.keep_alive = False
            base_res = base_session.get(url, headers=settings.headers, cookies=cookies, allow_redirects=False)
            base_soup = BeautifulSoup(base_res.text, "html.parser")
            return base_soup
        except requests.RequestException, e:
            print e
            print "failed url: " + url

    def get_html_beautiful_soup_without_cookies(self, url):
        url = settings.host_url + url
        try:
            base_session = requests.session()
            base_session.keep_alive = False
            base_res = base_session.get(url, headers=settings.headers, allow_redirects=False)
            base_soup = BeautifulSoup(base_res.text, "html.parser")
            return base_soup
        except requests.RequestException, e:
            print e
            print "failed url: " + self.url

    def get_cookies(self):
        cookies = {}
        for line in self.cookies.split(';'):
            key, value = line.split('=', 1)
            cookies[key] = value
        return cookies

    def parser_url(self, base_soup):
        span = base_soup.find('span', class_='w863 city_list25 fr')
        if span.find('br') is not None:
            url_list = span.find('br').find_next_siblings('a')
        else:
            url_list = span.find_all('a')
        url_list.pop(0)  # delete 不限 url
        for url in url_list:
            print url['href']
            print url.string
        return url_list

    def deal_url(self, url):
        base_soup = self.get_html_beautiful_soup_without_cookies(url)
        url_list = self.parser_url(base_soup)

    def pop_unlimited_url(self, url_list):
        if url_list is not None and len(url_list) is not 0:
            url_list.pop(0)  # delete 不限url
        return url_list

    # 获取所有省的URL,for example: 江苏
    def get_province_url_list(self, soup):
        span = soup.find('span', class_='w866 fr')
        if span is not None:
            url_list = span.find_all('a')
            url_list = self.pop_unlimited_url(url_list)
            #如果地区信息已经存在,则将它从要插入的URL list中删除#
            for i in range(len(url_list)-1, -1, -1):
                print i
                url = url_list[i]
                is_exist = self.check_region_info_exist_or_not_by_url(url['href'])
                if is_exist:
                    print url_list[0].string + " has been exist"
                    url_list.pop(0)
            if url_list is not None and len(url_list) > 0:
                self.insert_region_url_list(url_list)
            self.step = settings.parser_steps['Parser_Privince_Level_URL'] # 成功获取URL
            #print self.step
            return url_list
        else:
            return

    def get_city_url_list(self, soup, url):
        #获取城市的URL
        span = soup.find('span', class_='w863 city_list25 fr')
        if span is not None:
            if span.find('br') is not None:
                url_list = span.find('br').find_previous_siblings('a')
            else:
                url_list = span.find_all('a')
            url_list = self.pop_unlimited_url(url_list)  # delete 不限 url
            url_list = self.validate_url_list_is_exist(url_list) #删除重复的地区信息
            if url_list is not None and len(url_list) > 0:
                region_info = self.search_region_info_by_url(url)
                if region_info is not None:
                    self.insert_region_url_list(url_list, region_info[0])
        return

    def get_district_url_list(self, soup, url):
        #获取地区的URL
        span = soup.find('span', class_='w863 city_list25 fr')
        if span is not None:
            if span.find('br') is not None:
                url_list = span.find('br').find_next_siblings('a')
            else:
                url_list = span.find_all('a')
            url_list = self.pop_unlimited_url(url_list)  # delete 不限 url
            url_list = self.validate_url_list_is_exist(url_list) #删除重复的地区信息
            if url_list is not None and len(url_list) > 0:
                region_info = self.search_region_info_by_url(url)
                if region_info is not None:
                    self.insert_region_url_list(url_list, region_info[0])
        return

    def get_land_url_list_by_distrct_url(self, soup, land_url):
        split = u'_______'
        #获取土地 url list的页数
        land = soup.find('div',class_='top_page fr')
        land_url_list = []
        if land is not None:
            land_num = land.find('span')
        else:
            land_num = None
        if land_num is not None:
            print land_num.string.split('/')[1]
            num = int(land_num.string.split('/')[1])
            deal_url = land_url.split(split)[0]
            print land_url
            deal_split_url = land_url.split(split)[1]
            if num == 34:
                print '34'
                #如果 num == 34, 通过规划用途(例如:住宅用地等)获取相关土地信息
                for i in range(0, 4):
                    tudi_zl_url = deal_url+u"_"+"%d"%(i+1)+u"______"+deal_split_url
                    print tudi_zl_url
                    base_soup = self.get_html_beautiful_soup_without_cookies(tudi_zl_url)

            else:
                for i in range(0,num):
                    tudi_url = deal_url+split+u"1_0_"+"%d"%(i+1)+u".html"
                    print tudi_url
                    land_url_list.append(tudi_url)
        return land_url_list

    def get_land_basic_info_by_land_info_url(self, soup, district_row_id=-1):
        land_info_list = soup.findAll('div', class_='list28_text fl')
        for land_basic_info in land_info_list:
            land_info_detailed_url = land_basic_info.find('h3').a['href']
            date =land_basic_info.find('td', attrs={'width': '100'}).text
            print land_info_detailed_url
            print len(land_info_detailed_url)
            print date
            print district_row_id
            # self.insert_land_url_list(land_info_detailed_url, date, district_row_id)
            land_info = LandInfo(land_info_detailed_url, district_row_id)
            if land_info.is_exist() is None:
                land_info.save_land_info()


    def get_tudi_detailed_info(self, soup,title=u''):

        bianhao = soup.find('div', class_='menubox01 mt20')
        if bianhao is not None:
            dikuai_bianhao = bianhao.find('span', class_='gray2').string.split('：')[1]
        else:
            dikuai_bianhao =''
        #print dikuai_bianhao.string.split('：')[1]
        print dikuai_bianhao
        table_list = soup.find_all('table', class_='tablebox02 mt10')
        td_list = table_list[0].find_all('td')
        for i in range(0, len(td_list)):
            print td_list[i].text.split('：')[1]
        td_list_sec = table_list[1].find_all('td')



    def validate_url_list_is_exist(self,url_list):
        if url_list is not None and len(url_list) > 0:
             # 如果地区信息已经存在,则将它从要插入的URL list中删除
            for i in range(len(url_list)-1,-1,-1):
                print i
                url = url_list[i]
                is_exist = self.check_region_info_exist_or_not_by_url(url['href'])
                if is_exist:
                    print url_list[0].string + " has been exist"
                    url_list.pop(0)
        return url_list

    # 将所获得地区信息插入到表格中
    def insert_region_url_list(self, url_list, parent_row_id=-1):
        sqlWrapper = SQLWrapper()
        conn = sqlWrapper.get_conn()
        command = 'insert into SFS_region_info(region_url,region_name,parent_row_id) values(%s,%s,%s)'
        for url in url_list:
            print url.string
            data = (url['href'], url.string, parent_row_id)
            sqlWrapper.excute_statement(command, data, conn)
        sqlWrapper.conn_commit(conn)
        sqlWrapper.conn_close(conn)
        self.step = settings.parser_steps['Insert_Privince_Level_URL']
        return

    def insert_land_url_list(self, url, date, distric_row_id=-1):
        sqlWrapper = SQLWrapper()
        conn = sqlWrapper.get_conn()
        command = 'insert into SFS_land_basic_info(land_url,land_date,district_row_id) values(%s,%s,%s)'
        data = (url, date, distric_row_id)
        sqlWrapper.excute_statement(command, data, conn)
        sqlWrapper.conn_commit(conn)
        sqlWrapper.conn_close(conn)
        return

    def check_region_info_exist_or_not_by_url(self, url):
        region_info = self.search_region_info_by_url(url)
        if region_info is None:
            return False
        else:
            return True

    # 根据url搜索相应地区信息
    def search_region_info_by_url(self, url):
        sqlWrapper = SQLWrapper()
        conn = sqlWrapper.get_conn()
        command = "select * from SFS_region_info where region_url = '%s'" % url
        if conn is not None:
            print url
            region_info = sqlWrapper.excute_fetch_statument(command, conn)
            sqlWrapper.conn_commit(conn)
            sqlWrapper.conn_close(conn)
            return region_info




#spider = BasicSpider(u'http://land.fang.com/market/________1_0_1.html', 0)
#spider.get_province_url_list(spider.url)