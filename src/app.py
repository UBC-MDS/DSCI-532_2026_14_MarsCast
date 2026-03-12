from shiny import App, ui, render, reactive
from pathlib import Path
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from dotenv import load_dotenv
import querychat
import chatlas
import shinychat
import narwhals.stable.v1 as nw
import os
from faicons import icon_svg
import ibis
from ibis import _

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "rag"))
from retriever import retrieve_context


AI_AGENT = "claude-haiku-4-5"
SEASON_MAP = {
    "Autumn": (0, 90),
    "Winter": (90, 180),
    "Spring": (180, 270),
    "Summer": (270, 360),
}
RECENCY_MAP = {
    "Last Month": pd.DateOffset(months=1),
    "Last 2 Months": pd.DateOffset(months=2),
    "Last 6 Months": pd.DateOffset(months=6),
    "Last 1 Year": pd.DateOffset(years=1),
    "Last 2 Years": pd.DateOffset(years=2),
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
KPI_VALUE_STYLE = "color:#FFE8D0; font-weight:700; font-size:1.7em; text-align:center; margin:0; text-shadow: 0 1px 6px rgba(0,0,0,0.6);"
KPI_CAPTION_STYLE = "color:rgba(255,205,160,0.8); font-size:0.7em; font-weight:300; margin-top:2px; letter-spacing:0.3px; text-align:center;"
DATE_CARD_WRAP_STYLE = FILTER_CARD_STYLE + "position:relative; padding-top:6px;"
DOWNLOAD_BUTTON_STYLE = (
    KPI_PILL_STYLE
    + "color:#FFAD70; font-weight:600; font-size:0.9em; border:1px solid rgba(210,85,30,0.5);"
)
USE_COLS = [
    "terrestrial_date",
    "sol",
    "ls",
    "month",
    "min_temp",
    "max_temp",
    "pressure",
]
SYSTEM_PROMPT = Path(__file__).parent / "prompts" / "system_prompt.md"
DATA_DESCRIPTION = Path(__file__).parent / "prompts" / "initial_data_description.md"
GREETING = (Path(__file__).parent / "prompts" / "greeting_prompt.txt").read_text()

load_dotenv()
anthropic_key = os.getenv("ANTHROPIC_API_KEY")

# Loading the Data
con = ibis.duckdb.connect()
df = con.read_parquet("data/processed/mars-weather.parquet")

qc = querychat.QueryChat(
    df,
    "mars_weather_data",
    greeting=GREETING,
    data_description=DATA_DESCRIPTION,
    extra_instructions=SYSTEM_PROMPT,
    client=chatlas.ChatAnthropic(api_key=anthropic_key, model=AI_AGENT),
)

# Default: the most recent month(Feb, Terrestrial Calendar)
latest_date = df.terrestrial_date.max().execute()
latest_martian_month = df.filter(_.terrestrial_date == latest_date).select(_.month).limit(1).execute().iloc[0,0]
latest_ls = df.filter(_.terrestrial_date == latest_date).select(_.ls).limit(1).execute().iloc[0,0]
latest_season = next((name for name, (lo, hi) in SEASON_MAP.items() if lo <= latest_ls < hi), "All")

# Adapted from DSCI 523 lecture 6 slides
def compare(current, baseline):
    """
    Compare current vs baseline, return icon and bagde text
    """
    # guard: can't compute a meaningful average
    if baseline is None or baseline == 0 or pd.isna(current) or pd.isna(baseline):
        return dict(icon="circle-minus", badge="no data")

    # percentage change relative to baseline
    pct = (current - baseline) / abs(baseline) * 100

    # badge sign and text
    sign = "+" if pct >= 0 else ""
    diff = current - baseline
    badge = f"{sign}{diff:.1f} ({sign}{pct:.1f}%) vs last year"

    # direction icon
    if diff > 0:
        icon = "arrow-trend-up"
    elif diff < 0:
        icon = "arrow-trend-down"
    else:
        icon = "minus"
    # icon = "arrow-trend-up" if pct > 0 else "arrow-trend-down"

    return dict(icon=icon, badge=badge)


def kpi_caption(cmp):
    """Return the badge text under the KPI number."""
    return ui.HTML(f'<strong style="opacity:0.9">{cmp["badge"]}</strong>')

qc = querychat.QueryChat(
    df.execute(),
    "mars_weather_data",
    greeting=GREETING,
    data_description=DATA_DESCRIPTION,
    extra_instructions=SYSTEM_PROMPT,
    client=chatlas.ChatAnthropic(api_key=anthropic_key, model=AI_AGENT),
)

# UI Section
app_ui = ui.page_navbar(
    ui.head_content(
        ui.tags.style(
            """
            .bslib-sidebar-layout > .sidebar {
                background-color: rgba(12, 3, 3, 0.88) !important;
                border-right: 1px solid rgba(210, 85, 30, 0.5) !important;
                backdrop-filter: blur(8px);
            }
            .bslib-sidebar-layout > .sidebar .sidebar-title {
                color: #FFAD70 !important;
                font-weight: 700;
                border-bottom: 1px solid rgba(210, 85, 30, 0.35);
                padding-bottom: 8px;
            }
            .bslib-sidebar-layout > .main {
                background-color: rgba(8, 2, 2, 0.75) !important;
                backdrop-filter: blur(6px);
            }
            .querychat shiny-chat-message {
                color: #FFE8D0 !important;
            }
            .querychat shiny-chat-user-message {
                background-color: rgba(180, 60, 10, 0.75) !important;
                color: #FFE8D0 !important;
                border-radius: 14px !important;
                border: 1px solid rgba(210, 85, 30, 0.5) !important;
            }
            .querychat .suggestion, .querychat a.suggestion {
                color: #FFAD70 !important;
                font-weight: 600;
            }
            .querychat shiny-chat-input textarea,
            .querychat shiny-chat-input input {
                background-color: rgba(20, 5, 3, 0.90) !important;
                color: #FFE8D0 !important;
                border: 1px solid rgba(210, 85, 30, 0.6) !important;
                border-radius: 12px !important;
            }
            .querychat shiny-chat-input textarea::placeholder,
            .querychat shiny-chat-input input::placeholder {
                color: rgba(255, 180, 120, 0.5) !important;
            }
            .querychat shiny-chat-input button {
                background-color: rgba(180, 60, 10, 0.8) !important;
                color: #FFE8D0 !important;
                border-radius: 10px !important;
            }
        """
        )
    ),
    *[
        # Dashboard
        ui.nav_panel(
            "Dashboard",
            ui.page_fluid(
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
                            style=RESET_BUTTON_STYLE,
                        ),
                        style="display:flex; justify-content:flex-end; margin-bottom:12px;",
                    ),
                    # Filters
                    ui.layout_columns(
                        ui.card(
                            ui.h5("Martian Month", style=FILTER_H_STYLE),
                            ui.div(
                                ui.input_select(
                                    "month",
                                    None,
                                    choices=["All"]
                                    + [f"Month {n}" for n in range(1, 13)],
                                    selected=latest_martian_month,
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
                                    choices=[
                                        "All",
                                        "Spring",
                                        "Summer",
                                        "Autumn",
                                        "Winter",
                                    ],
                                    selected=latest_season,
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
                                    start=latest_date.replace(day=1),
                                    end=latest_date,
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
                            ui.p("Avg Min Temperature", style=KPI_LABEL_STYLE),
                            ui.div(ui.output_ui("avg_min"), style=KPI_VALUE_STYLE),
                            style=KPI_PILL_STYLE,
                        ),
                        ui.card(
                            ui.p("Avg Max Temperature", style=KPI_LABEL_STYLE),
                            ui.div(ui.output_ui("avg_max"), style=KPI_VALUE_STYLE),
                            style=KPI_PILL_STYLE,
                        ),
                        ui.card(
                            ui.p("Avg Air Pressure", style=KPI_LABEL_STYLE),
                            ui.div(ui.output_ui("avg_pressure"), style=KPI_VALUE_STYLE),
                            style=KPI_PILL_STYLE,
                        ),
                        ui.card(
                            ui.p(
                                "Pressure Variability (Std Dev)", style=KPI_LABEL_STYLE
                            ),
                            ui.div(
                                ui.output_text("std_pressure"), style=KPI_VALUE_STYLE
                            ),
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
                                ui.card(
                                    ui.output_plot("pressure_min_temp_plot"),
                                    style=PLOT_CARD_STYLE,
                                ),
                                ui.card(
                                    ui.output_plot("pressure_max_temp_plot"),
                                    style=PLOT_CARD_STYLE,
                                ),
                                col_widths=(6, 6),
                            ),
                            ui.card(
                                ui.output_plot("temp_series"), style=PLOT_CARD_STYLE
                            ),
                            ui.card(
                                ui.output_plot("pressure_series"), style=PLOT_CARD_STYLE
                            ),
                        ),
                    ),
                )
            ),
        ),
        # AI Dashboard
        ui.nav_panel(
            "AI Page",
            ui.page_fluid(
                ui.div(
                    {"style": BG_STYLE},
                    ui.div(
                        ui.h2(
                            "MarsCast AI",
                            style="color:#FFFFFF; font-size:2.3em; font-weight:900; margin:0; text-shadow: 0 2px 12px rgba(0,0,0,0.9);",
                        ),
                        ui.p(
                            "Solstice checking in from Mars. Environmental data streams are active and ready for analysis.",
                            style="color:rgba(255,205,160,0.95); margin:4px 0 0 0;",
                        ),
                        style="display:flex; flex-direction:column; align-items:flex-start; max-width:1200px; margin:0 0 12px 0;",
                    ),
                    ui.tags.hr(style=TOP_RULE_STYLE),
                    ui.page_sidebar(
                        ui.sidebar(
                            ui.div(
                                {"class": "querychat"}, shinychat.chat_ui("mars_chat")
                            ),
                            width=400,
                            height="100%",
                            fillable=True,
                            class_="querychat-sidebar",
                        ),
                        ui.div(
                            ui.download_button(
                                "download_view",
                                "Download CSV",
                                style=DOWNLOAD_BUTTON_STYLE,
                            ),
                            ui.card(
                                ui.card_header(ui.output_text("title")),
                                ui.output_data_frame("data_table"),
                                fill=True,
                            ),
                            ui.card(
                                ui.output_plot("ai_pressure_min_temp_plot"),
                                style=PLOT_CARD_STYLE,
                            ),
                            ui.card(
                                ui.output_plot("ai_temp_series_plot"),
                                style=PLOT_CARD_STYLE,
                            ),
                            style="display:flex; flex-direction:column; gap:14px;",
                        ),
                        fillable=True,
                    ),
                )
            ),
        ),
    ],
    title=None,
    id="main_nav",
    inverse=True,
)


