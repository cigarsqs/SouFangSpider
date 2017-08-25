# coding=utf-8

import datetime
from sqlalchemy import Column, Date, Float, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Base import Base


class LandInfo(Base):

    """
        Land Basic Info
    """
    __tablename__ = 'SFS_land_info'

    id = Column(Integer, primary_key=True)

    land_url = Column(String)
    # 地区
    land_province = Column(String)
    # 所在地
    land_city = Column(String)
    # 建设用地面积
    land_construction_area = Column(String)
    # 总面积
    land_total_area = Column(String)
    # 规划建筑面积
    land_planned_area = Column(String)
    # 出让形式
    land_transfer_form = Column(String)
    # 出让年限
    land_transfer_period = Column(String)
    # 位置
    land_position = Column(String)
    # 四至
    land_four_to = Column(String)
    # 规划用途
    land_planning_use = Column(String)
    # parent row id
    parent_row_id = Column(String)
    # 代征面积
    land_confiscated_area = Column(String)
    # 容积率
    land_plot_ratio = Column(String)
    # 绿化率
    land_greening_rate = Column(String)
    # 商业比例
    commercial_scale = Column(String)
    # 建筑密度
    land_building_density = Column(String)
    # 限制高度
    land_limited_height = Column(String)
    # 地块编号
    land_number = Column(String)
    # 更新时间
    last_modified_date = Column(Date)

    def __init__(self, land_url, parent_row_id):
        self.last_modified_date = datetime.datetime.now()
        self.land_url = land_url
        self.parent_row_id = parent_row_id

    def save_land_info(self):
        # 初始化数据库连接:
        engine = create_engine('mysql+pymysql://root:passwd@localhost:3306/test')
        Session = sessionmaker(bind=engine)  # 相当于 cursor
        session = Session()
        new_land_info = LandInfo(self.land_url, self.parent_row_id)
        session.add(new_land_info)
        session.commit()
        session.close()

    # check land info is in the database or not
    def is_exist(self):
        # 初始化数据库连接:
        engine = create_engine('mysql+pymysql://root:passwd@localhost:3306/test')
        Session = sessionmaker(bind=engine)  # 相当于 cursor
        session = Session()
        return session.query(LandInfo).filter(LandInfo.land_url == self.land_url).one_or_none()










