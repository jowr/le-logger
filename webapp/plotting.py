
import random

#FIGURE_OPTIONS = dict(plot_width=1200, plot_height=300, logo="grey")
FIGURE_OPTIONS = dict(logo="grey")
SCATTER_OPTIONS = dict(alpha=0.5)
LINE_OPTIONS = dict(line_width=2, alpha=0.5)
DUMMY_DATA_RND = lambda: [random.choice([i for i in range(100)]) for r in range(10)]
DUMMY_DATA_SRT = lambda: sorted(DUMMY_DATA_RND())

from bokeh.palettes import viridis
numlines = 4 #len(toy_df.columns)
mypalette=viridis(numlines)

#from bokeh.sampledata import download
#download()

from bokeh.sampledata.glucose import data
subset = data.ix['2010-10-06']
#x, y = subset.index.to_series(), subset['glucose']



def embed_multiple(js_resources, css_resources, script, divs):
    from jinja2 import Template    

    ########## RENDER PLOTS ################

    # Define our html template for out plots
    template = Template('''<!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="utf-8">
            <title>Koekken 2017</title>
            {{ js_resources }}
            {{ css_resources }}
        </head>
        <body>
        <h2>Koekken 2017</h2>

        <h3>Alt Data</h3>
        {{ plot_div.all_data }}

        <h3>Dagsdata</h3>
        {{ plot_div.daily_data }}

        {{ plot_script }}
        </body>
    </html>
    ''')

    html = template.render(js_resources=js_resources,
                           css_resources=css_resources,
                           plot_script=script,
                           plot_div=divs)

    #filename = 'embed_multiple_responsive.html'

    #with io.open(filename, mode='w', encoding='utf-8') as f:
    #    f.write(html)
    #
    #view(filename)
    return html


def embed_multiple_responsive(time_series=[], temp_series=[], humi_series=[]):
    import io
    from jinja2 import Template

    from bokeh.embed import components
    from bokeh.plotting import figure
    from bokeh.resources import INLINE
    from bokeh.util.browser import view

    from bokeh.charts import BoxPlot

    from bokeh.layouts import gridplot
    from bokeh.models import DatetimeTickFormatter

    import pandas as pd

    ########## BUILD FIGURES ################

    if len(time_series) < 1:
        time_series = [DUMMY_DATA_SRT(), DUMMY_DATA_SRT(), DUMMY_DATA_SRT(), DUMMY_DATA_SRT()]
    if len(temp_series) < 1:
        temp_series = [DUMMY_DATA_SRT(), DUMMY_DATA_SRT(), DUMMY_DATA_SRT(), DUMMY_DATA_SRT()]
    if len(humi_series) < 1:
        humi_series = [DUMMY_DATA_SRT(), DUMMY_DATA_SRT(), DUMMY_DATA_SRT(), DUMMY_DATA_SRT()]

    series_count = len(time_series)
    colours = viridis(series_count)

    labels = []
    data_frames = []
    data_frames_filtered = []
    for i in range(series_count):
        data_frame = pd.DataFrame(columns=['time', 'temp', 'humi'])
        data_frame['time'] = time_series[i]
        data_frame['temp'] = temp_series[i]
        data_frame['humi'] = humi_series[i]
        data_frames.append(data_frame)
        labels.append(str(i))

        hours_filter = (data_frame.time.dt.hour >= 15) & (data_frame.time.dt.hour <= 21)

        data_frame = pd.DataFrame(columns=['time', 'temp', 'humi', 'hour'])
        data_frame['time'] = time_series[i][hours_filter]
        data_frame['hour'] = data_frame.time.dt.time
        data_frame['hour_int'] = data_frame.time.dt.hour
        data_frame['temp'] = temp_series[i][hours_filter]
        data_frame['humi'] = humi_series[i][hours_filter]
        data_frames_filtered.append(data_frame)

    ########## ALL DATA ################

    all_data_temp = figure(responsive=True, x_axis_label = "Days", x_axis_type = "datetime", y_axis_label = "Temperature / C", y_axis_type = "linear", **FIGURE_OPTIONS)
    #all_data_temp.multi_line(time_series, temp_series, line_color=viridis(len(time_series)), **LINE_OPTIONS)
    for (clr, leg, xda, yda ) in zip(colours, labels, time_series, temp_series):
        #my_plot = all_data_temp.line(xda, yda, color = clr, legend = leg, **LINE_OPTIONS)
        my_plot = all_data_temp.scatter(xda, yda, color = clr, legend = leg, **SCATTER_OPTIONS)

    all_data_humi = figure(x_range=all_data_temp.x_range, responsive=True, x_axis_label = "Days", x_axis_type = "datetime", y_axis_label = "Relative humidity / \%", y_axis_type = "linear", **FIGURE_OPTIONS)
    #all_data_humi.multi_line(time_series, humi_series, line_color=viridis(len(time_series)), **LINE_OPTIONS)
    for (clr, leg, xda, yda ) in zip(colours, labels, time_series, humi_series):
        #my_plot = all_data_humi.line(xda, yda, color = clr, legend = leg, **LINE_OPTIONS)
        my_plot = all_data_humi.scatter(xda, yda, color = clr, legend = leg, **SCATTER_OPTIONS)

    for p in [all_data_temp, all_data_humi]:
        p.xaxis.formatter=DatetimeTickFormatter(formats=dict(
            hours=["%k:%M"],
            days=["%d. %m. %y"],
            months=["%m %Y"],
            years=["%Y"],
        ))

    all_data = gridplot([all_data_temp, all_data_humi], ncols=2, plot_width=500, plot_height=250, sizing_mode='scale_width', 
                        toolbar_options=dict(logo="grey"))
                        #toolbar_options=dict(logo="grey", location='above'), merge_tools=False)

    ########## DAILY DATA ################  

    #daily_data_temp = figure(responsive=True, x_axis_label = "Time / h", x_axis_type = "datetime", y_axis_label = "Temperature / C", y_axis_type = "linear", **FIGURE_OPTIONS)
    ##daily_data_temp.multi_line(hours_series, temp_series, line_color=viridis(len(time_series)), **LINE_OPTIONS)
    #for (clr, leg, frm ) in zip(colours, labels, data_frames_filtered):
    #    #my_plot = daily_data_temp.line(xda, yda, color = clr, legend = leg)
    #    my_plot = daily_data_temp.scatter(frm['hour'], frm['temp'], color = clr, legend = leg, **SCATTER_OPTIONS)

    daily_data_temp = BoxPlot(data_frames_filtered[0], values='temp', label='hour_int', plot_width=400)

    #daily_data_humi = figure(x_range=daily_data_temp.x_range, responsive=True, x_axis_label = "Time / h", x_axis_type = "datetime", y_axis_label = "Relative humidity / \%", y_axis_type = "linear", **FIGURE_OPTIONS)
    ##daily_data_humi.multi_line(hours_series, humi_series, line_color=viridis(len(time_series)), **LINE_OPTIONS)
    #for (clr, leg, frm ) in zip(colours, labels, data_frames_filtered):
    #    #my_plot = daily_data_humi.line(xda, yda, color = clr, legend = leg)
    #    my_plot = daily_data_humi.scatter(frm['hour'], frm['humi'], color = clr, legend = leg, **SCATTER_OPTIONS)

    daily_data_humi = BoxPlot(data_frames_filtered[0], values='humi', label='hour_int', plot_width=400)

    for p in [daily_data_temp, daily_data_humi]:
        p.xaxis.formatter=DatetimeTickFormatter(formats=dict(
            hours=["%k:%M"],
            days=["%d. %m. %y"],
            months=["%m %Y"],
            years=["%Y"],
        ))

    daily_data = gridplot([daily_data_temp, daily_data_humi], ncols=2, plot_width=500, plot_height=250, sizing_mode='scale_width', 
                        toolbar_options=dict(logo="grey"))
                        #toolbar_options=dict(logo="grey", location='above'), merge_tools=False)


    ########## RENDER PLOTS ################

    resources = INLINE
    js_resources = resources.render_js()
    css_resources = resources.render_css()
    script, divs = components({'all_data': all_data, 'daily_data': daily_data})

    return embed_multiple(js_resources, css_resources, script, divs)

