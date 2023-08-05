import os
import re
import json
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_styled_input as dsi
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
from flask_caching import Cache
from PIL import Image
import base64
from io import BytesIO
from urllib.parse import unquote
from . import app
from .helper import iter_contour, timeit, image_picker

#####################################################
# global variables
dataset_path = 'data'
color = {
    'centroid': 'OrangeRed', 
    'ctc': 'Crimson', 
    'nuclei': 'LightSkyBlue', 
    '+': 'Orange', 
    'immune': 'ForestGreen'
}

cache = Cache(app, config={'CACHE_TYPE': 'simple'})
page = dash.Dash(server=app)
page.title = 'Nuclei Viewer'

#####################################################
# frontend page layout
page.layout = html.Div([
        # Banner
        html.Div(className='banner', children=[
            html.Img(src="/assets/aixmed.png", className='logo'),
            html.H2('Nuclei Analysis App'),
            html.H6('© 2018 AIxMed, Inc. All Rights Reserved'),
            html.Img(src="/assets/logo.png")
        ]),
        # hidden variables
        html.Div(id='dummy', style={'display': 'none'}),
        # represents the URL bar, doesn't render anything
        dcc.Location(id='url', refresh=False),
        # Body
        html.Div(className='container row', children=[
            # menu and info
            html.Div(className='two columns', children=[
                # Dataset info
                html.Div(className='card', children=[
                    dcc.Dropdown(
                        id='dataset',
                        className='dropdown',
                        searchable=False,
                        placeholder='Dataset ...',
                    ),
                    dcc.Dropdown(
                        id='uid',
                        className='dropdown',
                        searchable=True,
                        placeholder='Samples ...',
                    ),
                    dsi.RadioItemRows(id='tile', style={'display': 'grid'}),
                ]),
                # Toolbar
                dsi.RadioItemRows(
                    id='img-mode',
                    className='card dash-styled-input',
                    options=[[
                        {'label': i, 'value': i} for i in 
                        ['RGB', 'EpCAM', 'CD45', 'DAPI']
                    ]],
                    value='RGB'
                ),
                dsi.RadioItemRows(
                    id='lock-zoom',
                    className='card dash-styled-input',
                    options=[[{'label': i, 'value': i} for i in ['Zoom lock', 'Refresh']]],
                    value='Zoom lock'
                ),
                dsi.RadioItemRows(
                    id='filter-nuclei',
                    className='card dash-styled-input',
                    options=[[{'label': i, 'value': i} for i in ['Adjacent', 'Generous']]],
                    value='Adjacent'
                ),
                dsi.RadioItemRows(
                    id='target-cell',
                    className='card dash-styled-input',
                    options=[[{'label': i, 'value': i} for i in ['Tumor', 'Immune']]],
                    value='Tumor'
                ),
                html.Div(className='card', children=[
                    html.Button(u'\U0001F4BE', id='save', className='icon'),
                    html.Button('+', id='add', className='icon'),
                    html.Button('-', id='del', className='icon disabled'),
                    html.Button(u'\u238C', id='reset', className='icon disabled'),
                ]),
                html.Table(id='info'),
            ]),
            # major content
            dcc.Graph(
                id='graph',
                className='ten columns',
                style={'height': '90vh'},
                config={
                    'modeBarButtonsToRemove': [
                        'sendDataToCloud', 'zoom2d', 'select2d', 'lasso2d',
                        'autoScale2d', 'hoverClosestCartesian',
                        'hoverCompareCartesian', 'toggleSpikelines', 'resetScale2d'
                    ],
                    'scrollZoom': True,
                    'doubleClick': 'autosize',
                    'displaylogo': False,
                }
            )
        ])
    ])

#####################################################
# backend callback functions
@page.callback(
    Output('dataset', 'options'), 
    [Input('dummy', 'n_clicks')]
)
@cache.memoize()
def update_dataset(_):
    # fire on page load
    return [{'label': f.name, 'value': f.name} for f in os.scandir(dataset_path) if f.is_dir()]

@page.callback(
    Output('uid', 'options'), 
    [Input('dataset', 'value')]
)
@cache.memoize()
def update_items(ds):
    ''' update items from selected dataset '''
    if not ds:
        return []
    return [
        {'label': shorten(f.name, n=20), 'value': f.name}
        for f in os.scandir(os.path.join(dataset_path, ds)) if f.is_dir()
    ]

