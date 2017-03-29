
import numpy as np
import pandas as pd

from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.layouts import gridplot
from bokeh.models import DatetimeTickFormatter
from bokeh.charts import BoxPlot

from bokeh.palettes import viridis as palette

from database import DataSet

#FIGURE_OPTIONS = dict(plot_width=1200, plot_height=300, logo="grey")
FIGURE_OPTIONS = dict(logo="grey")
SCATTER_OPTIONS = dict(alpha=0.5)
LINE_OPTIONS = dict(line_width=2, alpha=0.95)

def _get_dummies():
    data_sets = []
    for i in range(4):
        ds = DataSet()
        ds.set_dummy_data()
        data_sets.append(ds)
    return data_sets

def alldata(data_sets=[]):    

    ########## BUILD FIGURES ################

    if len(data_sets) < 1:
        data_sets = _get_dummies()

    series_count = len(data_sets)
    colours = palette(series_count)

    all_data_temp = figure(responsive=True, x_axis_label = "Days", x_axis_type = "datetime", y_axis_label = "Temperature / C", y_axis_type = "linear", **FIGURE_OPTIONS)
    for (clr, ds) in zip(colours, data_sets):
        my_plot = all_data_temp.line(ds.time_series, ds.temp_series, color = clr, legend = ds.name, **LINE_OPTIONS)

    all_data_humi = figure(x_range=all_data_temp.x_range, responsive=True, x_axis_label = "Days", x_axis_type = "datetime", y_axis_label = "Relative humidity / \%", y_axis_type = "linear", **FIGURE_OPTIONS)
    for (clr, ds) in zip(colours, data_sets):
        my_plot = all_data_humi.line(ds.time_series, ds.humi_series, color = clr, legend = ds.name, **LINE_OPTIONS)

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


    ########## RENDER PLOTS ################

    resources = INLINE
    js_resources = resources.render_js()
    css_resources = resources.render_css()
    plot_script, plot_divs = components({'Oversigt over alt data': all_data})

    return js_resources, css_resources, plot_script, plot_divs



def operating_hours(data_sets=[]):

    ########## BUILD FIGURES ################

    if len(data_sets) < 1:
        data_sets = _get_dummies()

    series_count = len(data_sets)
    colours = palette(series_count)

    data_frames = []
    for ds in data_sets:
        df = ds.as_data_frame()
        day_filter = (df['timestamp'].dt.dayofweek == 5) | (df['timestamp'].dt.dayofweek == 6)
        #df = df.drop(df[day_filter].index)
        hour_filter = (df['timestamp'].dt.hour < 15) | (df['timestamp'].dt.hour > 21)
        #df = df.drop(df[hour_filter].index)

        #df = df.drop(df[day_filter | hour_filter].index)

        #df['temperature'][day_filter | hour_filter] = np.NaN
        #df['humidity'][day_filter | hour_filter] = np.NaN

        idx = df.ix[day_filter | hour_filter].index
        #df.temperature[idx] = np.NaN
        #df.humidity[idx] = np.NaN
        df.loc[idx,'temperature'] = np.NaN
        df.loc[idx,'humidity'] = np.NaN
        #df.at[dates[5], 'E'] = 7

        df['time'] = df['timestamp'].dt.time
        data_frames.append(df)

    all_data_temp = figure(responsive=True, x_axis_label = "Time of day", x_axis_type = "datetime", y_axis_label = "Temperature / C", y_axis_type = "linear", **FIGURE_OPTIONS)
    for (clr, ds, df) in zip(colours, data_sets, data_frames):
        #my_plot = all_data_temp.scatter(df.time, df.temperature, color = clr, legend = ds.name, **SCATTER_OPTIONS)
        my_plot = all_data_temp.line(df.time, df.temperature, color = clr, legend = ds.name, **LINE_OPTIONS)

    all_data_humi = figure(x_range=all_data_temp.x_range, responsive=True, x_axis_label = "Time of day", x_axis_type = "datetime", y_axis_label = "Relative humidity / \%", y_axis_type = "linear", **FIGURE_OPTIONS)
    for (clr, ds, df) in zip(colours, data_sets, data_frames):
        my_plot = all_data_humi.scatter(df.time, df.humidity, color = clr, legend = ds.name, **SCATTER_OPTIONS)
        #my_plot = all_data_humi.line(df.time, df.humidity, color = clr, legend = ds.name, **LINE_OPTIONS)

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


    ########## RENDER PLOTS ################

    resources = INLINE
    js_resources = resources.render_js()
    css_resources = resources.render_css()
    plot_script, plot_divs = components({'Data fra kl. 15 - 22, uden loerdag': all_data})

    return js_resources, css_resources, plot_script, plot_divs


