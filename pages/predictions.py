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

            Use the dropdown menus to select the characteristics associated with the mushroom.


            """
        ),
        dcc.Markdown('#### What is the Cap Surface'),
        dcc.Dropdown(
            id='cap_surface',
            options = [
                {'label': 'fibrous', 'value': 'fibrous'},
                {'label': 'grooves', 'value': 'grooves'},
                {'label': 'scaly', 'value': 'scaly'},
                {'label': 'smooth', 'value': 'smooth'}
            ],
            value='fibrous'
        ),        
        dcc.Markdown('#### Does the Mushroom Bruise?'),
        dcc.Dropdown(
            id='bruises',
            options = [
                {'label': 'Yes', 'value': 'yes'},
                {'label': 'No', 'value': 'no'},
            ],
            value='yes'
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
        dcc.Markdown('#### In What Habitat Did You Find The Mushroom?'),
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
    ],
    md=4,
)
column2 = dbc.Col(
    [ 
        dcc.Markdown('#### What Type of Ring Does The Mushroom Have?'),
        dcc.Dropdown(
            id='ring_type',
            options = [
                {'label': 'cobwebby', 'value': 'cobwebby'},
                {'label': 'evanescent', 'value': 'evanescent'},
                {'label': 'flaring', 'value': 'flaring'},
                {'label': 'large', 'value': 'large'},
                {'label': 'pendant', 'value': 'pendant'},
                {'label': 'sheathing', 'value': 'sheathing'},
                {'label': 'ring zone', 'value': 'zone'},
                {'label': 'none', 'value': 'none'}
            ],
            value='cobwebby'
        ), 
        dcc.Markdown('#### What Color are the Spores?'),
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
        dcc.Markdown('#### How is the Stalk Shaped?'),
        dcc.Dropdown(
            id='stalk_shape',
            options = [
                {'label': 'enlarging', 'value': 'enlarging'},
                {'label': 'tapering', 'value': 'tapering'}
            ],
            value='enlarging'
        ), 
        dcc.Markdown('#### What Kind of Stalk Root Does The Mushroom Have?'),
        dcc.Dropdown(
            id='stalk_root',
            options = [
                {'label': 'bulbous', 'value': 'bulbous'},
                {'label': 'club', 'value': 'club'},
                {'label': 'cup', 'value': 'cup'},
                {'label': 'equal', 'value': 'equal'},
                {'label': 'rhizomorph', 'value': 'rhizomorph'},
                {'label': 'rooted', 'value': 'rooted'}
            ],
            value='bulbous'
        ), 
    ],
    md=4,
)

column3 = dbc.Col(
    [
        html.H2('Edible or Regrettable?', className='mb-5'), 
        html.Div(id='prediction-content', className='lead', style={'font-weight': 'bold'}),
        html.Div(id='prediction-image') 
    ]
)

layout = dbc.Row([column1, column2, column3])

@app.callback(
    Output('prediction-content', 'children'),
    [
        Input('cap_surface', 'value'), 
        Input('bruises', 'value'),
        Input('gill_spacing', 'value'),
        Input('gill_size', 'value'),
        Input('stalk_shape', 'value'), 
        Input('stalk_root', 'value'),
        Input('ring_type', 'value'), 
        Input('spore_print_color', 'value'),
        Input('habitat', 'value')    
    ],
)

def predict(
    cap_surface, 
    bruises, 
    gill_spacing, 
    gill_size, 
    stalk_shape,
    stalk_root, 
    ring_type, 
    spore_print_color, 
    habitat
):

    if bruises == 'yes':
        bruises = True
    else:
         bruises = False
    
    #make dataframe from inputs
    df = pd.DataFrame(
        data=[[cap_surface, 
               bruises,
               gill_spacing, 
               gill_size, 
               stalk_shape,
               stalk_root, 
               ring_type,
               spore_print_color,
               habitat]],
        columns= ['cap_surface', 
                  'bruises', 
                  'gill_spacing', 
                  'gill_size', 
                  'stalk_shape',
                  'stalk_root', 
                  'ring_type', 
                  'spore_print_color', 
                  'habitat']
    )
    
    # Get the model's prediction
    y_pred = pipeline.predict(df)[0]
    
    class_index = 1
    y_pred_proba = (pipeline.predict_proba(df)[:, class_index][0]) * 100
    
    return f'Your mushroom is {y_pred}. There is a {y_pred_proba:.0f}% probability that the mushroom is poisonous!' 

@app.callback(
    Output('prediction-image', 'children'),
    [
        Input('cap_surface', 'value'), 
        Input('bruises', 'value'),
        Input('gill_spacing', 'value'),
        Input('gill_size', 'value'),
        Input('stalk_shape', 'value'), 
        Input('stalk_root', 'value'),
        Input('ring_type', 'value'), 
        Input('spore_print_color', 'value'),
        Input('habitat', 'value')     
    ],
)

def predict(
    cap_surface, 
    bruises, 
    gill_spacing, 
    gill_size, 
    stalk_shape,
    stalk_root, 
    ring_type, 
    spore_print_color, 
    habitat
):

    if bruises == 'yes':
        bruises = True
    else:
         bruises = False
    
    #make dataframe from inputs
    df = pd.DataFrame(
        data=[[cap_surface, 
               bruises,
               gill_spacing, 
               gill_size, 
               stalk_shape,
               stalk_root, 
               ring_type,
               spore_print_color,
               habitat]],
        columns= ['cap_surface', 
                  'bruises', 
                  'gill_spacing', 
                  'gill_size', 
                  'stalk_shape',
                  'stalk_root', 
                  'ring_type', 
                  'spore_print_color', 
                  'habitat']
    )
    
    # Get the model's prediction
    y_pred = pipeline.predict(df)[0]

    if y_pred == 'poisonous':
        return html.Img(src='assets/regrettable.png',className='img-fluid', style = {'height': '400px'})
    else:
        return html.Img(src='assets/edible.jpg',className='img-fluid', style = {'height': '400px'})