@page.callback(
    Output('tile', 'options'), 
    [Input('uid', 'value')],
    [State('dataset', 'value')]
)
def update_tile(uid, ds):
    ''' update items from selected dataset '''
    if not ds or not uid:
        return [[]]
    metadata = read_metadata(os.path.join(ds, uid))
    if 'grid' not in metadata:
        return [[{'label': '', 'value': ''}]]
    grid = np.array(metadata['grid'])
    options = []
    for j in range(grid.shape[0]):
        option = []
        for i in range(grid.shape[1]):
            tile = '{}_{}'.format(j, i)
            path = os.path.join(ds, uid, tile)
            option.append({
                'label': grid[j, i], 
                'value': tile, 
                'disabled': False if is_valid_sample(path) else True
            })
        options.append(option)
    return options

@page.callback(
    Output('tile', 'value'),
    [Input('tile', 'options')])
def update_tile_value(tile):
    if tile and len(tile[0]):
        return tile[0][0]['value']

@page.callback(
    Output('graph', 'figure'),
    [Input('tile', 'value'), Input('img-mode', 'value'), Input('filter-nuclei', 'value')],
    [State('dataset', 'value'), State('uid', 'value'), 
     State('lock-zoom', 'value'), State('graph', 'relayoutData')]
)
def update_graph(tile, mode, filter, ds, uid, zoom, relayout):
    if not ds or not uid or tile is None:
        return {}
    path = os.path.join(ds, uid, tile)
    res = b64img(path, mode)
    if not res:
        return {'layout': {'title': 'Invalid image data'}}
    b64, w, h = res
    # figure images
    images = [dict(
        xref='x',
        yref='y',
        x=0,
        y=0,
        yanchor='top', # top-left is (0, 0)
        sizing='stretch',
        sizex=w,
        sizey=h,
        layer='below',
        source=b64
    )] if mode else []
    # figure grid lines
    xaxis = dict(
        autorange=False,
        showgrid=False,
        zeroline=False,
        showline=False,
        range=(0, w),
        scaleanchor='y',
        scaleratio=1,
    )
    yaxis = dict(
        autorange=False,
        showgrid=False,
        zeroline=False,
        showline=False,
        range=(h, 0),
    )
    if relayout and zoom == 'Zoom lock':
        if 'xaxis.range[0]' in relayout:
            xaxis['range'] = (
                relayout['xaxis.range[0]'],
                relayout['xaxis.range[1]']
            )
        if 'yaxis.range[0]' in relayout:
            yaxis['range'] = (
                relayout['yaxis.range[0]'],
                relayout['yaxis.range[1]']
            )
    # custom menu with buttons
    contour_menu = dict(
        buttons=[   
            dict(
                args=['visible', True],
                label='Show Mask',
                method='restyle'
            ),
            dict(
                args=['visible', False],
                label='Hide Mask',
                method='restyle'
            )
        ],
        direction='left',
        showactive=True,
        type='buttons',
        x=0,
        xanchor='left',
        y=1.01, # slight above figure
        yanchor='top',
    )
    menus = [contour_menu]
    # configure legend
    legend = dict(
        x=0,
        y=1.01,
        orientation='h'
    )
    # configure layout
    layout = dict(
        autosize=True,
        dragmode='pan',
        hovermode='closest',
        xaxis=xaxis,
        yaxis=yaxis,
        images=images,
        margin=dict(t=10, b=30, l=40, r=10, pad=4),
        #updatemenus=menus,
        legend=legend
    )
    data = traces(path, (h, w), (filter == 'Adjacent'))
    return dict(data=data, layout=layout)

@page.callback(
    Output('dummy', 'children'),
    [Input('save', 'n_clicks')],
    [State('dataset', 'value'), State('uid', 'value'), 
     State('tile', 'value'), State('target-cell', 'value'),
     State('graph', 'figure')],
)
def save_data(btn, ds, uid, tile, _, figure):
    ''' detect selected masks by shape's color '''
    if not ds or not uid or tile is None:
        return []
    path = os.path.join(ds, uid, tile)
    metadata = read_metadata(path)
    data = []
    for trace in figure['data']:
        if trace['legendgroup'] == 'ctc':
            data.append(trace['customdata'][0])
    metadata['ctc'] = data
    write_metadata(path, metadata)
    return []

