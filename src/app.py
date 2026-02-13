from shiny import App, ui, render, reactive
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Loading the Data
df = pd.read_csv("data/raw/mars-weather.csv")
df["terrestrial_date"] = pd.to_datetime(df["terrestrial_date"])

# Reusable inline styles
CARD_STYLE = "background-color:#b78850; box-shadow: 2px 2px 8px #000000; border-radius:26px; padding:18px;"
FILTER_CARD_STYLE = "background-color:rgba(183,136,80,0.92); box-shadow: 0px 10px 22px rgba(0,0,0,0.28); border-radius:28px; padding:18px; border:1px solid rgba(255,255,255,0.18); min-height:150px;"
KPI_PILL_STYLE = "background-color:rgba(143,29,29,0.92); box-shadow: 0px 10px 22px rgba(0,0,0,0.28); border-radius:44px; padding:22px 18px; min-height:120px; display:flex; flex-direction:column; align-items:center; justify-content:center; border:1px solid rgba(255,255,255,0.18);"
PLOT_CARD_STYLE = "background-color:rgba(255,255,255,0.95); box-shadow: 0px 8px 18px rgba(0,0,0,0.18); border-radius:18px; padding:10px;"
CHART_SHELL_STYLE = "margin-top:18px; background-color:rgba(183,136,80,0.45); box-shadow: 0px 10px 22px rgba(0,0,0,0.24); border-radius:28px; padding:18px; border:1px solid rgba(255,255,255,0.18);"
CHART_SCROLL_STYLE = "max-height:560px; overflow-y:auto; padding-right:8px;"

BG_STYLE = """
min-height:100vh;
padding:24px 24px 40px 24px;
background-image:
  linear-gradient(rgba(245, 220, 170, 0.82), rgba(205, 165, 105, 0.62)),
  url('www/mars_bg.jpg');
background-size:cover;
background-position:center;
background-attachment:fixed;
"""

TITLE_STYLE = "text-align:center; color:#b22323; font-size:3.2em; font-weight:800; margin:6px 0 0 0; letter-spacing:0.5px;"
SUBTITLE_STYLE = "text-align:center; color:#3b2418; font-weight:400; font-size:1.05em; margin:0 0 16px 0;"
TOP_RULE_STYLE = "border:none; height:4px; background:rgba(178,35,35,0.35); border-radius:999px; margin:10px auto 18px auto; max-width:1200px;"

FILTER_H_STYLE = "color:#b22323; font-weight:700; font-size:1.25em; margin:0 0 10px 0;"
KPI_LABEL_STYLE = "color:white; font-weight:600; font-size:1.05em; text-align:center; margin:0 0 6px 0; letter-spacing:0.3px;"
KPI_VALUE_STYLE = "color:white; font-weight:700; font-size:1.8em; text-align:center; margin:0;"


DATE_CARD_WRAP_STYLE = FILTER_CARD_STYLE + "position:relative; padding-top:28px;"
DATE_BADGE_STYLE = """
position:absolute; top:-14px; right:18px;
background-color:#8f1d1d; color:white;
padding:14px 20px; border-radius:18px;
font-weight:900; font-size:2.0em;
box-shadow: 0px 10px 22px rgba(0,0,0,0.28);
"""


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
                ui.input_select(
                    "month",
                    None,
                    choices=sorted(df["month"].dropna().unique())
                ),
                style=FILTER_CARD_STYLE
            ),

            ui.card(
                ui.h5("Season Selector", style=FILTER_H_STYLE),
                ui.input_select(
                    "season",
                    None,
                    choices={
                        "Autumn (ls = 0)": 0,
                        "Winter (ls = 90)": 90,
                        "Spring (ls = 180)": 180,
                        "Summer (ls = 270)": 270
                    }
                ),
                style=FILTER_CARD_STYLE
            ),

            ui.card(
                ui.div("Terrestrial Date", style=DATE_BADGE_STYLE),
                ui.input_date_range(
                    "date_range",
                    None,
                    start=df["terrestrial_date"].min(),
                    end=df["terrestrial_date"].max()
                ),
                style=DATE_CARD_WRAP_STYLE
            ),
            col_widths=(4, 4, 4),
        ),

        # KPI row
        ui.layout_columns(
            ui.card(
                ui.p("Latest Sol KPI", style=KPI_LABEL_STYLE),
                ui.div(ui.output_text("latest_sol"), style=KPI_VALUE_STYLE),
                style=KPI_PILL_STYLE
            ),
            ui.card(
                ui.p("AVG Min Temp KPI", style=KPI_LABEL_STYLE),
                ui.div(ui.output_text("avg_min"), style=KPI_VALUE_STYLE),
                style=KPI_PILL_STYLE
            ),
            ui.card(
                ui.p("AVG Max Temp KPI", style=KPI_LABEL_STYLE),
                ui.div(ui.output_text("avg_max"), style=KPI_VALUE_STYLE),
                style=KPI_PILL_STYLE
            ),
            ui.card(
                ui.p("Avg Pressure KPI", style=KPI_LABEL_STYLE),
                ui.div(ui.output_text("avg_pressure"), style=KPI_VALUE_STYLE),
                style=KPI_PILL_STYLE
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

        # Filter by the month
        if input.month():
            filtered = filtered[filtered["month"] == input.month()]

        # Filter by the season
        season_map = {
            "Autumn (ls = 0)": 0,
            "Winter (ls = 90)": 90,
            "Spring (ls = 180)": 180,
            "Summer (ls = 270)": 270
        }
        if input.season():
            filtered = filtered[filtered["ls"] == season_map[input.season()]]

        # Filter by date range
        if input.date_range():
            start, end = input.date_range()
            filtered = filtered[
                (filtered["terrestrial_date"] >= pd.to_datetime(start)) &
                (filtered["terrestrial_date"] <= pd.to_datetime(end))
            ]

        return filtered

    # KPI Outputs
    @output
    @render.text
    def latest_sol():
        filtered = filtered_df()
        return str(filtered["sol"].max()) if not filtered.empty else "N/A"

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
