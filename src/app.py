from shiny import App, ui, render, reactive
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

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
    "Last Month": pd.DateOffset(months=1),
    "Last 2 Months":   pd.DateOffset(months=2),
    "Last 6 Months":  pd.DateOffset(months=6),
    "Last 1 Year":  pd.DateOffset(years=1),
    "Last 2 Years":  pd.DateOffset(years=2),
}

# Reusable inline styles
# Produced with the Help of Generative AI
CARD_STYLE = "background-color:rgba(20,6,6,0.82); box-shadow: 2px 2px 8px #000000; border-radius:26px; padding:18px;"
FILTER_CARD_STYLE = "background-color:rgba(18,5,5,0.78); box-shadow: 0px 8px 24px rgba(0,0,0,0.55); border-radius:20px; padding:6px 10px; border:1px solid rgba(210,85,30,0.45); backdrop-filter:blur(6px);"
KPI_PILL_STYLE = "background-color:rgba(10,2,2,0.85); box-shadow: 0px 8px 24px rgba(0,0,0,0.55); border-radius:44px; padding:10px 12px; min-height:70px; display:flex; flex-direction:column; align-items:center; justify-content:center; border:1px solid rgba(210,85,30,0.5); backdrop-filter:blur(6px);"
PLOT_CARD_STYLE = "background-color:rgba(14,4,4,0.82); box-shadow: 0px 8px 24px rgba(0,0,0,0.55); border-radius:18px; padding:8px; border:1px solid rgba(210,85,30,0.4); backdrop-filter:blur(6px);"
CHART_SHELL_STYLE = "margin-top:18px; background-color:rgba(10,2,2,0.60); box-shadow: 0px 10px 22px rgba(0,0,0,0.4); border-radius:28px; padding:18px; border:1px solid rgba(210,85,30,0.35); backdrop-filter:blur(4px);"
CHART_SCROLL_STYLE = "max-height:560px; overflow-y:auto; padding-right:8px;"

BG_STYLE = """
min-height:100vh;
padding:24px 24px 40px 24px;
background-image: url('/mars_bg.png');
background-size:cover;
background-position:center;
background-attachment:fixed;
"""

TITLE_STYLE = "text-align:center; color:#FFFFFF; font-size:3.6em; font-weight:900; margin:6px 0 0 0; letter-spacing:1px; text-shadow: 0 2px 12px rgba(0,0,0,0.9), 0 0 40px rgba(220,80,20,0.7);"
SUBTITLE_STYLE = "text-align:center; color:rgba(255,205,160,0.95); font-weight:400; font-size:1.3em; margin:0 0 16px 0; text-shadow: 0 1px 8px rgba(0,0,0,0.8); letter-spacing:0.3px;"
TOP_RULE_STYLE = "border:none; height:1px; background:linear-gradient(to right, transparent, rgba(210,85,30,0.7), transparent); border-radius:999px; margin:10px auto 18px auto; max-width:1200px;"

RESET_BUTTON_STYLE = "color:#FFAD70; font-weight:600; font-size:1em"
FILTER_H_STYLE = "text-align:center; color:#FFAD70; font-weight:700; font-size:0.95em; margin:0 0 4px 0; text-transform:uppercase; letter-spacing:0.8px;"
KPI_LABEL_STYLE = "color:#FFAD70; font-weight:600; font-size:0.82em; text-align:center; margin:0 0 2px 0; letter-spacing:0.6px; text-transform:uppercase;"
KPI_VALUE_STYLE = (
    "color:#FFE8D0; font-weight:700; font-size:1.7em; text-align:center; margin:0; text-shadow: 0 1px 6px rgba(0,0,0,0.6);"
)


DATE_CARD_WRAP_STYLE = FILTER_CARD_STYLE + "position:relative; padding-top:6px;"


# UI Section
app_ui = ui.page_fluid(
    ui.div(
        {"style": BG_STYLE},
        ui.h1("MarsCast", style=TITLE_STYLE),
        ui.h4("Weather Patterns from The Red Planet", style=SUBTITLE_STYLE),
        ui.tags.hr(style=TOP_RULE_STYLE),
        # Reset Button
        ui.div(
            ui.input_action_button(
                "reset_all",
                "Reset",
                class_="btn btn-sm btn-outline-secondary",
                style=RESET_BUTTON_STYLE
            ),
            style="display:flex; justify-content:flex-end; margin-bottom:12px;"
        ),
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
                    ui.card(ui.output_plot("pressure_min_temp_plot"), style=PLOT_CARD_STYLE),
                    ui.card(ui.output_plot("pressure_max_temp_plot"), style=PLOT_CARD_STYLE),
                    col_widths=(6, 6),
                ),
                ui.card(ui.output_plot("temp_series"), style=PLOT_CARD_STYLE),
                ui.card(ui.output_plot("pressure_series"), style=PLOT_CARD_STYLE),
            ),
        ),
    )
)


