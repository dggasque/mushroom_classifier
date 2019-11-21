# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from joblib import load
import pandas as pd
import plotly.graph_objs as go

# Imports from this application
from app import app

pdp = load('assets/pdp.joblib')
pdp2 = load('assets/pdp2.joblib')
pdp3 =load('assets/pdp3.joblib')

surface = go.Surface(
    x=pdp.columns,
    y=pdp.index,
    z=pdp.values
)

fig = go.Figure(surface)

fig.update_layout(scene = dict(
                    xaxis_title='Spore Print Color',
                    yaxis_title='Ring Type',
                    zaxis_title='Predicted Probability of Poisonous Mushroom'),
                    width=700,
                    margin=dict(r=20, b=10, l=10, t=10))


surface2 = go.Surface(
    x=pdp2.columns,
    y=pdp2.index,
    z=pdp2.values
)

fig2 = go.Figure(surface2)

fig2.update_layout(scene = dict(
                    xaxis_title='Spore Print Color',
                    yaxis_title='Gill Size',
                    zaxis_title='Predicted Probability of Poisonous Mushroom'),
                    width=700,
                    margin=dict(r=20, b=10, l=10, t=10))

surface3 = go.Surface(
    x=pdp3.columns,
    y=pdp3.index,
    z=pdp3.values
)

fig3 = go.Figure(surface3)

fig3.update_layout(scene = dict(
                    xaxis_title='Gill Spacing',
                    yaxis_title='Gill Size',
                    zaxis_title='Predicted Probability of Poisonous Mushroom'),
                    width=700,
                    margin=dict(r=20, b=10, l=10, t=10))

# 1 column layout
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            ## Insights

            ### Evaluation of The Model

            Using Random Forest Classifier, the model is able to predict the edibility of mushrooms with
            100% accuracy. You can see from the confusion matrix from the test set that ther were no false 
            positives for the edible class. Nor were there any poisonous mushrooms predicted as edible.

            #### Confusion Matrix Fitting the Model to the Test Set
            """
        ),
        html.Img(src='assets/ConfusionMatrix.png', className='img-fluid'),
        dcc.Markdown(
            """
            #### Classification Report Fitting the Model to the Test Set
    
            """
        ),
        html.Img(src='assets/RFClassificationReport.png', className='img-fluid'),
        dcc.Markdown(
            """
            As expected from the confusion matrix, the Precision score for edible mushrooms is 
            100% and the recall score for poisonous mushrooms is also 100%. I have included the prediction
            probability of the mushroom being poisonous in the applications predictions. While 
            the model fits the test data perfectly. It should still be understood that there is some level of 
            uncertainty in the hypothetical situation that a new mushroom has been discovered that was not 
            included in the original dataset.
    
            """
        ),
        dcc.Markdown(
            """
            ### How the Model Decides

            Analyzing the principle dependencies of the individual features, I found that `spore_print_color`
            and `ring_type` the biggest impacts on determining that a mushroom was poisionous. 
            """
        ),
        html.Img(src='assets/SporePrintColorPDP.png', className='img-fluid'),
        html.Img(src='assets/RingTypePDP.png', className='img-fluid'),
        dcc.Markdown(
            """
            This 3D Plotly graph demonstrates how the two features interact with each other. 
            """
        ),
        dcc.Graph(figure=fig),
        dcc.Markdown(
            """
            To determine a mushroom is edible, `gill_spacing` and `gill_size` had the biggest impact
            on reducing the probability that the mushroom was poisonous.
            """
        ),
        html.Img(src='assets/GillSpacingPDP.png', className='img-fluid'),
        html.Img(src='assets/GillSizePDP.png', className='img-fluid'),
        dcc.Markdown(
            """
            You can see from this 3D graph the interaction of `gill_spacing` and `gill_size` have on 
            the predicted probability. A mushroom with narrow and close gills has a high probability of being 
            poisonous; however shifting either spacing or size can signifigantly reduce the probability. 
            """
        ),
        dcc.Graph(figure=fig3),
        dcc.Markdown(
            """
            You can see from this 3D graph the interaction of `gill_size` and `spore_print_color` have on 
            the predicted probability. A broad gill size reduces the probability with some colors.
            """
        ),
        dcc.Graph(figure=fig2),
    ],
)

layout = dbc.Row([column1])