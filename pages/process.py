# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Imports from this application
from app import app

# 1 column layout
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            ## Process

            ### About the Data
            
            The data for this project was originally donated to the UCI Machine Learning Repository in 1987. 
            Mushroom records are derived from *The Audubon Society Feild Guide to North American Mushrooms*(1981). 
            The guide identifies each species of mushroom as edible, definitely poisonous, or of unknown edibility. 
            The data set combines the latter class into the class poisonous. 
            There are 22 categorical features that can be used to predict whether a mushroom is edible or poisonous. 
            The dataset can be found in CSV format at <https://www.kaggle.com/uciml/mushroom-classification> 
            
            
            To make it easier for users of the app to understand the features, I have created a mapped version of 
            the dataset that replaces the single letter categorical values with the words they represent. 
            The notebook and mapped version of the dataset can be found in the GitHub repository associated with this app. 
            Click on the GitHub icon at the bottom of any page to access it.

            ### Get Baseline Score

            The distribution of the two classes are balanced with a split of 51.8% edible and 48.2% poisonous mushrooms. 
            Guessing that all the mushrooms are edible would yeild an accuracy score of 51.8%.

            ### Feature Selection
            
            Using the mushroom dataset, the model can obtain a perfect accuracy score using three features: odor, 
            gill_size, and spore_print_color. You can see from the permutation importance graph that odor was the 
            key feature for determining whether a mushroom was edible or poisonous.  

            """
        ),
        html.Img(src='assets/permutationOdor.png', className='img-fluid'),
        dcc.Markdown(
            """
            Taking odor out of the 
            """
        )

    ],
)

layout = dbc.Row([column1])