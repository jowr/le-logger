from sqlalchemy import Column, Float, Integer, String, DateTime, ForeignKey
from sqlalchemy import create_engine, and_, func
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, reconstructor

import datetime, random
import numpy as np
import pandas as pd

def DUMMY_DATA_RND(max_value, points):
    rng = range(int(max_value))
    return [random.choice(rng) for r in range(int(points))]

def DUMMY_DATA_SRT(max_value, points):
    return sorted(DUMMY_DATA_RND(max_value, points))

Base = declarative_base()

class Campaign(Base):
    __tablename__ = 'campaigns'
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    desc = Column(String(1000))


class DataSet(Base):
    __tablename__ = 'datasets'
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    time_series = Column(postgresql.ARRAY(DateTime))
    temp_series = Column(postgresql.ARRAY(Float))
    humi_series = Column(postgresql.ARRAY(Float))

    campaign_id = Column(Integer, ForeignKey('campaigns.id'))
#    campaign = relationship("Campaign")#, back_populates="datasets")

    @reconstructor
    def init_on_load(self):
        self.time_series = np.asanyarray(self.time_series)
        self.temp_series = np.asanyarray(self.temp_series)
        self.humi_series = np.asanyarray(self.humi_series)
    
    def as_data_frame(self):
        data_frame = pd.DataFrame(columns=['timestamp', 'temperature', 'humidity'])
        data_frame['timestamp'] = self.time_series
        data_frame['temperature'] = self.temp_series
        data_frame['humidity'] = self.humi_series

        #data_frame['weekday'] = data_frame['datetime'].dt.dayofweek
        #data_frame['time'] = data_frame['datetime'].dt.time
        #data_frame['hour'] = data_frame.time.dt.hour
        #hours_filter = (data_frame.time.dt.hour >= 15) & (data_frame.time.dt.hour <= 21)

        return data_frame

    def set_dummy_data(self, max_value=100, points=10):
        self.id = 0
        self.name = "Dummy name {0}".format(DUMMY_DATA_RND(1e5, 1)[0])
        self.time_series = np.asanyarray(DUMMY_DATA_SRT(max_value, points))
        self.temp_series = np.asanyarray(DUMMY_DATA_SRT(max_value, points))
        self.humi_series = np.asanyarray(DUMMY_DATA_SRT(max_value, points))

#Campaign.datasets = relationship("DataSet", order_by=DataSet.id, back_populates="campaign")

def create_models_engine(PGDB_URI, echo=False):
    engine = create_engine(PGDB_URI, connect_args={'sslmode':'require'}, echo=echo)
    Base.metadata.create_all(engine)
    return engine

#DBSession = sessionmaker(bind=engine)
#session = DBSession()
#testcases = [{"numbers": [25, 33, 42, 55], "name": "David"}, {"numbers": [11, 33, 7, 19 ], "name":     "Salazar"}, {"numbers": [32, 6, 20, 23 ], "name": "Belinda"}, {"numbers": [19, 20, 27, 8 ], "name": "Casey"},     {"numbers": [25, 31, 10, 40 ], "name": "Kathie"}, {"numbers": [25, 20, 40, 39 ], "name": "Dianne"},     {"numbers": [1, 20, 18, 38 ], "name": "Cortez"} ]
#for t in testcases:
#    session.add(TestUser(name=t['name'], numbers=t['numbers']))
#session.commit()

def get_campaign_and_data(session, campaign_name):
    ca = session.query(Campaign).filter(Campaign.name == campaign_name).one()
    ds_s = session.query(DataSet).filter(DataSet.campaign_id == ca.id).all()
    return ca, ds_s