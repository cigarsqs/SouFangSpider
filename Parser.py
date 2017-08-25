# coding=utf-8
import settings
from BasicSpider import BasicSpider
from parsers import land_detailed_info
from parsers import trade_info


class Parser:

    def __init__(self, url, spliter, step=0):
        self.spliter = spliter
        self.step = step
        self.url = url

    def check_parser_step(self):
        if self.step == 1:
            return 0

    def deal_url(self):
        url_list = self.url.split(self.spliter)
        if url_list is not None and len(url_list) >= 0:
            if len(url_list) == 2: # the input
                return 0
        else:
            print u'the format of url is wrong!'
            return -1

    def get_all_province_url(self):
        spider = BasicSpider(self.url, self.step)
        base_soup = spider.get_html_beautiful_soup_without_cookies(self.url)
        #span =base_soup.find('span', class_='w866 fr')
        spider.get_province_url_list(base_soup)

    def get_city_url_by_province_url(self, province_url):
        url = settings.host_url + province_url
        spider = BasicSpider(url, self.step)
        base_soup = spider.get_html_beautiful_soup_without_cookies(province_url)
        spider.get_city_url_list(base_soup, province_url)

    def get_district_url_by_city_url(self, city_url):
        url = settings.host_url + city_url
        spider = BasicSpider(url, self.step)
        base_soup = spider.get_html_beautiful_soup_without_cookies(city_url)
        spider.get_district_url_list(base_soup, city_url)

    #get land info list
    def get_land_info_url_list_by_district_url(self, district_url):
        url = settings.host_url + district_url
        spider = BasicSpider(url, self.step)
        base_soup = spider.get_html_beautiful_soup_without_cookies(district_url)
        land_info_url_list = spider.get_land_url_list_by_distrct_url(base_soup, district_url)
        district_info = spider.search_region_info_by_url(district_url)
        if land_info_url_list is not None:
            for land_info_page_url in land_info_url_list:
                """
                    self.get_basic_info_by_land_info_url_lsit(land_info_url, district_info[0])
                """
                print len(land_info_page_url)
                print district_info[0]
                self.get_basic_info_by_land_info_page_url_list(land_info_page_url, district_info[0])



    # get land basic info
    def get_basic_info_by_land_info_page_url_list(self, land_info_page_url, district_row_id=-1):
        url = settings.host_url + land_info_page_url
        spider = BasicSpider(url, self.step)
        base_soup = spider.get_html_beautiful_soup_without_cookies(land_info_page_url)
        land_info_url_list = spider.get_land_basic_info_by_land_info_url(base_soup, district_row_id)

    def get_detailed_info_by_land_info_url(self, land_info_url):
        url = settings.host_url + land_info_url
        spider = BasicSpider(url, self.step)
        base_soup = spider.get_html_beautiful_soup_without_cookies(land_info_url)
        # spider.get_tudi_detailed_info(base_soup)
        #land_detailed_info.get_detailed_land_info(base_soup, land_info_url)
        land_detailed_info.update_land_detailed_info()

    def get_trade_info_by_land_url(self):
        trade_info.update_trade_info_by_land_info()


parser = Parser(u'/market/________1_0_1.html', u'________', 0)
# parser.get_city_url_by_province_url(u'/market/320000________1_0_1.html')
# parser.get_district_url_by_city_url(u'/market/320600________1_0_1.html')

# parser.get_land_info_url_list_by_district_url(u'/market/320600_320602_______1_0_1.html')
# parser.get_all_province_url()
# parser.get_detailed_info_by_land_info_url(u'/market/9611a8e3-ba59-45af-902a-701810d6bf5c.html')
parser.get_trade_info_by_land_url()
