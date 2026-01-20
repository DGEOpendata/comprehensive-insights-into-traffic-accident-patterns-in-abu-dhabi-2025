python
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Load dataset
url = "https://data.abudhabi.ae/traffic-accidents-2025.xlsx"
data = pd.read_excel(url)

# Create Dash app
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Traffic Accident Analysis Dashboard"),
    dcc.Dropdown(
        id='filter-city',
        options=[{'label': city, 'value': city} for city in data['city'].unique()],
        placeholder="Select a city"
    ),
    dcc.Graph(id='accident-map'),
    dcc.Graph(id='accident-cause-chart')
])

@app.callback(
    [Output('accident-map', 'figure'), 
     Output('accident-cause-chart', 'figure')],
    [Input('filter-city', 'value')]
)
def update_dashboard(selected_city):
    
    filtered_data = data if not selected_city else data[data['city'] == selected_city]
    
    # Map visualization
    map_fig = px.scatter_mapbox(filtered_data, 
                                lat='latitude', 
                                lon='longitude', 
                                color='type_of_accident', 
                                title="Accident Locations", 
                                mapbox_style="open-street-map")

    # Cause chart
    cause_fig = px.bar(filtered_data, 
                       x='cause', 
                       title="Accident Causes", 
                       color='cause')

    return map_fig, cause_fig

if __name__ == '__main__':
    app.run_server(debug=True)
