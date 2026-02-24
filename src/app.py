from shiny import App, ui, render, reactive
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Loading the Data
df = pd.read_csv("data/raw/mars-weather.csv")
df["terrestrial_date"] = pd.to_datetime(df["terrestrial_date"])

SEASON_MAP = {
    "Autumn": (0, 90),
    "Winter": (90, 180),
    "Spring": (180, 270),
    "Summer": (270, 360),
}

RECENCY_MAP = {
    "Last 6 Months": pd.DateOffset(months=6),
    "Last 1 Year":   pd.DateOffset(years=1),
    "Last 2 Years":  pd.DateOffset(years=2),
    "Last 3 Years":  pd.DateOffset(years=3),
    "Last 5 Years":  pd.DateOffset(years=5),
}

# Reusable inline styles
# Produced with the Help of Generative AI
CARD_STYLE = "background-color:#b78850; box-shadow: 2px 2px 8px #000000; border-radius:26px; padding:18px;"
FILTER_CARD_STYLE = "background-color:#98182E; box-shadow: 0px 10px 22px rgba(0,0,0,0.28); border-radius:20px; padding:6px 10px; border:1px solid rgba(255,255,255,0.18);"
KPI_PILL_STYLE = "background-color:#B82020; box-shadow: 0px 10px 22px rgba(0,0,0,0.28); border-radius:44px; padding:10px 12px; min-height:70px; display:flex; flex-direction:column; align-items:center; justify-content:center; border:1px solid rgba(255,255,255,0.18);"
PLOT_CARD_STYLE = "background-color:#FFAB26; box-shadow: 0px 8px 18px rgba(0,0,0,0.18); border-radius:18px; padding:10px;"
CHART_SHELL_STYLE = "margin-top:18px; background-color:rgba(183,136,80,0.45); box-shadow: 0px 10px 22px rgba(0,0,0,0.24); border-radius:28px; padding:18px; border:1px solid rgba(255,255,255,0.18);"
CHART_SCROLL_STYLE = "max-height:560px; overflow-y:auto; padding-right:8px;"

BG_STYLE = """
min-height:100vh;
padding:24px 24px 40px 24px;
background-image:
  linear-gradient(#FE7701, rgba(205, 165, 105, 0.62)),
  url('www/mars_bg.jpg');
background-size:cover;
background-position:center;
background-attachment:fixed;
"""

TITLE_STYLE = "text-align:center; color:#B82020; font-size:3.2em; font-weight:800; margin:6px 0 0 0; letter-spacing:0.5px;"
SUBTITLE_STYLE = "text-align:center; color:#FFFFFF; font-weight:400; font-size:1.5em; margin:0 0 16px 0;"
TOP_RULE_STYLE = "border:none; height:4px; background:rgba(178,35,35,0.35); border-radius:999px; margin:10px auto 18px auto; max-width:1200px;"

FILTER_H_STYLE = "text-align:center; color:#FFFFFF; font-weight:700; font-size:1.5em; margin:0 0 4px 0;"
KPI_LABEL_STYLE = "color:white; font-weight:600; font-size:1.2em; text-align:center; margin:0 0 2px 0; letter-spacing:0.3px;"
KPI_VALUE_STYLE = (
    "color:white; font-weight:700; font-size:2.0em; text-align:center; margin:0;"
)


DATE_CARD_WRAP_STYLE = FILTER_CARD_STYLE + "position:relative; padding-top:6px;"


