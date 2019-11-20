# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from joblib import load
import pandas as pd

# Imports from this application
from app import app

pipeline = load('assets/pipeline.joblib')

# 2 column layout. 1st column width = 4/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            ## Predictions

            Your instructions: How to use your app to get new predictions.

            """
        ),
        dcc.Markdown('#### Gill Attatchment Type'),
        dcc.Dropdown(
            id='gill_attachment',
            options = [
                {'label': 'attached', 'value': 'attached'},
                {'label': 'descending', 'value': 'descending'},
                {'label': 'free', 'value': 'free'},
                {'label': 'notched', 'value': 'notched'}
            ],
            value='attached'
        ),
        dcc.Markdown('#### Gill Color'),
        dcc.Dropdown(
            id='gill_color',
            options = [
                {'label': 'black', 'value': 'black'},
                {'label': 'brown', 'value': 'brown'},
                {'label': 'buff', 'value': 'buff'},
                {'label': 'chocolate', 'value': 'chocolate'},
                {'label': 'gray', 'value': 'gray'},
                {'label': 'green', 'value': 'green'},
                {'label': 'orange', 'value': 'orange'},
                {'label': 'pink', 'value': 'pink'},
                {'label': 'purple', 'value': 'purple'},
                {'label': 'red', 'value': 'red'},
                {'label': 'white', 'value': 'white'},
                {'label': 'yellow', 'value': 'yellow'}
            ],
            value='black'
        ),
        dcc.Markdown('#### Gill Size'),
        dcc.Dropdown(
            id='gill_size',
            options = [
                {'label': 'broad', 'value': 'broad'},
                {'label': 'narrow', 'value': 'narrow'}
            ],
            value='broad'
        ),
        dcc.Markdown('#### Gill Spacing'),
        dcc.Dropdown(
            id='gill_spacing',
            options = [
                {'label': 'close', 'value': 'close'},
                {'label': 'crowded', 'value': 'crowded'},
                {'label': 'distant', 'value': 'distant'},
            ],
            value='distant'
        ),
        dcc.Markdown('#### Habitat'),
        dcc.Dropdown(
            id='habitat',
            options = [
                {'label': 'grasses', 'value': 'grasses'},
                {'label': 'leaves', 'value': 'leaves'},
                {'label': 'meadows', 'value': 'meadows'},
                {'label': 'paths', 'value': 'paths'},
                {'label': 'urban', 'value': 'urban'},
                {'label': 'waste', 'value': 'waste'},
                {'label': 'woods', 'value': 'woods'}
            ],
            value='grasses'
        ),
        dcc.Markdown('#### Population'),
        dcc.Dropdown(
            id='population',
            options = [
                {'label': 'abundant', 'value': 'abundant'},
                {'label': 'clustered', 'value': 'clustered'},
                {'label': 'numerous', 'value': 'numerous'},
                {'label': 'scattered', 'value': 'scattered'},
                {'label': 'several', 'value': 'several'},
                {'label': 'solitary', 'value': 'solitary'}
            ],
            value='abundant'
        ), 
        dcc.Markdown('#### Spore Print Color'),
        dcc.Dropdown(
            id='spore_print_color',
            options = [
                {'label': 'black', 'value': 'black'},
                {'label': 'brown', 'value': 'brown'},
                {'label': 'buff', 'value': 'buff'},
                {'label': 'chocolate', 'value': 'chocolate'},
                {'label': 'green', 'value': 'green'},
                {'label': 'orange', 'value': 'orange'},
                {'label': 'purple', 'value': 'purple'},
                {'label': 'white', 'value': 'white'},
                {'label': 'yellow', 'value': 'yellow'}
            ],
            value='black'
        ), 
    ],
    md=4,
)

column2 = dbc.Col(
    [
        html.H2('Edible or Regrettable?', className='mb-5'), 
        html.Div(id='prediction-content', className='lead', style={'font-weight': 'bold'}),
        html.Div(id='prediction-image') 
    ]
)

layout = dbc.Row([column1, column2])

@app.callback(
    Output('prediction-content', 'children'),
    [
        Input('spore_print_color', 'value'), 
        Input('gill_size', 'value'),
        Input('gill_attachment', 'value'),
        Input('population', 'value'),
        Input('habitat', 'value'), 
        Input('gill_spacing', 'value'),
        Input('gill_color', 'value')  
    ],
)

def predict(
    spore_print_color,  
    gill_size,
    gill_attachment,
    population, 
    habitat, 
    gill_spacing,
    gill_color):

    #make dataframe from inputs
    df = pd.DataFrame(
        data=[[ spore_print_color,
               gill_size,  
               gill_attachment, 
               population, 
               habitat, 
               gill_spacing,
               gill_color]],
        columns= ['spore_print_color',
                  'gill_size', 
                  'gill_attachment', 
                  'population', 
                  'habitat', 
                  'gill_spacing',
                  'gill_color']
    )
    
    # Get the model's prediction
    y_pred = pipeline.predict(df)[0]
        
    class_index = 1
    y_pred_proba = pipeline.predict_proba(df)[:, class_index][0]
    
    return f'Your mushroom is {y_pred}. There is a probability of {y_pred_proba:.2f} that the mushroom is poisonous' 

@app.callback(
    Output('prediction-image', 'children'),
    [
        Input('spore_print_color', 'value'), 
        Input('gill_size', 'value'),
        Input('gill_attachment', 'value'),
        Input('population', 'value'),
        Input('habitat', 'value'), 
        Input('gill_spacing', 'value'),
        Input('gill_color', 'value')  
    ],
)

def predict_image(
    spore_print_color,
    gill_size, 
    gill_attachment, 
    population, 
    habitat, 
    gill_spacing,
    gill_color):

    #make dataframe from inputs
    df = pd.DataFrame(
        data=[[ spore_print_color,
               gill_size,  
               gill_attachment, 
               population, 
               habitat, 
               gill_spacing,
               gill_color]],
        columns= ['spore_print_color',
                  'gill_size',  
                  'gill_attachment', 
                  'population', 
                  'habitat', 
                  'gill_spacing',
                  'gill_color']
    )
    
    # Get the model's prediction
    y_pred = pipeline.predict(df)[0]

    if y_pred == 'poisonous':
        return html.Img(src='assets/regrettable.png',className='img-fluid', style = {'height': '400px'})
    else:
        return html.Img(src='assets/edible.jpg',className='img-fluid', style = {'height': '400px'})