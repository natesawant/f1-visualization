import pandas as pd
import fastf1
from fastf1 import plotting
import plotly.express as px


def position_changes(year: int, gp: str):
    event = fastf1.get_event(year, gp)
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

        df[abb] = pd.Series(drv_laps["Position"].to_numpy())

    df["Lap Number"] = df.index + 1

    fig = px.line(
        df,
        x="Lap Number",
        y=df.columns,
        color_discrete_map=colors,
        title=f"Position Changes During {gp}",
    )

    fig.update_layout(
        font_color="rgba(255,255,255,255)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend_title_text="Driver",
    )

    fig.update_yaxes(title_text="Position")
    return fig