# Server
def server(input, output, session):
    sql_val = reactive.Value(None)
    title_val = reactive.Value(None)

    def update_dashboard(data):
        sql_val.set(data["query"])
        title_val.set(data["title"])

    def reset_dashboard():
        sql_val.set(None)
        title_val.set(None)

    chat = qc.client(update_dashboard=update_dashboard, reset_dashboard=reset_dashboard)
    mars_chat = shinychat.Chat("mars_chat")

    @mars_chat.on_user_submit
    async def _handle_chat_submit(user_input: str):
        context = retrieve_context(user_input)
        augmented = (
            f"## Retrieved Context\n{context}\n\n## User Question\n{user_input}"
            if context
            else user_input
        )
        stream = await chat.stream_async(augmented, echo="none", content="all")
        await mars_chat.append_message_stream(stream)

    @reactive.effect
    async def _greet():
        await mars_chat.append_message(GREETING)

    @reactive.calc
    def ai_filtered_df():
        q = sql_val()
        if not q:
            return df.execute()
        return nw.to_native(qc.data_source.execute_query(q))

    @output
    @render.data_frame
    def data_table():
        return render.DataGrid(ai_filtered_df(), height="420px")

    @output
    @render.download(filename="mars_ai_filtered.csv")
    def download_view():
        yield ai_filtered_df().to_csv(index=False)

    # AI Page Vizualizations
    @output
    @render.plot
    def ai_pressure_min_temp_plot():
        d = ai_filtered_df()
        if d is None or d.empty:
            plt.figure()
            plt.title("Air Pressure vs Minimum Temperature (AI Filtered)")
            plt.text(
                0.5, 0.5, "No data for current AI filter", ha="center", va="center"
            )
            plt.axis("off")
            return

        plt.figure()
        sns.regplot(x="pressure", y="min_temp", data=d, color="#FFAD70", ci=None)
        plt.ylabel("Min Temperature (C)")
        plt.xlabel("Air Pressure (Pa)")
        plt.title("Air Pressure vs Minimum Temperature (AI Filtered)")
        plt.xticks(rotation=0)

    @output
    @render.plot
    def ai_temp_series_plot():
        d = ai_filtered_df()
        if d is None or d.empty:
            plt.figure()
            plt.title("Daily Average Temperatures (AI Filtered)")
            plt.text(
                0.5, 0.5, "No data for current AI filter", ha="center", va="center"
            )
            plt.axis("off")
            return

        dd = d.copy()
        dd["terrestrial_date"] = pd.to_datetime(dd["terrestrial_date"])
        dd = (
            dd.set_index("terrestrial_date")[["min_temp", "max_temp"]]
            .resample("1D")
            .mean()
            .reset_index()
        )

        plt.figure(figsize=(10, 6))
        plt.plot(
            dd["terrestrial_date"],
            dd["min_temp"],
            label="Minimum Temperature",
            color="#FFAD70",
        )
        plt.plot(
            dd["terrestrial_date"],
            dd["max_temp"],
            label="Maximum Temperature",
            color="#C1440E",
        )
        plt.ylabel("Temperature (C)")
        plt.xlabel("Terrestrial date")
        plt.title("Daily Average Temperatures (AI Filtered)")
        plt.xticks(rotation=90)
        plt.legend()

    @output
    @render.text
    def title():
        return title_val() or "Mars Weather Data"

    def apply_filters(exclude=None):
        """Apply all active filters except the one named in `exclude`."""
        filtered = df

        if exclude != "month" and input.month() != "All":
            filtered = filtered.filter(_.month == input.month())

        if exclude != "season" and input.season() != "All":
            lo, hi = SEASON_MAP[input.season()]
            filtered = filtered.filter((_.ls >= lo) & (_.ls < hi))

        if exclude != "date_range":
            start, end = sorted(input.date_range())
            filtered = filtered.filter((_.terrestrial_date >= start)& (_.terrestrial_date <= end))

        if exclude != "recency" and input.recency() != "All":
            cutoff = df.terrestrial_date.max().execute() - RECENCY_MAP[input.recency()]
            filtered = filtered.filter(_.terrestrial_date >= cutoff)

        return filtered.execute()

    @reactive.calc
    def filtered_df():
        return apply_filters()

    @reactive.calc
    def series_filtered():
        filtered = filtered_df()
        return (
            filtered.set_index("terrestrial_date")[["max_temp", "min_temp", "pressure"]]
            .resample("1D")
            .mean()
            .reset_index()
        )

    @reactive.calc
    def filtered_baseline_df():
        current = filtered_df()
        if current.empty:
            return None

        target_dates = (current["terrestrial_date"] - pd.DateOffset(years=1)).dt.date
        baseline = df.filter(_.terrestrial_date.isin(target_dates))

        return baseline.execute()
    
    # --- Cascading filter updates ---

    @reactive.effect
    def _update_month_choices():
        ctx = apply_filters(exclude="month")
        present = set(ctx["month"].unique())
        valid = ["All"] + [
            f"Month {n}" for n in range(1, 13) if f"Month {n}" in present
        ]
        selected = input.month() if input.month() in valid else "All"
        ui.update_select("month", choices=valid, selected=selected)

    @reactive.effect
    def _update_season_choices():
        ctx = apply_filters(exclude="season")
        valid = ["All"] + [
            name
            for name, (lo, hi) in SEASON_MAP.items()
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
                name
                for name, offset in RECENCY_MAP.items()
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
        ui.update_date_range(
            "date_range",
            start=df.terrestrial_date.min().execute(),
            end=df.terrestrial_date.max().execute(),
        )

    # KPI Outputs
    @output
    @render.ui
    def avg_min():
        curr = filtered_df()
        base = filtered_baseline_df()

        if curr.empty:
            return ui.div("N/A", style="opacity: 0.6;")

        curr_avg = curr["min_temp"].mean()

        if base is None or base.empty:
            return ui.TagList(
                ui.div(f"{curr_avg:.2f} °C"),
                ui.div("No baseline data", style="font-size: 0.7em; opacity: 0.5;"),
            )

        base_avg = base["min_temp"].mean()
        cmp = compare(curr_avg, base_avg)

        return ui.TagList(
            ui.div(
                ui.span(
                    icon_svg(cmp["icon"], height="0.7em"), style=f"margin-right: 8px"
                ),
                ui.span(f"{curr_avg:.2f} °C"),
            ),
            ui.div(kpi_caption(cmp), style=KPI_CAPTION_STYLE),
        )

    @output
    @render.ui
    def avg_max():
        curr = filtered_df()
        base = filtered_baseline_df()

        if curr.empty:
            return ui.div("N/A", style="opacity: 0.6;")

        curr_avg = curr["max_temp"].mean()

        if base is None or base.empty:
            return ui.TagList(
                ui.div(f"{curr_avg:.2f} °C"),
                ui.div("No baseline data", style="font-size: 0.7em; opacity: 0.5;"),
            )

        base_avg = base["max_temp"].mean()
        cmp = compare(curr_avg, base_avg)

        return ui.TagList(
            ui.div(
                ui.span(
                    icon_svg(cmp["icon"], height="0.7em"), style=f"margin-right: 8px"
                ),
                ui.span(f"{curr_avg:.2f} °C"),
            ),
            ui.div(kpi_caption(cmp), style=KPI_CAPTION_STYLE),
        )

    @output
    @render.ui
    def avg_pressure():
        curr = filtered_df()
        base = filtered_baseline_df()

        if curr.empty:
            return ui.div("N/A", style="opacity: 0.6;")

        curr_avg = curr["pressure"].mean()

        if base is None or base.empty:
            return ui.TagList(
                ui.div(f"{curr_avg:.2f} Pa"),
                ui.div("No baseline data", style="font-size: 0.7em; opacity: 0.5;")
            )

        base_avg = base["pressure"].mean()
        cmp = compare(curr_avg, base_avg)

        return ui.TagList(
            ui.div(
                ui.span(
                    icon_svg(cmp["icon"], height="0.7em"), style=f"margin-right: 8px"
                ),
                ui.span(f"{curr_avg:.2f} Pa"),
            ),
            ui.div(kpi_caption(cmp), style=KPI_CAPTION_STYLE),
        )

    @output
    @render.text
    def std_pressure():
        filtered = filtered_df()
        return f"{filtered['pressure'].std():.2f} Pa" if not filtered.empty else "N/A"

    @output
    @render.plot
    def temp_series():
        filtered = series_filtered()
        plt.figure(figsize=(10, 6))
        plt.plot(
            filtered["terrestrial_date"],
            filtered["min_temp"],
            label="Minimum Temperature",
            color="#FFAD70",
        )
        plt.plot(
            filtered["terrestrial_date"],
            filtered["max_temp"],
            label="Maximum temperature",
            color="#C1440E",
        )
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
        plt.plot(filtered["terrestrial_date"], filtered["pressure"], color="#FFAD70")
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
        sns.regplot(x="pressure", y="min_temp", data=filtered, color="#FFAD70", ci=None)
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
        sns.regplot(x="pressure", y="max_temp", data=filtered, color="#C1440E", ci=None)
        plt.ylabel("Temperature (C)")
        plt.xlabel("Air Pressure (Pa)")
        plt.title("Air Pressure and Maximum Temperature")
        plt.xticks(rotation=90)
        plt.plot(legend=False)


app = App(app_ui, server, static_assets=Path(__file__).parent / "www")