# Server
def server(input, output, session):

    def apply_filters(exclude=None):
        """Apply all active filters except the one named in `exclude`."""
        filtered = df.copy()

        if exclude != "month" and input.month() != "All":
            filtered = filtered[filtered["month"] == input.month()]

        if exclude != "season" and input.season() != "All":
            lo, hi = SEASON_MAP[input.season()]
            filtered = filtered[(filtered["ls"] >= lo) & (filtered["ls"] < hi)]

        if exclude != "date_range":
            start, end = sorted(input.date_range())
            filtered = filtered[
                (filtered["terrestrial_date"] >= pd.to_datetime(start))
                & (filtered["terrestrial_date"] <= pd.to_datetime(end))
            ]

        if exclude != "recency" and input.recency() != "All":
            cutoff = filtered["terrestrial_date"].max() - RECENCY_MAP[input.recency()]
            filtered = filtered[filtered["terrestrial_date"] >= cutoff]


        return filtered

    @reactive.calc
    def filtered_df():
        return apply_filters()
    
    @reactive.calc
    def series_filtered():
        filtered = filtered_df()
        return    (
            filtered.set_index("terrestrial_date")[["max_temp", "min_temp", "pressure"]]
            .resample("1D").mean().reset_index()
            )


    # --- Cascading filter updates ---

    @reactive.effect
    def _update_month_choices():
        ctx = apply_filters(exclude="month")
        present = set(ctx["month"].unique())
        valid = ["All"] + [f"Month {n}" for n in range(1, 13) if f"Month {n}" in present]
        selected = input.month() if input.month() in valid else "All"
        ui.update_select("month", choices=valid, selected=selected)

    @reactive.effect
    def _update_season_choices():
        ctx = apply_filters(exclude="season")
        valid = ["All"] + [
            name for name, (lo, hi) in SEASON_MAP.items()
            if ((ctx["ls"] >= lo) & (ctx["ls"] < hi)).any()
        ]
        selected = input.season() if input.season() in valid else "All"
        ui.update_select("season", choices=valid, selected=selected)

    @reactive.effect
    def _update_recency_choices():
        ctx = apply_filters(exclude="recency")
        if ctx.empty:
            valid = ["All"]
        else:
            max_date = ctx["terrestrial_date"].max()
            valid = ["All"] + [
                name for name, offset in RECENCY_MAP.items()
                if (ctx["terrestrial_date"] >= max_date - offset).any()
            ]
        selected = input.recency() if input.recency() in valid else "All"
        ui.update_select("recency", choices=valid, selected=selected)
    
    @reactive.effect
    @reactive.event(input.reset_all)
    def _reset_filters():
        ui.update_select("month", selected="All")
        ui.update_select("season", selected="All")
        ui.update_select("recency", selected="All")
        ui.update_date_range("date_range",
                             start=df["terrestrial_date"].min(),
                             end=df["terrestrial_date"].max()
                            )

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
    def temp_series():
        filtered = series_filtered()
        plt.figure(figsize=(10, 6))
        plt.plot(filtered["terrestrial_date"], filtered["min_temp"], label='Minimum Temperature', color='#FFAD70')
        plt.plot(filtered["terrestrial_date"], filtered["max_temp"], label='Maximum temperature', color='#C1440E')
        plt.ylabel("Temperature (C)")
        plt.xlabel("Terrestrial date")
        plt.title("Daily average temperatures")
        plt.xticks(rotation=90)
        plt.plot(legend=False)


    @output
    @render.plot
    def pressure_series():
        filtered = series_filtered()
        plt.figure(figsize=(10, 6))
        plt.plot(filtered["terrestrial_date"], filtered["pressure"], color = '#FFAD70')
        plt.ylabel("Air Pressure (Pa)")
        plt.xlabel("Terrestrial date")
        plt.title("Daily average air pressure")
        plt.xticks(rotation=90)
        plt.plot(legend=False)

    @output
    @render.plot
    def pressure_min_temp_plot():
        filtered = filtered_df()
        plt.figure()
        sns.scatterplot(x = "pressure", y="min_temp", data=filtered, color = '#FFAD70')
        plt.ylabel("Temperature (C)")
        plt.xlabel("Air Pressure (Pa)")
        plt.title("Air Pressure and Minimum Temperature")
        plt.xticks(rotation=90)
        plt.plot(legend=False)
    
    @output
    @render.plot
    def pressure_max_temp_plot():
        filtered = filtered_df()
        plt.figure()
        sns.scatterplot(x = "pressure", y="max_temp", data=filtered, color = '#C1440E')
        plt.ylabel("Temperature (C)")
        plt.xlabel("Air Pressure (Pa)")
        plt.title("Air Pressure and Maximum Temperature")
        plt.xticks(rotation=90)
        plt.plot(legend=False)


app = App(app_ui, server, static_assets=Path(__file__).parent / "www")
