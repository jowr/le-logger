
def embed_multiple_responsive():
    import io
    import random

    from jinja2 import Template

    from bokeh.embed import components
    from bokeh.plotting import figure
    from bokeh.resources import INLINE
    from bokeh.util.browser import view

    ########## BUILD FIGURES ################

    PLOT_OPTIONS = dict(plot_width=800, plot_height=300)
    SCATTER_OPTIONS = dict(size=12, alpha=0.5)

    data = lambda: [random.choice([i for i in range(100)]) for r in range(10)]

    red = figure(responsive=True, tools='pan', **PLOT_OPTIONS)
    red.scatter(data(), data(), color="red", **SCATTER_OPTIONS)

    blue = figure(responsive=False, tools='pan', **PLOT_OPTIONS)
    blue.scatter(data(), data(), color="blue", **SCATTER_OPTIONS)

    green = figure(responsive=True, tools='pan', **PLOT_OPTIONS)
    green.scatter(data(), data(), color="green", **SCATTER_OPTIONS)

    ########## RENDER PLOTS ################

    # Define our html template for out plots
    template = Template('''<!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="utf-8">
            <title>Responsive plots</title>
            {{ js_resources }}
            {{ css_resources }}
        </head>
        <body>
        <h2>Resize the window to see some plots resizing</h2>
        <h3>Red - pan tool, responsive</h3>
        {{ plot_div.red }}
        <h3>Green - pan tool, responsive (maintains new aspect ratio)</h3>
        {{ plot_div.green }}
        <h3>Blue - pan tool, not responsive</h3>
        {{ plot_div.blue }}
        {{ plot_script }}
        </body>
    </html>
    ''')

    resources = INLINE

    js_resources = resources.render_js()
    css_resources = resources.render_css()

    script, div = components({'red': red, 'blue': blue, 'green': green})

    html = template.render(js_resources=js_resources,
                           css_resources=css_resources,
                           plot_script=script,
                           plot_div=div)

    filename = 'embed_multiple_responsive.html'

    #with io.open(filename, mode='w', encoding='utf-8') as f:
    #    f.write(html)
    #
    #view(filename)
    return html

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