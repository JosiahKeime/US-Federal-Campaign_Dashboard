import dash
from dash import dcc, html, Input, Output, callback, dash_table
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import utils.style_sheets as ss
import numpy as np

# state code to state name dictionaryu
us_states = {
    'AL': 'Alabama',
    'AK': 'Alaska',
    'AZ': 'Arizona',
    'AR': 'Arkansas',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'IA': 'Iowa',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'ME': 'Maine',
    'MD': 'Maryland',
    'MA': 'Massachusetts',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MS': 'Mississippi',
    'MO': 'Missouri',
    'MT': 'Montana',
    'NE': 'Nebraska',
    'NV': 'Nevada',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NY': 'New York',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VT': 'Vermont',
    'VA': 'Virginia',
    'WA': 'Washington',
    'WV': 'West Virginia',
    'WI': 'Wisconsin',
    'WY': 'Wyoming'
}

# party to color list
party_lst = [['Democrat',"#0a76f1"], ['Republican', "#EB0909"] ]

# a fucntion to filter dataframe on input attrubites and group sum metrics after filtering
# use for Map plot
def get_disbur_att(data=None, office=None, year=None, party='null', metric='Total_Disbursement'):
    if office: data = data[data['Cand_Office'] == office]
    if year:   data = data[data['Cand_Election_Yr'] == year]
    if party != 'null':  data = data[data['party'] == party]
    data = data[[metric, 'Cand_Office_St']].groupby(['Cand_Office_St']).sum().copy()
    data['Cand_Office_St'] = data.index
    data = data.reset_index(drop=True)
    return data

# a fucntion to filter dataframe on input attrubites and group sum metrics after filtering,
# used for bar plots
def get_all_fig_att(data=None, office=None, party='null', metric='Total_Disbursement'):
    if office: data = data[data['Cand_Office'] == office]

    if party != 'null':  data = data[data['party'] == party]
    data = data[[metric, 'Cand_Election_Yr']].groupby(['Cand_Election_Yr']).sum().copy()
    data['Cand_Election_Yr'] = data.index
    data = data.reset_index(drop=True)
    return data

# creates group party chart figure for display
def omni_party_graph(df_money, party_lst, metric, office=None):
    fig = go.Figure()
    
    for party_name, party_color in party_lst:
        df = get_all_fig_att(data=df_money, office=office, party=party_name, metric=metric)

        fig.add_trace(go.Bar(
            name= party_name,
            x=df['Cand_Election_Yr'],
            y=df[metric],
            marker_color=party_color,  
            text=[str(i) + 'B' for i in (df[metric].values/1e9).round(2)],
            textposition='outside',
            textfont=dict(size=100, weight='bold')
        ))

        fig.update_layout(
            title= '',
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis_title='Years',
            yaxis_title= metric.replace("_", " "),
            barmode='group',
            #height=500,
            #width=900,
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="top",
                y=1,
                xanchor="left",
                x=1.02
            ),
            yaxis=dict(
                gridcolor='lightgray',
                gridwidth=1,
                zeroline=True,
                zerolinecolor='lightgray',
                zerolinewidth=1
            ),
            xaxis=dict(
                tickangle=0
            ),
            plot_bgcolor='white',
            paper_bgcolor='white'
        )

    return fig


# Read in Data
df_money = pd.read_excel('data/omni_account_df.xlsx', index_col=0)
# get years in dataset
years = df_money['Cand_Election_Yr'].unique()

# get default filtered data for map graph
default_df = get_disbur_att(data=df_money)

# dict defining what rows to display in the data table
table_display_cols = [ {'name': 'Candidate', 'id':'Cand_Name' }, 
                       {'name': 'State', 'id':'Cand_Office_St' },
                        {'name': 'District', 'id':'Cand_Office_Dist' },
                       {'name': 'Party', 'id':'party' },
                        {'name': 'Office', 'id':'Cand_Office' },
                        {'name': 'Party', 'id':'Cand_Party_Affiliation' },
                        {'name': 'Year', 'id':'Cand_Election_Yr' },
                        {'name': 'Total Disbursement', 'id':'Total_Disbursement' },
                        {'name': 'Total Contribution', 'id':'Net_Contribution' },

                        ]
# dataframe for presidental graph
pres_df = df_money[df_money['Cand_Office'] == 'P']
pres_df = pres_df[pres_df['party'].isin(['Democrat', 'Republican'])]
pres_df = pres_df[pres_df['Cand_Election_Yr'].isin([2008, 2012, 2016, 2020, 2024])]


# Initialize the Dash app
app = dash.Dash(__name__)

