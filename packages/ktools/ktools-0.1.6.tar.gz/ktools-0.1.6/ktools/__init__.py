"""ktools - kirin's toolkit."""

__version__ = '0.1.6'
__author__ = 'fx-kirin <ono.kirin@gmail.com>'
__all__ = ['get_top_correlations', 'get_bottom_correlations', 'get_diff_from_initial_value', 
           'convert_datetimeindex_to_timestamp', 'bokeh_scatter', 'bokeh_categorical_scatter', 'bokeh_bar_plot',
           'setup_logger']

import numpy as np
import time
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.models import HoverTool
from bokeh.io import output_notebook
from bokeh.palettes import viridis
import seaborn as sns
import logzero
import logging 

def get_redundant_pairs(df):
    '''Get diagonal and lower triangular pairs of correlation matrix'''
    pairs_to_drop = set()
    cols = df.columns
    for i in range(0, df.shape[1]):
        for j in range(0, i+1):
            pairs_to_drop.add((cols[i], cols[j]))
    return pairs_to_drop

def get_top_correlations(df, n=5):
    au_corr = df.corr().unstack()
    labels_to_drop = get_redundant_pairs(df)
    au_corr = au_corr.drop(labels=labels_to_drop).sort_values(ascending=False)
    return au_corr[0:n]

def get_bottom_correlations(df, n=5):
    au_corr = df.corr().unstack()
    labels_to_drop = get_redundant_pairs(df)
    au_corr = au_corr.drop(labels=labels_to_drop).sort_values(ascending=False)
    return au_corr[0:n]

def get_diff_from_initial_value(series):
    return (series / (series.iat[0] - 1))

def convert_datetimeindex_to_timestamp(index):
    return (index.astype(np.int64).astype(np.float) // 10**9) + time.timezone

def bokeh_scatter(x, y):
    source = ColumnDataSource(
            data=dict(
                x=x,
                y=y,
                desc=x.index,
            )
        )

    hover = HoverTool(
            tooltips=[
                ("(x,y)", "($x, $y)"),
                ("index", "@desc"),
            ]
        )

    p = figure(plot_width=1600, plot_height=700, tools=[hover, 'pan', 'box_zoom', 'reset'],
               title="Mouse over the dots")

    p.circle('x', 'y', size=5, source=source)
    show(p)
    
def bokeh_categorical_scatter(df, x_label, y_label, category_label, desc=None):
    hover = HoverTool(
            tooltips=[
                ("(x,y)", "(@x, @y)"),
                ("index", "@desc"),
            ]
        )
    if desc is None:
        desc = df[x_label].index

    p = figure(plot_width=1600, plot_height=1000, tools=[hover, 'wheel_zoom', 'pan', 'box_zoom', 'reset'],
               title="Mouse over the dots")

    categories = df[category_label]
    category_size = len(categories.unique())
    colors = sns.color_palette("hls", category_size).as_hex()
    name = df['業種'].name
    for i, category in enumerate(categories.unique()):
        p_x = df[df[name] == category][x_label]
        p_y = df[df[name] == category][y_label]
        p_desc = desc[df[name] == category]
        source = ColumnDataSource(
                data=dict(
                    x=p_x,
                    y=p_y,
                    desc=p_desc,
                )
            )
        p.circle('x', 'y', size=5, source=source, color=colors[i], legend=str(category))
    p.legend.location = "top_right"
    p.legend.click_policy="hide"
    show(p)
    
def bokeh_bar_plot(p_x):
    palette = sns.color_palette("hls", len(p_x)).as_hex()
    hover = HoverTool(
        tooltips=[
            ("(x,y)", "(@x, @y)"),
        ]
    )
    p = figure(x_range=p_x.index.astype(str).values, plot_width=800, plot_height=600, tools=[hover, 'wheel_zoom', 'pan', 'box_zoom', 'reset'])

    p_desc = p_x.index
    source = ColumnDataSource(
            data=dict(
                x=p_x.index.astype(str),
                y=p_x.values,
                color=palette
            ),
        )
    p.vbar('x', top='y', width=0.9, source=source, color='color')
    show(p)

def setup_logger(output_file=None):
    formatter = logzero.LogFormatter(fmt='%(color)s[%(levelname)1.1s %(asctime)s %(name)s:%(module)s:%(lineno)d]%(end_color)s %(message)s')
    logzero.__name__ = ''
    logzero.setup_logger('', output_file, formatter=formatter)
