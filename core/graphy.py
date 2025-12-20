import plotly.graph_objects as go
import pandas as pd
from pathlib import Path
def plot_graph(name : str):
    BASE_DIR = Path(__file__).resolve().parent
    csv_path = BASE_DIR / "static" / "data" / "chart_data.csv"
    html_path = BASE_DIR / "static" / "data" / "graph.html"

    df = pd.read_csv(csv_path, header=[0,1], index_col=0)
    df = df.ffill().bfill()
    df.index = pd.to_datetime(df.index)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x = df.index,
            y = df[(name ,'Close')],
            mode = "lines"
        )
    )
    fig.write_html(html_path)

if __name__ == "main":
    #test here
    plot_graph("Name")