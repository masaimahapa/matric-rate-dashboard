import pandas as pd
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import ipywidgets as widgets
import dash_table

import numpy
from datetime import datetime as dt

global data
data= pd.read_csv('data/matric-pass-rate.csv')
data= data.set_index('Province')


def add_national_average(data):
    numbers={}

    for col in data.columns:
        numbers[f'{col}']=round(sum([float(each) for each in data[col]])/len(data), 2)
    
    ser= pd.Series(numbers).rename('National')
    return data.append(pd.Series(ser), ignore_index=False)


data= add_national_average(data)
data= data.rename(columns={"2009":2009, "2010":2010, "2011":2011, "2012":2012})

app= dash.Dash(__name__)
server= app.server


app.layout= html.Div([
    
    html.H1('Matric Pass Rates',
    style={
        'textAlign':'center',
        'color':'red'
    }),
    dcc.Tabs(id='tab', value='stats', children=[
        dcc.Tab(label='stats', value='tab-all'),
        dcc.Tab(label='table', value='table')
    ]
    
    )
    ,

    html.Div([
            

    dcc.Dropdown(
        id='Province-Dropdown',
        
        placeholder='choose a province',
        #multi=True,
        options=[
            {'label': 'National', 'value':'National'},
            {'label': 'Gauteng', 'value':'Gauteng'},
            {'label': 'Western Cape', 'value':'Western Cape'},
            {'label': 'Eastern Cape', 'value':'Eastern Cape'},
            {'label': 'Limpopo', 'value':'Limpopo'},
            {'label': 'Free State', 'value': 'Free State'},
            {'label': 'North West', 'value':'North West'},
            {'label': 'Mpumalanga', 'value':'Mpumalanga'},
            {'label':'Northern Cape', 'value': 'Northern Cape'},
            {'label': 'KwaZulu-Natal', 'value':'KwaZulu-Natal'},
            
        ],
        value=['National'],
        

    ),
    dcc.DatePickerRange(
        id='my_date_picker',
        start_date= dt(2009,1,1),
        end_date= dt(2013,1,1)      
    ),
    
    html.Br(),
    
    dcc.RangeSlider(
        id='date-range',
        
        value=[2010,2012],
        min=2008,
        max=2013,
        
        step=1,
        
        #marks= {i:i for i in range(2009,2013)}
    ),
    dcc.Graph(
        id='pass-rate-bar',
        
    ),
],
 style={'width':'55%', 'float':'right', 'display':'inline-block'} ),

html.Div([
    html.H2('average pass rate%',
    style={
        'color':'red'
    }),
    html.Div(
        id='Output-container',
        style={
            'font-size':'40px'
        }
    ),
    dcc.Graph(
        id='pie'
    )
], 
style={'width':'40%', 'float':'left', 'display':'inline-block'} ,
id='main-container',),



    ])


@app.callback(Output('main-container', 'children'),
[Input('tab', 'value')])
def update_page(tab):
    if tab=='tab-all':
        return html.Div([
    html.H2('average pass rate%',
    style={
        'color':'red'
    }),
    html.Div(
        id='Output-container',
        style={
            'font-size':'40px'
        }
    ),
    dcc.Graph(
        id='pie',
        #values=data.loc[]
    )
], )
    elif tab=='table':
        return html.Div([
            html.H1('Just the table'),
            dash_table.DataTable(
                id='columns',
                columns=[{"name":each, "id":each} for each in data.columns],
                data= data.to_dict('records')
            )
        ])
        

@app.callback(Output(component_id='pass-rate-bar', component_property= 'figure'),
 [Input(component_id='my_date_picker', component_property='start_date'),
 Input(component_id='my_date_picker', component_property='end_date'),
 Input(component_id='Province-Dropdown', component_property='value'),
 Input(component_id='date-range', component_property='min'),
 Input(component_id='date-range', component_property='max')
 ])
def update_graph(start_date, end_date, value, min, max):
    my_plots= []
    #loop over province
    value= [value]

    for each in value:
        trace1= {'data': [go.Scatter(
            x=list(data.columns),
            #x=list(data[data.columns<=int(min)].columns),
            y= data.loc[each],
            mode='lines',
            name= f'{each}',
        )],
        'layout': go.Layout(
            xaxis={'title':'Date', 'tickvals':['2009', '2010', '2011', '2012', '2013']},
            yaxis={'title':'passes'},
            plot_bgcolor='white',
            font={'color':'black'}
        )}
        my_plots.append(trace1)
    return my_plots[0]



@app.callback(Output('Output-container', 'children'),
[Input('Province-Dropdown', 'value')])
def update_text(value):
    total= [float(each) for each in data.loc[value]]
    return f'{value} : {round(sum(total)/ len(total), 2)}% '


@app.callback(Output('pie', 'figure'), [Input('Province-Dropdown', 'value')])
def update_pie(value):
    values=[20,10,15]
    my_pie= {'data': [go.Pie(
        values= values,
        labels=['limpopo', 'gauteng', 'north west']
         
    )]}
    return my_pie



if __name__ == "__main__":
    app.run_server(debug=True)