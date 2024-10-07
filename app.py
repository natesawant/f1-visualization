from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

df = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv"
)

app = Dash()

app.layout = [
    html.H1(children="F1 Visualizations", style={"textAlign": "center"}),
    html.Div(
        [
            html.Div(
                [
                    html.Img(src=app.get_asset_url("old-f1-car.png")),
                    html.Img(src=app.get_asset_url("new-f1-car.png")),
                ],
                style={"display": "flex", "justify-content": "space-between"},
            ),
            dcc.Slider(
                1950,
                2024,
                1,
                value=2024,
                marks={1950: "1950", 1975: "1975", 2000: "2000", 2024: "2024"},
                tooltip={"placement": "bottom", "always_visible": True},
                id="year-selection",
            ),
        ],
        style={"padding": "5%"},
    ),
]

if __name__ == "__main__":
    app.run(debug=True)
