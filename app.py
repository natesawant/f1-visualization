from functools import cache
from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px
import pandas as pd

import fastf1
from fastf1 import plotting

app = Dash()

server = app.server

df = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv"
)


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
                    dcc.Loading(
                        dcc.Graph(id="gp-graph"),
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
    print(value, year)
    event = fastf1.get_event(year, value)
    session = event.get_race()
    session.load(telemetry=False, weather=False)

    df = pd.DataFrame()
    colors = {}

    try:
        laps = session.laps
    except:
        return

    for drv in session.drivers:
        drv_laps = laps.pick_driver(drv)

        abb = drv_laps["Driver"].iloc[0]
        colors[abb] = plotting.get_driver_color(abb, session)

        # df["LapNumber"] = drv_laps["LapNumber"].to_numpy()
        df[abb] = pd.Series(drv_laps["Position"].to_numpy())

        # ax.plot(drv_laps["LapNumber"], drv_laps["Position"], label=abb, color=color)

    df["LapNumber"] = df.index

    fig = px.line(
        df,
        x="LapNumber",
        y=df.columns,
        color_discrete_map=colors,
        title=f"Position Changes During {value}",
    )

    fig.update_layout(
        font_color="rgba(255,255,255,255)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return fig


if __name__ == "__main__":
    app.run(debug=True)