########################## Dashboard Subcomponents - Level 2 ###############################
# map graph compononet
map_comp = html.Div([ dcc.Graph(id='us-map', style=ss.MAP_STYLE)], style=ss.MAP_CONTAINER)

# year drop down componont
year_selector = html.Div([
                html.Label("Select Year:", style=ss.LABEL_STYLE),
                dcc.Dropdown(
                    id='year-dropdown',
                    options=[{'label': str(year), 'value': year} for year in [2008, 2010, 2012, 
                                                                              2014, 2016, 2018, 
                                                                              2020, 2022, 2024]],
                    value=2024,
                    style=ss.DROPDOWN_STYLE
                )
            ], style=ss.CONTROL_GROUP)

# chamber drop down component
chamber_selector = html.Div([
                            html.Label("Select Chamber:", style=ss.LABEL_STYLE),
                            dcc.Dropdown(
                                id='office-dropdown',
                                options=[
                                    {'label': 'Senate', 'value': 'S'},
                                    {'label': 'House of Representatives', 'value': 'H'},
                                    {'label': 'White House', 'value': 'P'}
                                ],
                                value='S',
                                style=ss.DROPDOWN_STYLE
                                        )
                            ], style=ss.CONTROL_GROUP)

# Metric drop down component
metric_selector = html.Div([
                            html.Label("Select Metric:", style=ss.LABEL_STYLE),
                            dcc.Dropdown(
                                id='metric-dropdown',
                                options=[
                                    {'label': 'Total Disbursement', 'value': 'Total_Disbursement'},
                                    {'label': 'Individual Itemized Contribution', 'value': 'Individual_Itemized_Contribution'},
                                    {'label': 'Individual Unitemized Contribution', 'value': 'Individual_Unitemized_Contribution'},
                                    {'label': 'Individual Contribution', 'value': 'Individual_Contribution'},
                                    {'label': 'Total Contribution', 'value': 'Total_Contribution'},
                                    {'label': 'Operating Expenditure', 'value': 'Operating_Expenditure'},
                                    {'label': 'Net Contribution', 'value': 'Net_Contribution'},
                                    {'label': 'Net Operating Expenditure', 'value': 'Net_Operating_Expenditure'},
                                ],
                                value='Total_Disbursement',
                                clearable = False,
                                style=ss.DROPDOWN_STYLE
                                        )
                            ], style=ss.CONTROL_GROUP)
# drop down to enable the selection of states
state_selector = html.Div([
                            html.Label("Select State:", style=ss.LABEL_STYLE),
                            dcc.Dropdown(
                                id='state-dropdown',
                                options=[
                                    {'label': 'All', 'value': 'all'},
                                    {'label': 'Select from Map', 'value': 'states'},
                                ],
                                value='states',
                                style=ss.DROPDOWN_STYLE
                                        )
                            ], style=ss.CONTROL_GROUP)

# drop down to select type of graph to display in main container
graph_selector = html.Div([
                            html.Label("Select Graph Type:", style=ss.LABEL_STYLE),
                            dcc.Dropdown(
                                id='graph-dropdown',
                                options=[
                                    {'label': 'Bar Graph', 'value': 'bar'},
                                    {'label': 'Choropleth', 'value': 'chro'},
                                ],
                                value='chro',
                                style=ss.DROPDOWN_STYLE
                                        )
                            ], style=ss.CONTROL_GROUP)

########################## Dashboard Subcomponents - Level 1 ###############################
# Dashboard Subcomponents - Level 1
# control sidebar compoent for all the dropdown selectors
sidebar_comp = html.Div([
                    html.H3("Controls"),
                    chamber_selector, # Chamber selection
                    year_selector,  # Year selection
                    #party_selector,
                    metric_selector,
                    state_selector,
                    graph_selector
                ], style=ss.SIDEBAR_CONTAINER
                )

########################## Dashboard Components - Level 0 ###############################
# header banner
header_comp = html.Header([
                        html.H1("US Election Spending Dashboard", 
                                style=ss.HEADER_TITLE),
                        html.P("Campaign Finance Data for The United States' House, Senate, and Presidency ",
                            style=ss.HEADER_SUBTITLE)
                    ], style=ss.HEADER_CONTAINER)
# graph and sidebar container
main_comp = html.Div([
                        sidebar_comp,
                        map_comp,
                    ], style=ss.MAIN_CONTAINER)
# datatable component
data_table = dash_table.DataTable(
        id='state_info_table',
        columns=table_display_cols,
        data=df_money.to_dict('records'),
        style_table={
        'width': '90%',  # Table width as percentage of container
        'height': '70%',
        'margin': '0 auto',  # Center the table
        'overflowY': 'auto',
        'overflowX': 'auto'
        }, 
         fixed_rows={'headers': True},
        style_cell={
            'height': 'auto',
            'minWidth': 'auto', 'width': 'auto', 'maxWidth': '90px', 'minWidth':'50px',
            'whiteSpace': 'normal',
            'textAlign': 'left'
        },
        filter_action="native",  # Enable filtering
        sort_action="native",  # Enable sorting
    )
