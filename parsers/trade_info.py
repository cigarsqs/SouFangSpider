# coding=utf-8

import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils.dateutils import get_date_from_str
import settings
from BasicSpider import BasicSpider
from model.LandInfo import LandInfo
from model.TradeInfo import TradeInfo
from utils.cookiesutils import get_cookies

reload(sys)
sys.setdefaultencoding('utf-8')


def get_trade_info(soup, trade_info):
    table_list = soup.find_all('table', class_='tablebox02 mt10')
    # there are two table: first one is about land info and second one is about trade info
    td_list = table_list[1].find_all('td')
    for i in range(0, len(td_list)):
        print td_list[i].text.split('：')[0]
        print td_list[i].text.split('：')[1]
        table_title = td_list[i].text.split('：')[0]
        table_value = td_list[i].text.split('：')[1]
        if table_title == '交易状况':
            trade_info.trade_status = table_value
        elif table_title == '竞得方':
            trade_info.trade_winner = table_value
        elif table_title == '起始日期':
            trade_info.trade_start_date = get_date_from_str(table_value)
        elif table_title == '截止日期':
            trade_info.trade_due_date = get_date_from_str(table_value)
        elif table_title == '成交日期':
            trade_info.trade_deal_date = get_date_from_str(table_value)
        elif table_title == '交易地点':
            trade_info.trade_place = table_value
        elif table_title == '起始价':
            trade_info.trade_starting_price = table_value
        elif table_title == '成交价':
            trade_info.trade_strike_price = table_value
        elif table_title == '楼面地价':
            trade_info.land_price = table_value
        elif table_title == '溢价率':
            trade_info.premium_rate = table_value
        elif table_title == '土地公告':
            trade_info.land_announcement = table_value
        elif table_title == '咨询电话':
            trade_info.consulting_telephone = table_value
        elif table_title == '保证金':
            trade_info.security_deposit = table_value
        elif table_title == '最小加价幅度':
            trade_info.minimum_markup = table_value


def save_trade_info(land_url):
    # 初始化数据库连接:
    engine = create_engine('mysql+pymysql://root:passwd@localhost:3306/test', encoding='utf-8')
    Session = sessionmaker(bind=engine)  # 相当于 cursor
    session = Session()
    new_trade_info = TradeInfo(land_url)
    session.add(new_trade_info)
    session.commit()
    session.close()


# check trade info is in the database or not
def is_exist(land_url, session):
    return session.query(TradeInfo).filter(TradeInfo.land_url == land_url).one_or_none()


# check need cookies or not
def check_need_cookies_or_not(soup):
    bg = soup.find('div', class_='alphabg')
    if bg is None:
        return False
    else:
        return True


def get_trade_info_by_url(land_url):
    url = settings.host_url + land_url
    spider = BasicSpider(url, 0)
    base_soup = spider.get_html_beautiful_soup_without_cookies(land_url)
    if check_need_cookies_or_not(base_soup):
        base_soup = spider.get_html_beautiful_soup_with_cookies(land_url, cookies=get_cookies(settings.cookies))
    trade_info = TradeInfo(land_url)
    get_trade_info(base_soup, trade_info)
    return trade_info


# update trade info
def update_trade_info_by_land_info():
    # 初始化数据库连接:
    engine = create_engine('mysql+pymysql://root:passwd@localhost:3306/test?charset=utf8', encoding='utf-8')
    Session = sessionmaker(bind=engine)  # 相当于 cursor
    session = Session()
    land_info_list = session.query(LandInfo)
    if land_info_list is not None:
        for land in land_info_list:
            print land.land_url
            if is_exist(land.land_url, session) is None:
                trade_info = get_trade_info_by_url(land.land_url)
                session.add(trade_info)
        session.commit()
        session.close()



