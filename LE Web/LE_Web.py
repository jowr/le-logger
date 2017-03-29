
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


    the_name = "Ventilation i faelleskoekkenet 2017"   
    ca = se.query(Campaign).filter(Campaign.name == the_name).one_or_none()
    if ca is None:
        ca = Campaign()
        ca.name = the_name
        se.add(ca)
    ca.desc = "Temperatur- og fugtmaalinger, tilfoejet {0}.".format(np.datetime64(datetime.datetime.now()))
    se.commit()
    
    the_name = "Opvaskerum, reference"
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


    the_name = 'Koekken, reference'
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

    
    the_name = "Opvaskerum, uden udsugning"
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


    the_name = "Koekken, uden udsugning"
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
    from jinja2 import Template

    from sqlalchemy.orm import sessionmaker
    
    from database import Campaign, DataSet, create_models_engine, get_campaign_and_data
    from plotting import alldata, operating_hours, statistics
    from renderer import render

    engine = create_models_engine(s.PGDB_URI)
    Session = sessionmaker(bind=engine)
    se = Session()

    ca, ds_s = get_campaign_and_data(se, "Ventilation i faelleskoekkenet 2017")

    js_resources, css_resources, plot_script, plot_divs = alldata(ds_s)

    page_title = ca.name
    page_header = ca.name
    page_text = "Desc"

    html = render(page_title, page_header, page_text, js_resources, css_resources, plot_script, plot_divs)

    filename = 'altdata.html'
    with io.open(os.path.join(s.STAT_PATH,filename), mode='w', encoding='utf-8') as f:
        f.write(html)


    js_resources, css_resources, plot_script, plot_divs = operating_hours(ds_s)

    page_title = ca.name
    page_header = ca.name
    page_text = "Desc"

    html = render(page_title, page_header, page_text, js_resources, css_resources, plot_script, plot_divs)

    filename = 'driftstimer.html'
    with io.open(os.path.join(s.STAT_PATH,filename), mode='w', encoding='utf-8') as f:
        f.write(html)


    js_resources, css_resources, plot_script, plot_divs = statistics(ds_s)

    page_title = ca.name
    page_header = ca.name
    page_text = "Desc"

    html = render(page_title, page_header, page_text, js_resources, css_resources, plot_script, plot_divs)

    filename = 'statistik.html'
    with io.open(os.path.join(s.STAT_PATH,filename), mode='w', encoding='utf-8') as f:
        f.write(html)

    js_resources = ""
    css_resources = ""
    plot_script = ""
    plot_divs = {"Startside":""}
    page_title = ca.name
    page_header = ca.name
    page_text = "Brug menuen oeverst for at komme videre til graferne."

    html = render(page_title, page_header, page_text, js_resources, css_resources, plot_script, plot_divs)

    filename = 'start.html'
    with io.open(os.path.join(s.STAT_PATH,filename), mode='w', encoding='utf-8') as f:
        f.write(html)

    sys.exit(0)