# UI Section
app_ui = ui.page_fluid(
    ui.div(
        {"style": BG_STYLE},
        ui.h1("MarsCast", style=TITLE_STYLE),
        ui.h4("Weather Patterns from The Red Planet", style=SUBTITLE_STYLE),
        ui.tags.hr(style=TOP_RULE_STYLE),
        # Filters
        ui.layout_columns(
            ui.card(
                ui.h5("Martian Month", style=FILTER_H_STYLE),
                ui.div(
                    ui.input_select(
                        "month",
                        None,
                        choices=["All"] + [f"Month {n}" for n in range(1, 13)],
                        selected="All",
                    ),
                    style="display:flex; justify-content:center;",
                ),
                style=FILTER_CARD_STYLE,
            ),
            ui.card(
                ui.h5("Season Selector", style=FILTER_H_STYLE),
                ui.div(
                    ui.input_select(
                        "season",
                        None,
                        choices=["All", "Spring", "Summer", "Autumn", "Winter"],
                        selected="All",
                    ),
                    style="display:flex; justify-content:center;",
                ),
                style=FILTER_CARD_STYLE,
            ),
            ui.card(
                ui.div("Terrestrial Date", style=FILTER_H_STYLE),
                ui.div(
                    ui.input_date_range(
                        "date_range",
                        None,
                        start=df["terrestrial_date"].min(),
                        end=df["terrestrial_date"].max(),
                    ),
                    style="display:flex; justify-content:center;",
                ),
                style=DATE_CARD_WRAP_STYLE,
            ),
            ui.card(
                ui.h5("Recent Data", style=FILTER_H_STYLE),
                ui.div(
                    ui.input_select(
                        "recency",
                        None,
                        choices=["All"] + list(RECENCY_MAP.keys()),
                        selected="All",
                    ),
                    style="display:flex; justify-content:center;",
                ),
                style=FILTER_CARD_STYLE,
            ),
            col_widths=(3, 3, 3, 3),
        ),
        # KPI row
        ui.layout_columns(
            ui.card(
                ui.p("AVG Min Temp (C)", style=KPI_LABEL_STYLE),
                ui.div(ui.output_text("avg_min"), style=KPI_VALUE_STYLE),
                style=KPI_PILL_STYLE,
            ),
            ui.card(
                ui.p("AVG Max Temp (C)", style=KPI_LABEL_STYLE),
                ui.div(ui.output_text("avg_max"), style=KPI_VALUE_STYLE),
                style=KPI_PILL_STYLE,
            ),
            ui.card(
                ui.p("AVG Pressure (Pa)", style=KPI_LABEL_STYLE),
                ui.div(ui.output_text("avg_pressure"), style=KPI_VALUE_STYLE),
                style=KPI_PILL_STYLE,
            ),
            ui.card(
                ui.p("STD Pressure (Pa)", style=KPI_LABEL_STYLE),
                ui.div(ui.output_text("std_pressure"), style=KPI_VALUE_STYLE),
                style=KPI_PILL_STYLE,
            ),
            col_widths=(3, 3, 3, 3),
        ),
        # Charts section with scroll container
        ui.div(
            {"style": CHART_SHELL_STYLE},
            ui.div(
                {"style": CHART_SCROLL_STYLE},
                ui.layout_columns(
                    ui.card(ui.output_plot("sol_plot"), style=PLOT_CARD_STYLE),
                    ui.card(ui.output_plot("ls_plot"), style=PLOT_CARD_STYLE),
                    col_widths=(6, 6),
                ),
                ui.layout_columns(
                    ui.card(ui.output_plot("min_temp_plot"), style=PLOT_CARD_STYLE),
                    ui.card(ui.output_plot("pressure_plot"), style=PLOT_CARD_STYLE),
                    col_widths=(6, 6),
                ),
            ),
        ),
    )
)


# Server
def server(input, output, session):

    @reactive.calc
    def filtered_df():
        filtered = df.copy()

        if input.month() != "All":
            filtered = filtered[filtered["month"] == input.month()]

        if input.season() != "All":
            lo, hi = SEASON_MAP[input.season()]
            filtered = filtered[(filtered["ls"] >= lo) & (filtered["ls"] < hi)]

        start, end = sorted(input.date_range())
        filtered = filtered[
            (filtered["terrestrial_date"] >= pd.to_datetime(start))
            & (filtered["terrestrial_date"] <= pd.to_datetime(end))
        ]

        if input.recency() != "All":
            cutoff = filtered["terrestrial_date"].max() - RECENCY_MAP[input.recency()]
            filtered = filtered[filtered["terrestrial_date"] >= cutoff]

        return filtered

    # KPI Outputs
    @output
    @render.text
    def avg_min():
        filtered = filtered_df()
        return f"{filtered['min_temp'].mean():.2f}" if not filtered.empty else "N/A"

    @output
    @render.text
    def avg_max():
        filtered = filtered_df()
        return f"{filtered['max_temp'].mean():.2f}" if not filtered.empty else "N/A"

    @output
    @render.text
    def avg_pressure():
        filtered = filtered_df()
        return f"{filtered['pressure'].mean():.2f}" if not filtered.empty else "N/A"

    @output
    @render.text
    def std_pressure():
        filtered = filtered_df()
        return f"{filtered['pressure'].std():.2f}" if not filtered.empty else "N/A"

    @output
    @render.plot
    def sol_plot():
        filtered = filtered_df()
        plt.figure()
        plt.hist(filtered["sol"], bins=20)
        plt.title("Distribution of Sol")
        plt.tight_layout()

    @output
    @render.plot
    def ls_plot():
        filtered = filtered_df()
        plt.figure()
        plt.hist(filtered["ls"], bins=20)
        plt.title("Distribution of Solar Longitude (ls)")
        plt.tight_layout()

    @output
    @render.plot
    def min_temp_plot():
        filtered = filtered_df()
        plt.figure()
        plt.hist(filtered["min_temp"], bins=20)
        plt.title("Distribution of Minimum Temperature")
        plt.tight_layout()

    @output
    @render.plot
    def pressure_plot():
        filtered = filtered_df()
        plt.figure()
        plt.hist(filtered["pressure"], bins=20)
        plt.title("Distribution of Pressure")
        plt.tight_layout()


app = App(app_ui, server)