#####################################################
# utility functions
def traces(path, size, filter):
    ''' parse json in syntax: 
    {
       'centroid': [[y0, x0], [y1, x1], [y2, x2] ... ], 
       'ctc': ['mask01.png', 'mask02.png' ...] 
    }
    '''
    items = []
    metadata = read_metadata(path)
    # parse centroid markers
    centroid = None
    if 'centroid' in metadata:
        centroid = np.array(metadata['centroid'])
        items.append(dict(
            showlegend = True,
            legendgroup = 'centroid',
            name = 'centroid',
            mode = 'markers',
            hoverinfo = 'x+y',
            marker = {'color': color['centroid'], 'symbol': 'x'},
            x = centroid[:, 1],
            y = centroid[:, 0]
        ))
    # parse contours
    def trace(group='nulcei', name='', is_legend=False, visible=True, x=[0], y=[0]):
        return dict(
            showlegend = is_legend,
            legendgroup = group,
            name = shorten(name),
            customdata = [name],
            mode = 'lines',
            line = {'color': color[group]},
            x = x,
            y = y,
            fill = 'none' if is_legend else 'toself',
            opacity = 1.0 if is_legend else 0.3,
            hoverinfo = 'skip' if is_legend else 'name',
            visible = True if visible else 'legendonly',
        )
    # non-interactive legend placeholders
    for g in ['nuclei', 'ctc', 'immune', '+',]:
        items.append(trace(g, g, True, g != 'nuclei'))
    # iterate contours
    filter = centroid if filter else None
    for m, c in iter_contour(os.path.join(dataset_path, path), size, filter):
        g = 'ctc' if 'ctc' in metadata and m in metadata['ctc'] else 'nuclei'
        c = np.vstack((c, c[0])) # closure shape to first pixel
        items.append(trace(g, m, False, g != 'nuclei', c[:, 1], c[:, 0]))
    return items

def is_valid_sample(path):
    fp = os.path.join(dataset_path, path, 'images')
    return os.path.exists(fp)

def shorten(str, n=10, suffix=False):
    # truncate a string to at most n characters
    if suffix:
        n = n//2
        return str[:n] + (str[n:] and '...' + str[-n:])
    else:
        return str[:n] + (str[n:] and '...')

def read_metadata(path):
    fp = os.path.join(dataset_path, path, 'meta.json')
    if not os.path.exists(fp):
        return {}
    with open(fp) as f:
        data = json.load(f)
        return data

def write_metadata(path, data):
    fp = os.path.join(dataset_path, path, 'meta.json')
    with open(fp, 'w') as f:
        json.dump(data, f)

@cache.memoize()
def b64img(path, mode, quality=75):
    # base64 encoding
    fp = image_picker(dataset_path, path, mode)
    if not fp:
        return None
    if isinstance(fp, list):
        r, g, b = Image.open(fp[0]), Image.open(fp[1]), Image.open(fp[2])
        im = Image.merge('RGB', (r, g, b))
    else:
        im = Image.open(fp)
        if im.mode == 'I;16':
            # Convert from 16-bit to 8-bit.
            # Image.point() does not support divide operation.
            # 255/65535 = 0.0038910505836575876, map [0, 65535] to [0, 255] 
            im = im.point(lambda i: i * 0.0038910505836575876)
            im = im.convert('L')
        if im.mode == 'RGBA':
            im = im.convert('RGB')
        if im.mode == 'L':
            # colorize grayscale image
            r = g = b = np.zeros_like(im)
            gray = np.asarray(im)
            channels = {
                'DAPI' : (r, g, gray),
                'CD45' : (r, gray, b),
                'EpCAM': (gray, g, b),
            }
            rgb = np.dstack(channels[mode])
            im = Image.fromarray(rgb)
    # convert to base64 jpeg
    w, h = im.size
    buff = BytesIO()
    im.save(buff, format='jpeg', quality=quality)
    encoded = base64.b64encode(buff.getvalue()).decode("utf-8")
    return 'data:image/jpeg;base64, ' + encoded, w, h
