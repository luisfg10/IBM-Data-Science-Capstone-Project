# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites

                                #  label is what the user sees, value is what´s passed into the callback
                                #  https://dash.plotly.com/dash-core-components/dropdown

                                # --- --- complete --- ---
                                dcc.Dropdown(id='site-dropdown',
                                  options=[{'label': 'All Sites', 'value': 'ALL'},
                                  {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'}, 
                                  {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                  {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                  {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}],
                                   value='ALL',
                                    placeholder="Please select a Launch Site",
                                    searchable=True      
                                  ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                # this needs a callback, as well as the right code for the chart
                                #  callback goes outside the app.layout tree
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                            min=0, max=10000, step=1000,
                                            value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        data=spacex_df
        
        fig = px.pie(data, values='class', 
        names='Launch Site', 
        title='Successful Launches by Site')
        return fig
    else:
        #  names are the partitions of the pie, values is the column that is summed up
        #  filter the dataframe by the required site
        data = spacex_df[spacex_df['Launch Site']==entered_site]
        # group by success or failure, and count each ocurrence
        data=data.groupby("class")["Launch Site"].count().reset_index()
        #  rename count column to a more appropriate name
        data.rename(columns={"Launch Site": "Total Count"}, inplace=True)
        # placeholder for site name
        site="Total Successful Launches for "+str(entered_site)
        # initiate the pie chart
        fig = px.pie(data, values='Total Count', 
        names='class', 
        title=site
                    )
        return fig
        
        
        # return the outcomes piechart for a selected site

        

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), 
              Input(component_id="payload-slider", component_property="value")])

#  the intuition behind these functions is that the inputs don´t need the same name as the ids in the callback
# inputs. However, they do need the same order
def get_sct_chart(entered_site, slider_range):
    if entered_site == 'ALL':
        low, high = slider_range
        # apply mask to the slider limits
        # lower limit
        data = spacex_df[spacex_df['Payload Mass (kg)']>low]
        # upper limit
        data = data[data['Payload Mass (kg)']<high]
        fig = px.scatter(data, x="Payload Mass (kg)", 
        y="class", color="Booster Version Category",
        title="Payload Mass- Launch Success Relation for all Sites")
        return fig
    else:
        data = spacex_df[spacex_df['Launch Site']==entered_site]
        low, high = slider_range
        # lower limit
        data = spacex_df[spacex_df['Payload Mass (kg)']>low]
        # upper limit
        data = data[data['Payload Mass (kg)']<high]
        # placeholder for site name
        site="Payload Mass- Success Relation for "+str(entered_site)
        fig = px.scatter(data, x="Payload Mass (kg)", y="class", 
        color="Booster Version Category",
        title=site)
                    
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
