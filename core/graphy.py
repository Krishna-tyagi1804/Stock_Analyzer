import plotly.graph_objects as go
import pandas as pd
import sqlite3
from pathlib import Path

def plot_graph(name : str):
    BASE_DIR = Path(__file__).resolve().parent
    card_path = BASE_DIR / "static" / "data" / "chart_data.db"
    html_path = BASE_DIR / "static" / "data" / "graph.html"
    con = sqlite3.connect(card_path)
    df = pd.read_sql(f"SELECT * FROM Chart_data", con, index_col="Date")
    df = df.ffill().bfill()

    fig = go.Figure()
    fig.add_trace(
            go.Scatter(
                x = df.index,
                y = df[f'{name}_Close'],
                mode = "lines",
                name = name
            )
        )
    fig.write_html(html_path)

#plot_graph("AAPL")
#test