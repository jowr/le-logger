
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

if False:
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.orm import Session as ALQsession
    from sqlalchemy import and_
    from sqlalchemy import func
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
        qry = se.query(DataSet)
        fil = qry.filter(and_(
            DataSet.name == the_name, 
            func.min(DataSet.time_series) == start_time
            ))
        dss = fil.all()
        if len(dss) > 0: 
            return dss[0]
        ds_int = DataSet()
        ds_int.name = the_name
        se.add(ds_int)
        se.commit()
        return ds_int


    the_name = "Almindelig drift"   
    ca = se.query(Campaign).filter(Campaign.name == the_name).one_or_none()
    if ca is None:
        ca = Campaign()
        ca.name = the_name
        se.add(ca)
    ca.desc = "Added on {0}".format(np.datetime64(datetime.datetime.now()))
    se.commit()
    
    the_name = "Opvaskerummet"
    ds = se.query(DataSet).filter(and_(
        DataSet.name == the_name,
        DataSet.campaign_id == ca.id)
        ).one_or_none()
    if ds is None:
        ds = DataSet()
        ds.name = the_name
        ds.campaign_id = ca.id
        se.add(ds)
    se.commit()

    with io.open(os.path.join(s.DATA_PATH,'20170321_LE01.xls'),'rb') as file:
        xlFile = ExcelFile(file)
        xlFile.xlLoad()
    
    ds.time_series = xlFile.time_datetime()
    ds.temp_series = xlFile.temperature
    ds.humi_series = xlFile.humidity
    se.commit()

    the_name = 'Koekkenet'
    ds = se.query(DataSet).filter(and_(
        DataSet.name == the_name,
        DataSet.campaign_id == ca.id)
        ).one_or_none()
    if ds is None:
        ds = DataSet()
        ds.name = the_name
        ds.campaign_id = ca.id
        se.add(ds)
    se.commit()

    with io.open(os.path.join(s.DATA_PATH,'20170321_LE02.xls'),'rb') as file:
        xlFile = ExcelFile(file)
        xlFile.xlLoad()
    ds.time_series = xlFile.time_datetime()
    ds.temp_series = xlFile.temperature
    ds.humi_series = xlFile.humidity
    se.commit()



    the_name = "Uden udsugning"
    ca = se.query(Campaign).filter(Campaign.name == the_name).one_or_none()
    if ca is None:
        ca = Campaign()
        ca.name = the_name
        se.add(ca)
    ca.desc = "Added on {0}".format(np.datetime64(datetime.datetime.now()))
    se.commit()

    
    the_name = "Opvaskerummet"
    ds = se.query(DataSet).filter(and_(
        DataSet.name == the_name,
        DataSet.campaign_id == ca.id)
        ).one_or_none()
    if ds is None:
        ds = DataSet()
        ds.name = the_name
        ds.campaign_id = ca.id
        se.add(ds)
    se.commit()

    with io.open(os.path.join(s.DATA_PATH,'20170326_LE01.xls'),'rb') as file:
        xlFile = ExcelFile(file)
        xlFile.xlLoad()
    
    ds.time_series = xlFile.time_datetime()
    ds.temp_series = xlFile.temperature
    ds.humi_series = xlFile.humidity
    se.commit()


    the_name = 'Koekkenet'
    ds = se.query(DataSet).filter(and_(
        DataSet.name == the_name,
        DataSet.campaign_id == ca.id)
        ).one_or_none()
    if ds is None:
        ds = DataSet()
        ds.name = the_name
        ds.campaign_id = ca.id
        se.add(ds)
    se.commit()

    with io.open(os.path.join(s.DATA_PATH,'20170326_LE02.xls'),'rb') as file:
        xlFile = ExcelFile(file)
        xlFile.xlLoad()
    ds.time_series = xlFile.time_datetime()
    ds.temp_series = xlFile.temperature
    ds.humi_series = xlFile.humidity
    se.commit()

if True:
    import io
    from plotting import embed_multiple_responsive, embed_themed

    from sqlalchemy.orm import sessionmaker
    from database import Campaign, DataSet, create_models_engine

    engine = create_models_engine(s.PGDB_URI)
    Session = sessionmaker(bind=engine)
    se = Session()

    time_series = []
    temp_series = []
    humi_series = []

    ca_s = se.query(Campaign).all()
    for ca in ca_s:
        ds_s = se.query(DataSet).filter(DataSet.campaign_id == ca.id).all()
        for ds in ds_s:
            #fig.line(ds.time_series, ds.temp_series)
            time_series.append(ds.time_series)
            temp_series.append(ds.temp_series)
            humi_series.append(ds.humi_series)

    html = embed_multiple_responsive(time_series=time_series, temp_series=temp_series, humi_series=humi_series)
    filename = 'embed_multiple_responsive.html'
    with io.open(os.path.join(s.STAT_PATH,filename), mode='w', encoding='utf-8') as f:
        f.write(html)

    #html = embed_themed()
    #filename = 'embed_themed.html'
    #with io.open(os.path.join(s.STAT_PATH,filename), mode='w', encoding='utf-8') as f:
    #    f.write(html)

    sys.exit(0)