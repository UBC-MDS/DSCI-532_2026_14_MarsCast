from shiny import App, ui, render
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Loading the Data
df = pd.read_csv("data/raw/mars-weather.csv")

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
                choices=["Autumn (ls=0)", "Winter (ls=90)",
                         "Spring (ls=180)", "Summer (ls=270)"]
            )
        ),

        ui.card(
            ui.h5("Terrestrial Date"),
            ui.input_date_range(
                "date_range",
                None
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