def statistics(data_sets=[]):

    ########## BUILD FIGURES ################

    if len(data_sets) < 1:
        data_sets = _get_dummies()

    series_count = len(data_sets)
    colours = palette(series_count)

    data_frame = pd.DataFrame()
    data_frames = []
    for ds in data_sets:
        df = ds.as_data_frame()
        day_filter = (df['timestamp'].dt.dayofweek == 5) | (df['timestamp'].dt.dayofweek == 6)
        #df = df.drop(df[day_filter].index)
        hour_filter = (df['timestamp'].dt.hour < 15) | (df['timestamp'].dt.hour > 21)
        #df = df.drop(df[hour_filter].index)

        #df = df.drop(df[day_filter | hour_filter].index)

        #df['temperature'][day_filter | hour_filter] = np.NaN
        #df['humidity'][day_filter | hour_filter] = np.NaN

        idx = df.ix[day_filter | hour_filter].index
        #df.temperature[idx] = np.NaN
        #df.humidity[idx] = np.NaN
        df.loc[idx,'temperature'] = np.NaN
        df.loc[idx,'humidity'] = np.NaN
        #df.at[dates[5], 'E'] = 7
        df = df.drop(idx)

        df['time'] = df['timestamp'].dt.time
        df['box_label'] = ["{1}-{2} - {0}".format(ds.name, tt, tt+1) for tt in df['timestamp'].dt.hour]
        df['box_label_merged'] = ["kl. {1}-{2} - {0}".format(ds.name.split(',')[0], tt, tt+1) for tt in df['timestamp'].dt.hour]
        df.loc[:,'colour'] = ds.name
        df.loc[:,'colour_merged'] = ds.name.split(',')[0]
        data_frames.append(df)
        data_frame = pd.concat([data_frame,df], ignore_index=True)

    #data_frame = pd.DataFrame(columns=['timestamp', 'temperature', 'humidity', 'box_label'])

    all_data_temp = BoxPlot(data_frame, values='temperature', label='box_label', color='colour', responsive=True, xlabel = "Time and place", ylabel = "Temperature / C", legend=False)
    all_data_humi = BoxPlot(data_frame, values='humidity', label='box_label', color='colour', responsive=True, xlabel = "Time and place", ylabel = "Relative humidity / \%", legend=False)

    all_data = gridplot([all_data_temp, all_data_humi], ncols=2, plot_width=500, plot_height=500, sizing_mode='scale_width', 
                        toolbar_options=dict(logo="grey"))
                        #toolbar_options=dict(logo="grey", location='above'), merge_tools=False)

    merged_data_temp = BoxPlot(data_frame, values='temperature', label='box_label_merged', color='colour_merged', responsive=True, xlabel = "Time and place", ylabel = "Temperature / C", legend=False)
    merged_data_humi = BoxPlot(data_frame, values='humidity', label='box_label_merged', color='colour_merged', responsive=True, xlabel = "Time and place", ylabel = "Relative humidity / \%", legend=False)

    merged_data = gridplot([merged_data_temp, merged_data_humi], ncols=2, plot_width=500, plot_height=500, sizing_mode='scale_width', 
                        toolbar_options=dict(logo="grey"))
                        #toolbar_options=dict(logo="grey", location='above'), merge_tools=False)


    ########## RENDER PLOTS ################

    resources = INLINE
    js_resources = resources.render_js()
    css_resources = resources.render_css()
    plot_script, plot_divs = components({'Data fra kl. 15 - 22, uden loerdag': all_data, 'Data fra kl. 15 - 22, uden loerdag, reference og uden udsugning': merged_data})

    return js_resources, css_resources, plot_script, plot_divs