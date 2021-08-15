# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df["Payload Mass (kg)"].max()
min_payload = spacex_df["Payload Mass (kg)"].min()

# Create Launch Site Dropdown options list
launch_pie_chart_multi_select_dropdown_options = [
    {"label": "All Sites", "value": "All Sites"}
]
launch_sites = spacex_df["Launch Site"].unique()
for launch_site in launch_sites:
    launch_pie_chart_multi_select_dropdown_options.append(
        {"label": launch_site, "value": launch_site}
    )
launch_pie_chart_multi_select_dropdown_options_default = "All Sites"
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(
    children=[
        html.H1(
            "SpaceX Launch Records Dashboard",
            style={"textAlign": "center", "color": "#503D36", "font-size": 40},
        ),
        # TASK 1: Add a dropdown list to enable Launch Site selection
        # The default select value is for ALL sites
        dcc.Dropdown(
            id="pie_chart_multi_select_dropdown",
            options=launch_pie_chart_multi_select_dropdown_options,
            value=launch_pie_chart_multi_select_dropdown_options_default,
            multi=False,
            placeholder="Select a Launch Site here",
            style={"width": "80%", "font-size": "20px",
                   "text-align-last": "center"},
            searchable=False
        ),
        html.Br(),
        # TASK 2: Add a pie chart to show the total successful launches count for all sites
        # If a specific launch site was selected, show the Success vs. Failed counts for the site
        html.Div(dcc.Graph(id="pie_chart")),
        html.Br(),
        html.Hr(),
        html.Br(),
        html.P("Payload range (Kg):"),
        # TASK 3: Add a slider to select payload range
        dcc.RangeSlider(
            id="scatter_chart_range_slider",
            min=min_payload,
            max=max_payload,
            step=1000,
            value=[min_payload, max_payload]),
        # TASK 4: Add a scatter chart to show the correlation between payload and launch success
        html.Div(dcc.Graph(id="scatter_chart")),
    ]
)

# TASK 2:
# Add a callback function for `pie_chart_multi_select_dropdown` as input, `pie_chart` as output


@app.callback(
    Output(component_id="pie_chart",
           component_property="figure"),
    [Input(component_id="pie_chart_multi_select_dropdown",
           component_property="value")]
)
def update_graph(pie_chart_multi_select_dropdown):
    selected_launch_sites = launch_sites if pie_chart_multi_select_dropdown == "All Sites" else [
        pie_chart_multi_select_dropdown]
    dff = spacex_df
    dff = dff[dff["Launch Site"].isin(
        selected_launch_sites)]
    if len(selected_launch_sites) > 1:
        dff = spacex_df[spacex_df["class"] == 1]
    names = "Launch Site" if len(selected_launch_sites) > 1 else "class"
    title = "Total Success Launches by Site" if pie_chart_multi_select_dropdown == "All Sites" else f"Total Success Launches for Site {pie_chart_multi_select_dropdown}"
    pie_chart = px.pie(
        data_frame=dff,
        names=names,
        title=title
    )
    return pie_chart


# TASK 4:
# Add a callback function for`scatter_chart_range_slider` as inputs, `scatter_chart` as output
@app.callback(
    Output(component_id="scatter_chart",
           component_property="figure"),
    [Input(component_id="pie_chart_multi_select_dropdown",
           component_property="value"),
     Input(component_id="scatter_chart_range_slider",
           component_property="value")]
)
def update_graph(pie_chart_multi_select_dropdown, scatter_chart_range_slider):
    selected_launch_sites = launch_sites if pie_chart_multi_select_dropdown == "All Sites" else [
        pie_chart_multi_select_dropdown]
    dff = spacex_df
    dff = dff[dff["Launch Site"].isin(
        selected_launch_sites)]
    dff = dff[(dff["Payload Mass (kg)"] >= scatter_chart_range_slider[0]) & (
        dff["Payload Mass (kg)"] <= scatter_chart_range_slider[1])]
    title = "Correlation between Payload Size and Success for all Sites" if pie_chart_multi_select_dropdown == "All Sites" else f"Correlation between Payload Size and Success for Site {pie_chart_multi_select_dropdown}"
    scatter_chart = px.scatter(
        data_frame=dff,
        x="Payload Mass (kg)",
        y="class",
        title=title,
        color="Booster Version Category"
    )
    return scatter_chart


# Run the app
if __name__ == "__main__":
    app.run_server()
