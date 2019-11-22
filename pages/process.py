# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Imports from this application
from app import app


web_url = 'https://gist.githubusercontent.com/dggasque/cf034a3ce095830bd891b5af42987fb0/raw/7223d727d1aa65ad915575fe9ff46d7ee1be0f0f/mushroom_mapped.csv'

df = pd.read_csv(web_url)

fig1 = px.histogram(df, x="odor", color="class")

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
        html.Img(src='assets/PermutationImportanceWithOdor.png', className='img-fluid'),
        dcc.Markdown(
            """
            The distribution of odors associated with each class of mushroom shows why the feature dominates the model.
            """
        ),
        dcc.Graph(figure=fig1),
        dcc.Markdown(
            """
            While using odor in the model creates the most accurate and efficient model, I have chosen to leave it out to make 
            *Edible or Regrettable* more interesting. By removing odor we are able to train a model that uses more features. This 
            also makes the model more like the process that someone might use to identify a mushroom.

            Looking at permutation importance after removing `odor` from the predictiopn model, there are nine features we can use 
            to predict the edibility of the mushrooms: `cap_surface`, `bruises`, `gill_spacing`, `gill_size`, `stalk_shape`, `stalk_root`, 
            `ring_type`, `spore_print_color`, and `habitat`.
            """
        ),
        html.Img(src='assets/PermutationWithoutOdor.png', className='img-fluid'),
        dcc.Markdown(
            """
            #### Model Selection
            
            This is a classification problem, so I began with a Logistic Regression model which yeilded a validation score of 92.5% and 
            Area Under the Receiver Operator Curve score of 93.8%. This is signifigantly better than the baseline score; however, a tree 
            based model can perform even better. I used Random Forest Classifier to build the final model. To train and test the data, 
            I used a three way train, valadate and test set split. You can find the evaluation of the model on the Insights page. 
            Below is the evaluation of the validation set using the linear model for comparision.

            ##### Classification Report for Logistic Regression
            """
        ),
        html.Img(src='assets/LRClassificationReport.png', className='img-fluid'),
        dcc.Markdown(
            """
            The Precision score for edible muishrooms is 90% which in terms of predicitive modeling can seem like a high score, but a 10% false 
            positive rate is also relatively high considering the consiquences can be deadly. The Recall score for poisonous mushrooms is 89%, so 
            11% of the poisonous mushrooms were misclassified as edible.

            ##### Confusion Matrix for Logistic Regression
            """
        ),
        html.Img(src='assets/LRConfusionMatrix.png', className='img-fluid'),
    ],
)

layout = dbc.Row([column1])