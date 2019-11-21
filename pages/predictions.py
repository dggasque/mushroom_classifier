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
                {'label': 'Fibrous', 'value': 'fibrous'},
                {'label': 'Grooves', 'value': 'grooves'},
                {'label': 'Scaly', 'value': 'scaly'},
                {'label': 'Smooth', 'value': 'smooth'}
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
                {'label': 'Broad', 'value': 'broad'},
                {'label': 'Narrow', 'value': 'narrow'}
            ],
            value='broad'
        ),
        dcc.Markdown('#### Gill Spacing'),
        dcc.Dropdown(
            id='gill_spacing',
            options = [
                {'label': 'Close', 'value': 'close'},
                {'label': 'Crowded', 'value': 'crowded'},
                {'label': 'Distant', 'value': 'distant'},
            ],
            value='distant'
        ),
    ],
    md=4,
)
column2 = dbc.Col(
    [ 
        dcc.Markdown('#### In What Habitat Did You Find The Mushroom?'),
        dcc.Dropdown(
            id='habitat',
            options = [
                {'label': 'Grasses', 'value': 'grasses'},
                {'label': 'Leaves', 'value': 'leaves'},
                {'label': 'Meadows', 'value': 'meadows'},
                {'label': 'Paths', 'value': 'paths'},
                {'label': 'Urban', 'value': 'urban'},
                {'label': 'Waste', 'value': 'waste'},
                {'label': 'Woods', 'value': 'woods'}
            ],
            value='grasses'
        ), 
        dcc.Markdown('#### What Type of Ring Does The Mushroom Have?'),
        dcc.Dropdown(
            id='ring_type',
            options = [
                {'label': 'Cobwebby', 'value': 'cobwebby'},
                {'label': 'Evanescent', 'value': 'evanescent'},
                {'label': 'Flaring', 'value': 'flaring'},
                {'label': 'Large', 'value': 'large'},
                {'label': 'Pendant', 'value': 'pendant'},
                {'label': 'Sheathing', 'value': 'sheathing'},
                {'label': 'Ring zone', 'value': 'zone'},
                {'label': 'None', 'value': 'none'}
            ],
            value='cobwebby'
        ), 
        dcc.Markdown('#### What Color are the Spores?'),
        dcc.Dropdown(
            id='spore_print_color',
            options = [
                {'label': 'Black', 'value': 'black'},
                {'label': 'Brown', 'value': 'brown'},
                {'label': 'Buff', 'value': 'buff'},
                {'label': 'Chocolate', 'value': 'chocolate'},
                {'label': 'Green', 'value': 'green'},
                {'label': 'Orange', 'value': 'orange'},
                {'label': 'Purple', 'value': 'purple'},
                {'label': 'White', 'value': 'white'},
                {'label': 'Yellow', 'value': 'yellow'}
            ],
            value='black'
        ),
        dcc.Markdown('#### How is the Stalk Shaped?'),
        dcc.Dropdown(
            id='stalk_shape',
            options = [
                {'label': 'Enlarging', 'value': 'enlarging'},
                {'label': 'Tapering', 'value': 'tapering'}
            ],
            value='enlarging'
        ), 
        dcc.Markdown('#### What Kind of Stalk Root Does The Mushroom Have?'),
        dcc.Dropdown(
            id='stalk_root',
            options = [
                {'label': 'Bulbous', 'value': 'bulbous'},
                {'label': 'Club', 'value': 'club'},
                {'label': 'Cup', 'value': 'cup'},
                {'label': 'Equal', 'value': 'equal'},
                {'label': 'Rhizomorph', 'value': 'rhizomorph'},
                {'label': 'Rooted', 'value': 'rooted'}
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
    
        
    if y_pred == 'edible':
        return f'Your mushroom is likely {y_pred}. BEWARE: There is a {y_pred_proba:.0f}% probability that the mushroom is poisonous!'
    else:
        return f'Your mushroom is likely {y_pred} with a predicted probability of {y_pred_proba:.0f}%!'


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
        return html.Img(src='assets/regrettable.png',className='img-fluid', style = {'height': '200px'})
    else:
        return html.Img(src='assets/edible.jpg',className='img-fluid', style = {'height': '200px'})