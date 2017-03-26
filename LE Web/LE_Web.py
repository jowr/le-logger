from __future__ import print_function
import io, os, sys

BASE_PATH = os.path.realpath(os.path.join(os.path.dirname(os.path.dirname(__file__)),'webapp'))
if BASE_PATH not in sys.path:
    sys.path = [BASE_PATH] + sys.path

from settings import const as s

if False:
    from excel import ExcelFile
    for fl in [
      os.path.join(s.DATA_PATH,'20170321_LE01.xls'), 
      os.path.join(s.DATA_PATH,'20170321_LE02.xls'), 
      os.path.join(s.DATA_PATH,'20170326_LE01.xls'), 
      os.path.join(s.DATA_PATH,'20170326_LE02.xls')]:
        with io.open(fl,'rb') as file:
            xlFile = ExcelFile(file)
            xlFile.xlLoad()
            print(xlFile.serial)
            print(xlFile.time)

if True:
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.orm import Session as ALQsession
    from sqlalchemy import and_
    from excel import ExcelFile
    from database import Campaign, DataSet, create_models_engine
    import numpy as np
    import datetime

    engine = create_models_engine(s.PGDB_URI, echo=True)
    Session = sessionmaker(bind=engine)
    se = Session()

    #def get_or_create(model, the_name):
    #    instance = se.query(model).filter_by(name=the_name).first()
    #    if instance:
    #        return instance
    #    else:
    #        #instance = model(**kwargs)
    #        instance = model()
    #        instance.name = the_name
    #        session.add(instance)
    #        session.commit()
    #        return instance

    def get_campaign(the_name):
        ca_int = se.query(Campaign).filter(Campaign.name == the_name).one_or_none()
        if ca_int is None:
            ca_int = Campaign()
            ca_int.name = the_name
            se.add(ca_int)
            se.commit()
        return ca_int

    def get_dataset(the_name, start_time):
        dss = se.query(DataSet).filter(DataSet.name == the_name).all()
        for dsss in dss:
            if (np.min(dsss.time_series) - start_time) < datetime.timedelta(seconds=1):
                return dsss
        ds_int = DataSet()
        ds_int.name = the_name
        se.add(ds_int)
        se.commit()
        return ds_int

    ca = get_campaign("Almindelig drift")
    ca.desc = "Added on {0}".format(np.datetime64(datetime.datetime.now()))
    se.commit()
    
    ds = DataSet()
    ds.name = 'Opvaskerummet'
    with io.open(os.path.join(s.DATA_PATH,'20170321_LE01.xls'),'rb') as file:
        xlFile = ExcelFile(file)
        xlFile.xlLoad()
        ds.time_series = xlFile.time_datetime()
        ds.temp_series = xlFile.temperature
        ds.humi_series = xlFile.humidity
        ds.campaign = ca

    ds_db = get_dataset(ds.name, np.min(ds.time_series))
    ds_db.time_series = ds.time_series
    ds_db.temp_series = ds.temp_series
    ds_db.humi_series = ds.humi_series
    ds_db.campaign = ds.campaign
    #se.merge(ds_db)
    se.commit()

    ds = DataSet()
    ds.name = 'Koekkenet'
    with io.open(os.path.join(s.DATA_PATH,'20170321_LE02.xls'),'rb') as file:
        xlFile = ExcelFile(file)
        xlFile.xlLoad()
        ds.time_series = xlFile.time_datetime()
        ds.temp_series = xlFile.temperature
        ds.humi_series = xlFile.humidity
        ds.campaign = ca
    
    ds_db = get_dataset(ds.name, np.min(ds.time_series))
    ds_db.time_series = ds.time_series
    ds_db.temp_series = ds.temp_series
    ds_db.humi_series = ds.humi_series
    ds_db.campaign = ds.campaign
    #se.merge(ds_db)
    se.commit()



    ca = get_campaign("Uden udsugning")
    ca.desc = "Added on {0}".format(np.datetime64(datetime.datetime.now()))
    se.commit()
    
    ds = DataSet()
    ds.name = 'Opvaskerummet'
    with io.open(os.path.join(s.DATA_PATH,'20170326_LE01.xls'),'rb') as file:
        xlFile = ExcelFile(file)
        xlFile.xlLoad()
        ds.time_series = xlFile.time_datetime()
        ds.temp_series = xlFile.temperature
        ds.humi_series = xlFile.humidity
        ds.campaign = ca
     
    ds_db = get_dataset(ds.name, np.min(ds.time_series))
    ds_db.time_series = ds.time_series
    ds_db.temp_series = ds.temp_series
    ds_db.humi_series = ds.humi_series
    ds_db.campaign = ds.campaign
    #se.merge(ds_db)
    se.commit()

    ds = DataSet()
    ds.name = 'Koekkenet'
    with io.open(os.path.join(s.DATA_PATH,'20170326_LE02.xls'),'rb') as file:
        xlFile = ExcelFile(file)
        xlFile.xlLoad()
        ds.time_series = xlFile.time_datetime()
        ds.temp_series = xlFile.temperature
        ds.humi_series = xlFile.humidity
        ds.campaign = ca
        
    ds_db = get_dataset(ds.name, np.min(ds.time_series))
    ds_db.time_series = ds.time_series
    ds_db.temp_series = ds.temp_series
    ds_db.humi_series = ds.humi_series
    ds_db.campaign = ds.campaign
    #se.merge(ds_db)
    se.commit()



