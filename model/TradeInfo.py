# coding=utf-8

import datetime
from sqlalchemy import Column, Date, Float, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Base import Base


class TradeInfo(Base):

    """
        Trade Info
    """

    __tablename__ = 'SFS_trade_info'

    id = Column(Integer, primary_key=True)

    land_url = Column(String)
    # 交易状况
    trade_status = Column(String)
    # 竞得方
    trade_winner = Column(String)
    # 起始日期
    trade_start_date = Column(Date)
    # 截止日期
    trade_due_date = Column(Date)
    # 成交日期
    trade_deal_date = Column(Date)
    # 交易地点
    trade_place = Column(String)
    # 起始价
    trade_starting_price = Column(String)
    # 成交价
    trade_strike_price = Column(String)
    # 楼面地价
    land_price = Column(String)
    # 溢价率
    premium_rate = Column(String)
    # 土地公告
    land_announcement = Column(String)
    # 咨询电话
    consulting_telephone = Column(String)
    # 保证金
    security_deposit = Column(String)
    # 最小加价幅度
    minimum_markup = Column(String)
    # last modified date
    last_modified_date = Column(Date)

    def __init__(self, land_url):
        self.last_modified_date = datetime.datetime.now()
        self.land_url = land_url

