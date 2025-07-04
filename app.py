import plotly.express as px
from shiny import App, ui, render
from shinywidgets import output_widget, render_widget, render_plotly
import seaborn as sns
import matplotlib.pyplot as plt
from palmerpenguins import load_penguins

penguins_df = load_penguins()

app_ui = ui.page_fluid(
    ui.layout_sidebar(
        ui.sidebar(
            ui.h2("Sidebar"),
            ui.input_selectize(
                "selected_attribute",
                "Choose a column:", 
                ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
            ),
            ui.input_numeric(
                "plotly_bin_count",
                "Plotly Bin Count",
                10
            ),
            ui.input_slider(
                "seaborn_bin_count",
                "Seaborn Bin Count",
                1,
                100,
                5
            ),
            ui.input_checkbox_group(
                "selected_species_list",
                "Selected Bin List",
                ["Adelie", "Gentoo", "Chinstrap"],
                selected=["Adelie"],
                inline=True
            ),
            ui.hr(),
            ui.a(
                "GitHub",
                href="https://github.com/tmartin-m/cintel-02-data/blob/main/app.py",
                target="_blank"
            )
        ),
        ui.layout_columns(
            ui.card(
                ui.h3("Data Table (shiny.output_table)"),
                ui.output_table("table1"),
                ui.hr(),
                
                ui.h3("Plotly Histogram"),
                ui.output_plot("plotly_hist"),
                
                ui.h3("Seaborn Histogram"),
                ui.output_plot("seaborn_hist"),
                
                ui.h3("Plotly Scatterplot (Flipper Length vs Body Mass)"),
                ui.output_plot("scatterplot") 
            )
        )
    )
)

def server(input, output, session):
    
    @output
    @render.table
    def table1():
        return penguins_df.head(10)

    @output
    @render_plotly
    def plotly_hist():
        fig = px.histogram(
            penguins_df,
            x="body_mass_g",
            color="species",
            barmode="overlay",
            nbins=input.plotly_bin_count(),
            title="Plotly Histogram of Body Mass by Species"
        )
        return fig

    @output
    @render.plot
    def seaborn_hist():
        plt.figure(figsize=(8, 4))
        df = penguins_df.dropna(subset=[body_mass_g", "species"])
        sns.histplot(data=df, x="body_mass_g", hue="species", multiple="layer", bins=input.seaborn_bin_count())
        plt.title("Seaborn Histogram of Body Mass by Species")
        plt.xlabel("Body Mass (g)")
        plt.ylabel("Count")
        return plt.gcf()

    @output
    @render_plotly
    def scatterplot():
        fig = px.scatter(
            penguins_df,
            x="flipper_length_mm",
            y="body_mass_g",
            color="species",
            title="Scatterplot: Flipper Length vs Body Mass"
        )
        return fig
    
app = App(app_ui, server)
