from functools import cache
from dash import Dash, html, dcc, callback, Output, Input, dash_table

import fastf1

from graphs import position_changes

app = Dash()

server = app.server

app.layout = [
    html.Div(
        [
            html.Div(
                [
                    html.Img(src=app.get_asset_url("F1.png"), style={"height": "44px"}),
                    html.H1(
                        children="ANALYTICS",
                        className="main-header",
                    ),
                ],
                style={
                    "display": "flex",
                    "flex-direction": "row",
                    "align-items": "center",
                    "gap": "32px",
                    "justify-content": "center",
                },
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Img(
                                src=app.get_asset_url("old-f1-car-white.png"),
                                draggable=False,
                            ),
                            html.Img(
                                src=app.get_asset_url("new-f1-car-white.png"),
                                draggable=False,
                            ),
                        ],
                        style={
                            "display": "flex",
                            "justify-content": "space-between",
                            "align-items": "center",
                        },
                    ),
                    dcc.Slider(
                        1950,
                        2024,
                        1,
                        value=2024,
                        marks={1950: "1950", 1975: "1975", 2000: "2000", 2024: "2024"},
                        tooltip={
                            "placement": "bottom",
                            "always_visible": True,
                        },
                        id="year-selection",
                    ),
                ],
                style={"padding": "2.5% 5%"},
            ),
            html.Div(
                [
                    dcc.Dropdown(id="gp-dropdown"),
                    dcc.Dropdown(
                        id="graph-type",
                        options=[
                            "Position Changes",
                            "Speed Over Race",
                            "Fastest Lap Speeds",
                        ],
                    ),
                    dcc.Loading(
                        dcc.Graph(id="gp-graph"), type="circle", color="#ff1e00"
                    ),
                ],
                style={
                    "display": "flex",
                    "flex-direction": "column",
                    "gap": "32px",
                    "padding": "10%",
                },
            ),
        ],
        style={"width": "100%", "height": "100vw"},
    )
]


@cache
@callback(
    Output("gp-dropdown", "options"),
    Output("gp-dropdown", "value"),
    Input("year-selection", "value"),
)
def update_schedule(value):
    schedule = fastf1.get_event_schedule(value)
    events = schedule["EventName"]
    schedule = schedule[["RoundNumber", "Country", "Location", "EventName"]]
    return events, events[0]


@cache
@callback(
    Output("gp-graph", "figure"),
    [
        Input("gp-dropdown", "value"),
        Input("year-selection", "value"),
    ],
)
def update_gp(value, year):
    fig = position_changes(year, value)

    return fig


if __name__ == "__main__":
    app.run(debug=True)
