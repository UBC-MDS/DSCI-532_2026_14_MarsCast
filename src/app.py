from shiny import App, ui, render, reactive
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Loading the Data
df = pd.read_csv("data/raw/mars-weather.csv")
df["terrestrial_date"] = pd.to_datetime(df["terrestrial_date"])

# UI Section

app_ui = ui.page_fluid(
    ui.h1("MarsCast", style="text-align:center; color:red;"),
    ui.h4("Weather Patterns from The Red Planet", style="text-align:center; color:#FF6347;"),
    ui.hr(),

    # Filters
    ui.layout_columns(

        ui.card(
            ui.h5("Martian Month"),
            ui.input_select(
                "month",
                None,
                choices=sorted(df["month"].dropna().unique())
            )
        ),

        ui.card(
            ui.h5("Season (Solar Longitude)"),
            ui.input_select(
                "season",
                None,
                  choices={
                    "Autumn (ls = 0)": 0,
                    "Winter (ls = 90)": 90,
                    "Spring (ls = 180)": 180,
                    "Summer (ls = 270)": 270
                }
            )
        ),

        ui.card(
            ui.h5("Terrestrial Date"),
            ui.input_date_range(
                "date_range",
                None,
                start=df["terrestrial_date"].min(),
                end=df["terrestrial_date"].max()
            )
        ),
    ),

    ui.hr(),

    # KPI Section
    ui.layout_columns(

        ui.card(
            ui.h5("Latest Sol"),
            ui.output_text("latest_sol")
        ),

        ui.card(
            ui.h5("Average Min Temp (°C)"),
            ui.output_text("avg_min")
        ),

        ui.card(
            ui.h5("Average Max Temp (°C)"),
            ui.output_text("avg_max")
        ),

        ui.card(
            ui.h5("Average Pressure (Pa)"),
            ui.output_text("avg_pressure")
        ),
    ),
    ui.hr(),

    # Distribution Plots
    ui.layout_columns(

        ui.card(ui.output_plot("sol_plot")),
        ui.card(ui.output_plot("ls_plot")),
    ),

    ui.layout_columns(
        ui.card(ui.output_plot("min_temp_plot")),
        ui.card(ui.output_plot("pressure_plot")),
    ),


)

# Server

def server(input, output, session):


    @reactive.calc
    def filtered_df():
        filtered = df.copy()

        # Filter by the  month
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
    

    #KPI Outputs
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


