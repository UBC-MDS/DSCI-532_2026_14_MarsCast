from shiny import App, ui, render
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Loading the Data
df = pd.read_csv("data/raw/mars-weather.csv")
df["terrestrial_date"] = pd.to_datetime(df["terrestrial_date"])

# UI Section

app_ui = ui.page_fluid(
    ui.h1("MarsCast"),
    ui.h4("Weather Patterns from The Red Planet"),
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

    @output
    @render.text
    def latest_sol():
        return str(df["sol"].max())

    @output
    @render.text
    def avg_min():
        return f"{df['min_temp'].mean():.2f}"

    @output
    @render.text
    def avg_max():
        return f"{df['max_temp'].mean():.2f}"

    @output
    @render.text
    def avg_pressure():
        return f"{df['pressure'].mean():.2f}"

    @output
    @render.plot
    def sol_plot():
        plt.figure()
        plt.hist(df["sol"], bins=20)
        plt.title("Distribution of Sol")

    @output
    @render.plot
    def ls_plot():
        plt.figure()
        plt.hist(df["ls"], bins=20)
        plt.title("Distribution of Solar Longitude (ls)")

    @output
    @render.plot
    def min_temp_plot():
        plt.figure()
        plt.hist(df["min_temp"], bins=20)
        plt.title("Distribution of Minimum Temperature")

    @output
    @render.plot
    def pressure_plot():
        plt.figure()
        plt.hist(df["pressure"], bins=20)
        plt.title("Distribution of Pressure")

app = App(app_ui, server)


