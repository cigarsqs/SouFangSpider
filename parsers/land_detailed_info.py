# coding=utf-8

import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import settings
from BasicSpider import BasicSpider
from model.LandInfo import LandInfo

reload(sys)
sys.setdefaultencoding('utf-8')


def get_detailed_land_info(soup, land_info):

    land_number_soup = soup.find('div', class_='menubox01 mt20')
    if land_number_soup is not None:
        land_number = land_number_soup.find('span', class_='gray2').string.split('：')[1]
    else:
        land_number = ''
    # print dikuai_bianhao.string.split('：')[1]
    print land_number
    land_info.land_number = land_number
    table_list = soup.find_all('table', class_='tablebox02 mt10')
    # there are two table: first one is about land info and second one is about trade info
    td_list = table_list[0].find_all('td')
    for i in range(0, len(td_list)):
        print td_list[i].text.split('：')[0]
        table_title = td_list[i].text.split('：')[0]
        table_value = td_list[i].text.split('：')[1]
        if table_title == '地区':
            land_info.land_province = table_value
        elif table_title == '所在地':
            land_info.land_city = table_value
        elif table_title == '总面积':
            land_info.land_total_area = table_value
        elif table_title == '建设用地面积':
            land_info.land_construction_area = table_value
        elif table_title == '规划建筑面积':
            land_info.land_planned_area = table_value
        elif table_title == '代征面积':
            land_info.land_confiscated_area = table_value
        elif table_title == '容积率':
            print td_list[i].text.split('：')[1]
            land_info.land_plot_ratio = table_value
        elif table_title == '绿化率':
            land_info.land_greening_rate = table_value
        elif table_title == '商业比例':
            land_info.commercial_scale = table_value
        elif table_title == '建筑密度':
            land_info.land_building_density = table_value
        elif table_title == '限制高度':
            print td_list[i].text.split('：')[1]
            land_info.land_limited_height = table_value
        elif table_title == '出让形式':
            land_info.land_transfer_form = table_value
        elif table_title == '出让年限':
            land_info.land_transfer_period = table_value
        elif table_title == '位置':
            land_info.land_position = table_value
        elif table_title == '四至':
            land_info.land_four_to = table_value
        elif table_title == '规划用途':
            land_info.land_planning_use = table_value


def get_land_info_by_url(land_url, session):
    for land in session.query(LandInfo).filter(LandInfo.land_url == land_url):
        print land.land_url
        url = settings.host_url + land_url
        spider = BasicSpider(url, 0)
        base_soup = spider.get_html_beautiful_soup_without_cookies(land_url)
        get_detailed_land_info(base_soup, land)
    session.commit()


# update land detailed info
def update_land_detailed_info():
    # 初始化数据库连接:
    engine = create_engine('mysql+pymysql://root:passwd@localhost:3306/test?charset=utf8', encoding='utf-8')
    Session = sessionmaker(bind=engine)  # 相当于 cursor
    session = Session()
    land_info_list = session.query(LandInfo)
    if land_info_list is not None:
        for land in land_info_list:
            get_land_info_by_url(land.land_url, session)




