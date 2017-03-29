from __future__ import print_function, division, absolute_import

import os, sys
import urlparse

BASE_PATH = os.path.realpath(os.path.dirname(__file__))
if BASE_PATH not in sys.path:
    sys.path = [BASE_PATH] + sys.path



from sqlalchemy.orm import sessionmaker    
from database import create_models_engine
from settings import const as s

engine = create_models_engine(s.PGDB_URI)
Session = sessionmaker(bind=engine)
se = Session()

# The main app
import flask 
from flask import Flask
app = Flask(__name__, template_folder=s.TEMP_PATH)

## All the views
#@app.route('/')
#def hello():
#    return 'Hello World with Flask and JJ!'

@app.route('/model')
def model():
    from models import MeasurementCampaign
    meas = MeasurementCampaign('default')
    return repr(meas)

@app.route('/pic')
def pic():
    from bokeh.plotting import figure, output_file, show, save
    from bokeh.resources import CDN
    from bokeh.embed import file_html

    # prepare some data
    x = [0.1, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    y0 = [i**2 for i in x]
    y1 = [10**i for i in x]
    y2 = [10**(i**2) for i in x]

    # output to static HTML file
    #output_file("log_lines.html")

    # create a new plot
    p = figure(
       tools="pan,box_zoom,reset,save",
       y_axis_type="log", y_range=[0.001, 10**11], title="log axis example",
       x_axis_label='sections', y_axis_label='particles'
    )

    # add some renderers
    p.line(x, x, legend="y=x")
    p.circle(x, x, legend="y=x", fill_color="white", size=8)
    p.line(x, y0, legend="y=x^2", line_width=3)
    p.line(x, y1, legend="y=10^x", line_color="red")
    p.circle(x, y1, legend="y=10^x", fill_color="red", line_color="red", size=6)
    p.line(x, y2, legend="y=10^x^2", line_color="orange", line_dash="4 4")

    # show the results
    #show(p)

    return file_html(p, CDN)

@app.route('/plot')
def circel():
    from bokeh.plotting import figure
    from bokeh.resources import CDN
    from bokeh.embed import file_html

    plot = figure()
    plot.circle([1,2], [3,4])

    return file_html(plot, CDN, "my plot")

@app.route("/simple")
def polynomial():
    """ Very simple embedding of a polynomial chart
    """
    from bokeh.embed import components
    from bokeh.plotting import figure
    from bokeh.resources import INLINE
    from bokeh.util.string import encode_utf8

    colors = {
        'Black': '#000000',
        'Red':   '#FF0000',
        'Green': '#00FF00',
        'Blue':  '#0000FF',
    }

    def getitem(obj, item, default):
        if item not in obj:
            return default
        else:
            return obj[item]

    # Grab the inputs arguments from the URL
    args = flask.request.args

    # Get all the form arguments in the url with defaults
    color = getitem(args, 'color', 'Black')
    _from = int(getitem(args, '_from', -10))
    to = int(getitem(args, 'to', 10))

    # Create a polynomial line graph with those arguments
    x = list(range(_from, to + 1))
    fig = figure(title="Polynomial")
    fig.line(x, [i ** 3 for i in x], color=colors[color], line_width=2)

    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    script, div = components(fig)
    
    try:
        html = flask.render_template(
            'embed.html',
            plot_script=script,
            plot_div=div,
            js_resources=js_resources,
            css_resources=css_resources,
            color=color,
            _from=_from,
            to=to
        )
        #return encode_utf8(html)
        return html
    except Exception as e:
        return str(e)

@app.route("/dbtest_simple")
def test_database_simple():
    import os
    import psycopg2
    import urlparse

    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(os.environ["DATABASE_URL"])

    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port, 
        sslmode='require'
    )
    return s.PGDB_URI

import database as db
@app.route("/dbtest")
def test_database():
    from sqlalchemy.orm import sessionmaker
    from database import Campaign, DataSet
    import numpy as np
    try:
        engine = db.create_models_engine(s.PGDB_URI)
        Session = sessionmaker(bind=engine)
        se = Session()

        ca = Campaign()
        ca.name = "Test campaign"
        ca.desc = "A longer description"
        
        ds = DataSet()
        ds.name = 'test name'
        ds.time_series = np.zeros(5)
        ds.temp_series = np.ones(5)
        ds.humi_series = np.empty(5).fill(np.NaN)
        ds.campaign = ca
        
        se.add(ca)
        se.add(ds)
        se.commit()
        return str(ds) + " and " + str(ca)
    except Exception as e:
        return str(e)