def embed_responsive_width_height():
    """ This example shows how a Bokeh plot can be embedded in an HTML
    document, in a way that the plot resizes to make use of the available
    width and height (while keeping the aspect ratio fixed).
    To make this work well, the plot should be placed in a container that
    *has* a certain width and height (i.e. non-scrollable), which is the
    body element in this case. A more realistic example might be embedding
    a plot in a Phosphor widget.
    """
    import random

    from bokeh.io import output_file, show
    from bokeh.plotting import figure

    PLOT_OPTIONS = dict(plot_width=600, plot_height=400)
    SCATTER_OPTIONS = dict(size=12, alpha=0.5)

    data = lambda: [random.choice([i for i in range(100)]) for r in range(10)]

    red = figure(sizing_mode='scale_both', tools='pan', **PLOT_OPTIONS)
    red.scatter(data(), data(), color="red", **SCATTER_OPTIONS)
    return red
    #output_file('embed_responsive_width_height.html')
    #show(red)


def embed_themed():

    import io

    from jinja2 import Template

    from bokeh.embed import components
    from bokeh.resources import INLINE
    from bokeh.util.browser import view
    from bokeh.themes import Theme
    from bokeh.plotting import figure

    x1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    y1 = [0, 8, 2, 4, 6, 9, 5, 6, 25, 28, 4]

    p1 = figure(title='DARK THEMED PLOT')
    p1.scatter(x1, y1)

    theme = Theme(json={
        'attrs': {
            'Figure': {
                'background_fill_color': '#2F2F2F',
                'border_fill_color': '#2F2F2F',
                'outline_line_color': '#444444'
                },
            'Axis': {
                'axis_line_color': "white",
                'axis_label_text_color': "white",
                'major_label_text_color': "white",
                'major_tick_line_color': "white",
                'minor_tick_line_color': "white",
                'minor_tick_line_color': "white"
                },
            'Grid': {
                'grid_line_dash': [6, 4],
                'grid_line_alpha': .3
                },
            'Circle': {
                'fill_color': 'lightblue',
                'size': 10,
                },
            'Title': {
                'text_color': "white"
                }
            }
        })

    script, div = components(p1, theme=theme)

    template = Template('''<!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="utf-8">
            <title>Bokeh Scatter Plots</title>
            {{ js_resources }}
            {{ css_resources }}
            {{ script }}
            <style>
                body {
                    background: #2F2F2F;
                }
                .embed-wrapper {
                    width: 50%;
                    height: 400px;
                    margin: auto;
                }
            </style>
        </head>
        <body>
            <div class="embed-wrapper">
            {{ div }}
            </div>
        </body>
    </html>
    ''')

    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    filename = 'embed_simple.html'

    html = template.render(js_resources=js_resources,
                           css_resources=css_resources,
                           script=script,
                           div=div)

    #with io.open(filename, mode='w', encoding='utf-8') as f:
    #    f.write(html)
    #view(filename)
    return html