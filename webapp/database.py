from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class DataSeries(Base):
    __tablename__ = 'testseries'
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    time_series = Column(postgresql.ARRAY(Float))
    temp_series = Column(postgresql.ARRAY(Float))
    humi_series = Column(postgresql.ARRAY(Float))


def create_models_engine(PGDB_URI):
    engine = create_engine(PGDB_URI, connect_args={'sslmode':'require'})
    Base.metadata.create_all(engine)
    return engine

#DBSession = sessionmaker(bind=engine)
#session = DBSession()
#testcases = [{"numbers": [25, 33, 42, 55], "name": "David"}, {"numbers": [11, 33, 7, 19 ], "name":     "Salazar"}, {"numbers": [32, 6, 20, 23 ], "name": "Belinda"}, {"numbers": [19, 20, 27, 8 ], "name": "Casey"},     {"numbers": [25, 31, 10, 40 ], "name": "Kathie"}, {"numbers": [25, 20, 40, 39 ], "name": "Dianne"},     {"numbers": [1, 20, 18, 38 ], "name": "Cortez"} ]
#for t in testcases:
#    session.add(TestUser(name=t['name'], numbers=t['numbers']))
#session.commit()