@app.route("/dbread")
def read_database():
    from sqlalchemy.orm import sessionmaker
    from database import Campaign, DataSet
    import numpy as np
    try:
        engine = db.create_models_engine(s.PGDB_URI)
        Session = sessionmaker(bind=engine)
        se = Session()

        ret = ""

        ca_s = se.query(Campaign).all()
        for ca in ca_s:
            ds_s = se.query(DataSet).filter(DataSet.campaign_id == ca.id).all()
            ret = ret + "\nCampaign: {0} ({1})\n".format(ca.name, len(ds_s))
            for ds in ds_s:
                ret = ret + "DataSet: {0} ({1}) - {2}\n".format(ds.name, ds.time_series.size, str(ds.time_series))

        return str(ret)
    except Exception as e:
        return str(e)

@app.route("/start.html")
def start_func():
    try:
        from database import Campaign, DataSet, get_campaign_and_data
        from plotting import alldata, operating_hours, statistics
        from renderer import render

        req_pth = os.path.join(s.STAT_PATH, "start.html")
        if os.path.isfile(req_pth):
            return app.send_static_file(req_pth)

        ca, ds_s = get_campaign_and_data(se, "Ventilation i faelleskoekkenet 2017")

        js_resources = ""
        css_resources = ""
        plot_script = ""
        plot_divs = {"Startside":""}
        page_title = ca.name
        page_header = ca.name
        page_text = "Brug menuen oeverst for at komme videre til graferne."

        html = render(page_title, page_header, page_text, js_resources, css_resources, plot_script, plot_divs)

        import io
        with io.open(req_pth, mode='w', encoding='utf-8') as f:
            f.write(html)

        return html+"xx"

    except Exception as e:
        return str(e)

@app.route('/')
def index_func():
    return start_func()

@app.route("/altdata.html")
def altdata_func():
    try:
        from database import Campaign, DataSet, get_campaign_and_data
        from plotting import alldata, operating_hours, statistics
        from renderer import render

        ca, ds_s = get_campaign_and_data(se, "Ventilation i faelleskoekkenet 2017")

        js_resources, css_resources, plot_script, plot_divs = alldata(ds_s)

        page_title = ca.name
        page_header = ca.name
        page_text = "Desc"

        html = render(page_title, page_header, page_text, js_resources, css_resources, plot_script, plot_divs)
        return html

    except Exception as e:
        return str(e)

@app.route("/driftstimer.html")
def driftstimer_func():
    try:
        from database import Campaign, DataSet, get_campaign_and_data
        from plotting import alldata, operating_hours, statistics
        from renderer import render

        ca, ds_s = get_campaign_and_data(se, "Ventilation i faelleskoekkenet 2017")

        js_resources, css_resources, plot_script, plot_divs = operating_hours(ds_s)

        page_title = ca.name
        page_header = ca.name
        page_text = "Desc"

        html = render(page_title, page_header, page_text, js_resources, css_resources, plot_script, plot_divs)
        return html

    except Exception as e:
        return str(e)

@app.route("/statistik.html")
def statistik_func():
    try:
        from database import Campaign, DataSet, get_campaign_and_data
        from plotting import alldata, operating_hours, statistics
        from renderer import render

        ca, ds_s = get_campaign_and_data(se, "Ventilation i faelleskoekkenet 2017")

        js_resources, css_resources, plot_script, plot_divs = statistics(ds_s)

        page_title = ca.name
        page_header = ca.name
        page_text = "Desc"

        html = render(page_title, page_header, page_text, js_resources, css_resources, plot_script, plot_divs)
        return html

    except Exception as e:
        return str(e)


#
import werkzeug
#
#@app.route('/upload')
#def upload_file():
#   return flask.render_template('upload.html')
#
#@app.route('/uploader', methods = ['GET', 'POST'])
#def upload_file():
#   if flask.request.method == 'POST':
#      f = flask.request.files['file']
#      f.save(werkzeug.secure_filename(f.filename))
#      return 'file uploaded successfully'

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = s.DATA_PATH
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['csv', 'xls', 'xlsx'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

from excel import ExcelFile
# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    try:
        # Get the name of the uploaded file
        file = flask.request.files['file']
        # Check if the file is one of the allowed types/extensions
        if file and allowed_file(file.filename):
            ## Make the filename safe, remove unsupported chars
            #filename = werkzeug.secure_filename(file.filename)
            #return filename
            ## Move the file form the temporal folder to
            ## the upload folder we setup
            #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            ## Redirect the user to the uploaded_file route, which
            ## will basicaly show on the browser the uploaded file
            #return flask.redirect(flask.url_for('uploaded_file', filename=filename))
            #return file.read()
            xlFile = ExcelFile()
            return xlFile.xlInfo(file)
    except Exception as e:
        return str(e)    
    return "No luck"

# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/data/<filename>')
def uploaded_file(filename):
    return flask.send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/uploader')
def uploader():
    return flask.render_template('upload.html')

# ... add the main method for Heroku at the end
if s.HEROKU:
    if __name__ == '__main__':
        # Bind to PORT if defined, otherwise default to 5000.
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port)
