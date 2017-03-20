from __future__ import print_function, division

import os, sys

if 'DYNO' in os.environ:
    HEROKU = True
else:
    HEROKU = False

BASE_PATH = os.path.realpath(os.path.dirname(__file__))

# The main app
import flask 
from flask import Flask
app = Flask(__name__, template_folder=os.path.join(BASE_PATH,'templates'))

# All the views
@app.route('/')
def hello():
    return 'Hello World with Flask and JJ!'

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
    args = {} #flask.request.args

    # Get all the form arguments in the url with defaults
    color = getitem(args, 'color', 'Black')
    _from = int(getitem(args, '_from', 0))
    to = int(getitem(args, 'to', 10))

    # Create a polynomial line graph with those arguments
    x = list(range(_from, to + 1))
    fig = figure(title="Polynomial")
    fig.line(x, [i ** 2 for i in x], color=colors[color], line_width=2)

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


# ... add the main method for Heroku at the end
if HEROKU:
    if __name__ == '__main__':
        # Bind to PORT if defined, otherwise default to 5000.
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port)
