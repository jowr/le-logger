from __future__ import print_function, division, absolute_import

import os, sys
import urlparse

BASE_PATH = os.path.realpath(os.path.dirname(__file__))
if BASE_PATH not in sys.path:
    sys.path = [BASE_PATH] + sys.path

from settings import const as s

# The main app
import flask 
from flask import Flask
app = Flask(__name__, template_folder=s.TEMP_PATH)

# All the views
@app.route('/')
def hello():
    return 'Hello World with Flask and JJ!'

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

@app.route("/dbtest")
def test_database():
    try:
        from sqlalchemy import Column, Integer, String
        from sqlalchemy.dialects import postgresql
        from sqlalchemy.ext.declarative import declarative_base
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker

        Base = declarative_base()

        class TestUser(Base):
            __tablename__ = 'testuser'
            id = Column(Integer, primary_key=True)
            name = Column(String(250))
            numbers = Column(postgresql.ARRAY(Integer))

        engine = create_engine(s.PGDB_URI, connect_args={'sslmode':'require'})

        Base.metadata.create_all(engine)

        #DBSession = sessionmaker(bind=engine)
        #session = DBSession()
        #
        ##testcases = [{"numbers": [25, 33, 42, 55], "name": "David"}, {"numbers": [11, 33, 7, 19 ], "name":     "Salazar"}, {"numbers": [32, 6, 20, 23 ], "name": "Belinda"}, {"numbers": [19, 20, 27, 8 ], "name": "Casey"},     {"numbers": [25, 31, 10, 40 ], "name": "Kathie"}, {"numbers": [25, 20, 40, 39 ], "name": "Dianne"},     {"numbers": [1, 20, 18, 38 ], "name": "Cortez"} ]
        ##
        ##for t in testcases:
        ##    session.add(TestUser(name=t['name'], numbers=t['numbers']))
        ##session.commit()
        #return session.info
        return str(engine)
    except Exception as e:
        return str(e)

#
#import werkzeug
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

# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
        return redirect(url_for('uploaded_file',
                                filename=filename))

# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/data/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/uploader')
def uploader():
    return render_template('upload.html')

# ... add the main method for Heroku at the end
if s.HEROKU:
    if __name__ == '__main__':
        # Bind to PORT if defined, otherwise default to 5000.
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port)
