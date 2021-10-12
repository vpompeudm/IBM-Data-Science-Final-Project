import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

app = dash.Dash(__name__)

app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                
                                dcc.Dropdown(id='site-dropdown', 
                                            options = [
                                                {'label': 'All Sites', 'value': 'ALL'},
                                                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'}, 
                                                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}, 
                                                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'}, 
                                                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                                            ],
                                            value = 'ALL',
                                            placeholder = 'Select a Launch Site here',
                                            searchable = True),
                                html.Br(),

                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0', 2500: '2500', 5000:'5000', 7500:'7500', 10000:'10000'},
                                                value=[spacex_df['Payload Mass (kg)'].min(), spacex_df['Payload Mass (kg)'].max()]),

                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), 
              Input(component_id="payload-slider", component_property="value")] )

def get_pie_chart(entered_site, payload_range):
    filtered_df = spacex_df[spacex_df['Payload Mass (kg)'].apply(lambda x: x>=payload_range[0] and x<=payload_range[1])]
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Success rate of all launch sites')
        return fig
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        count_df = filtered_df['class'].value_counts().to_frame().reset_index()
        count_df.columns = ['class', 'count']
        fig = px.pie(count_df, values='count', 
        names='class', 
        title=f'Success rate of {entered_site} launch site')
        return fig

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), 
              Input(component_id="payload-slider", component_property="value")] )

def get_scatter_chart(entered_site, payload_range):
    filtered_df = spacex_df[spacex_df['Payload Mass (kg)'].apply(lambda x: x>=payload_range[0] and x<=payload_range[1])]
    if entered_site == 'ALL':   
        fig = px.scatter(filtered_df, y='class', 
        x='Payload Mass (kg)', color='Booster Version Category',
        title='Correlation between Payload and Success for all Launch Sites')
        return fig
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(filtered_df, y='class', 
        x='Payload Mass (kg)', color='Booster Version Category',
        title=f'Correlation between Payload and Success for all {entered_site} Launch Site')
        return fig


if __name__ == '__main__':
    app.run_server()
