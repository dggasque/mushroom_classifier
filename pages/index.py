# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

# Imports from this application
from app import app

# 2 column layout. 1st column width = 4/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            ## Edible or Regrettable?

            Living in the Pacific Northwest, the rain brings delightful and dangerous mushrooms alike.  
            *Edible or Regrettable* categorizes mushrooms in the *Lepiota* or *Agaricus* family as edible or poisonous, based on a few key characteristics.  
            Questionable mushrooms are categorized as poisonous, so rest assured that your edible mushrooms will be delicious.

            DISCLAIMER: I am just a data scientist and mushroom hunting hobbyist. This app is for educational purposes only. 
            """
        ),
        dcc.Link(dbc.Button('Can I Eat This?', color='primary'), href='/predictions')
    ],
    md=4,
)

column2 = dbc.Col(
    [
        html.Img(src='assets/RamsWithMushroom.jpg', className='img-fluid')
    ]
)

layout = dbc.Row([column1, column2])