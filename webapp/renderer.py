
from jinja2 import Template

HEADER_LINKS = '<b>Navigation:</b> <a href="start.html">start</a> | <a href="altdata.html">alt data</a> | <a href="driftstimer.html">driftstimer</a> | <a href="statistik.html">statistik</a>'

def render(page_title, page_header, page_text, js_resources, css_resources, plot_script, plot_divs):

    template = Template('''<!DOCTYPE html>
        <html lang="en">
            <head>
                <meta charset="utf-8">
                <title>{{ page_title }}</title>
                {{ js_resources }}
                {{ css_resources }}
            </head>
            <body>
            {{ header_links }}
            <h2>{{ page_header }}</h2>

            {% for key, value in plot_divs.iteritems() %}
                <h3>{{ key }}</h3>
                {{ value }}
            {% endfor %}

            {{ page_text }}

            {{ plot_script }}
            </body>
        </html>
        ''')

    html = template.render(
        page_title=page_title,
        header_links=HEADER_LINKS,
        page_header=page_header,
        page_text=page_text,
        js_resources=js_resources,
        css_resources=css_resources,
        plot_script=plot_script,
        plot_divs=plot_divs)

    return html