# container for datatable and state aneme
state_info_comp = html.Div([
        html.H3(id='info_title',children="State Details", style=ss.INFO_TITLE),
        html.Div(id='state-info', children="Click on a state to filter the data table"),
        data_table,   
    ], style=ss.INFO_CONTAINER)

# container for footer components
footer_comp = html.Footer([
        html.Hr(style=ss.FOOTER_HR),
        html.P("© 2025 U.S. Election Spending Dashboard | Built with Plotly Dash",
               style=ss.FOOTER_TEXT),
        html.P("Data from FEC All candidates dataset (https://www.fec.gov/campaign-finance-data/all-candidates-file-description/)",
               style=ss.FOOTER_SUBTEXT)
    ], style=ss.FOOTER_CONTAINER)

# Define the layout
app.layout = html.Div([
    # Header
    header_comp,
    # Main content container
    main_comp, 
    # State information section
    state_info_comp,
    # Footer
    footer_comp
], style={'height': '100%'})

########################## Callback functrions ###############################
# update Map from dropdowns
@app.callback(
    Output("us-map", "figure"),
    [Input("office-dropdown", "value"),
     Input('year-dropdown', 'value'),
     Input('metric-dropdown', 'value'),
     Input('graph-dropdown', 'value'),
    ])
def display_choropleth(office, year, metric, graph):

    global df_money
    global pres_df
    if metric is None: metric = 'Total_Disbursement'

    if graph == 'chro':
        if office == 'S' or office == 'H':
            df = get_disbur_att(data=df_money, office=office, year=year, metric=metric)
            fig = go.Figure(go.Choropleth(
                                z=df[metric],
                                locations=df["Cand_Office_St"],
                                locationmode= 'USA-states',
                                colorscale = 'Viridis',
                                colorbar_title = "Billion USD",
                                ))
            fig.update_layout(
                title_text = '',
                geo_scope='usa', # limite map scope to USA
                margin=dict(l=0, r=0, t=0, b=0) # set margins
            )
            fig.update_traces(
            zmin=df[metric].min(),  # Minimum value for color scale
            zmax=df[metric].max() # Maximum value for color scale
            )

        else: 
            fig = px.histogram(pres_df, x="Cand_Election_Yr", y= metric,
                color='party', 
                height=400,
                color_discrete_sequence=["blue", "red"]
                )
            fig.update_layout(
                title={'text': '',
                    'x': 0.5,
                    'xanchor': 'center'},
                xaxis_title='Years',
                yaxis_title= metric.replace("_", " "),
            )
            fig.update_xaxes(
                tickvals=[2008, 2012, 2016, 2020, 2024],  # Positions where ticks should appear
                ticktext=['2008', '2012', '2016', '2020', '2024']  # Optional: Custom labels
            )
    else:
        fig = omni_party_graph(df_money, party_lst, metric, office=office)

    return fig

# update state details from clicks on map graph
@callback(
    [Output('state_info_table', 'data'),
    Output('info_title','children')],
    [Input('us-map', 'clickData'),
     Input('office-dropdown', 'value'),
     Input('year-dropdown', 'value'),
     Input('state-dropdown', 'value')]
)
def display_state_info(clickData, office, year, bool_state):
    global us_states
    global table_display_cols
    global df_money
    title_txt = 'Data Table'

    if bool_state == 'all' and office != 'P':
        filtered_df = df_money[(df_money['Cand_Office'] == office)]

    elif office != 'P':
        filtered_df = df_money[(df_money['Cand_Office'] == office) & 
                                (df_money['Cand_Election_Yr']==year)]
        if clickData:
            loc = clickData['points'][0]['location']
            filtered_df = filtered_df[(filtered_df['Cand_Office_St'] == loc)]
    
            temp_txt = us_states[loc]+', '+ str(year) +' '

            if office == 'S':
                filtered_df['Cand_Office_Dist'] = 'Senate'
                title_txt = temp_txt + 'Senate'
            elif office == 'H':
                title_txt = temp_txt + 'House of Representive'
    else:
        filtered_df = df_money[(df_money['Cand_Office'] == office)]
        title_txt = 'Presidental Elections from 2008 to 2024'
        filtered_df.loc[:,'Cand_Office_Dist'] = np.nan

    return filtered_df.to_dict('records'), title_txt

# Run the app
if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=8050)