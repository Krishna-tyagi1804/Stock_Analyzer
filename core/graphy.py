import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import sqlite3
from pathlib import Path

def plot_graphy(name : str):
    BASE_DIR = Path(__file__).resolve().parent
    card_path = BASE_DIR / "static" / "data" / "chart_data.db"
    html_path = BASE_DIR / "static" / "data" / f"{name}_graph.html"
    con = sqlite3.connect(card_path)
    df = pd.read_sql(f"SELECT * FROM Chart_data", con, index_col="Date")
    df = df.dropna()
    df = df.bfill().ffill()
    df[f'{name}_SMA_20'] = df[f'{name}_Close'].rolling(window=20).mean()
    df[f'{name}_SMA_50'] = df[f'{name}_Close'].rolling(window=50).mean()
    df[f'{name}_SMA_200'] = df[f'{name}_Close'].rolling(window=200).mean()
   
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
            go.Scatter(
                x = df.index,
                y = df[f'{name}_Close'],
                mode = "lines",
                line=dict(width=1.5,color='blue'),
                name="Price",  
                ),
            secondary_y=False
    )    
    fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Price",
    template="plotly_white",
    hovermode="x unified", 
    hoverlabel=dict(
        bgcolor="white", 
        font_size=12
    ),
    )
    
    fig.update_xaxes(
    rangeselector=dict(
        buttons=list([
            dict(count=6, label="1w", step="day", stepmode="backward"),
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(step="all")
        ])
    ),
    showspikes=True, 
    spikemode="across", 
    spikesnap="cursor", 
    spikethickness=1,
    spikecolor="grey"
    )
    fig.update_yaxes(
    showspikes=True, 
    spikethickness=1,
    spikecolor="grey"
    )
    fig.update_layout(
    # 1. This removes the whitespace INSIDE the graph
    margin=dict(l=0, r=0, t=0, b=0),
    
    # 2. This ensures the background matches your card
    paper_bgcolor='rgba(0,0,0,0)', # Transparent background
    plot_bgcolor='rgba(0,0,0,0)',
    
    # 3. Adjust the height if needed
    height=300, 
    autosize=True
    )
    fig.write_html(html_path, config={'displayModeBar': False})
    

def plot_graph(name : str):
    BASE_DIR = Path(__file__).resolve().parent
    card_path = BASE_DIR / "static" / "data" / "chart_data.db"
    html_path = BASE_DIR / "static" / "data" / "graph.html"
    con = sqlite3.connect(card_path)
    df = pd.read_sql(f"SELECT * FROM Chart_data", con, index_col="Date")
    df = df.dropna()
    df = df.bfill().ffill()
    df[f'{name}_SMA_20'] = df[f'{name}_Close'].rolling(window=20).mean()
    df[f'{name}_SMA_50'] = df[f'{name}_Close'].rolling(window=50).mean()
    df[f'{name}_SMA_200'] = df[f'{name}_Close'].rolling(window=200).mean()
   
    fig = make_subplots(specs=[[{"secondary_y": True}]]) 
    fig1 = make_subplots(specs=[[{"secondary_y": True}]]) 
    
    fig1.add_trace(
            go.Candlestick(
            x=df.index,
            open=df[f'{name}_Open'],
            high=df[f'{name}_High'],
            low=df[f'{name}_Low'],
            close=df[f'{name}_Close'],
            increasing_line_color= '#26a69a', 
            decreasing_line_color= '#ef5350'
         )
    )
    
    fig1.add_trace(
            go.Scatter(
                x = df.index,
                y = df[f'{name}_SMA_20'],
                mode = "lines",
                line=dict(width=1.5),
                name="SMA 20",  
                ),
            secondary_y=False
        )
    
    
    fig1.update_layout(
    title='Technical Analysis',
    yaxis_title='Price',
    template='plotly_white',  # Dark mode is standard for trading apps
    xaxis_rangeslider_visible=False,  # Remove the bottom slider to save space
    showlegend=False,  # Hiding legend often looks cleaner for single tickers
    margin=dict(l=50, r=50, t=80, b=50)
    )
    
    
    fig1.update_xaxes(
    showspikes=True, 
    spikemode="across", 
    spikesnap="cursor", 
    spikethickness=1,
    spikecolor="grey"
    )
    
    fig1.update_yaxes(
    type="log",   
    secondary_y=False,
    autorange=True,
    showspikes=True, 
    spikethickness=1,
    spikecolor="grey"
    )
    
    fig.add_trace(
    go.Bar(
        x=df.index, 
        y=df[f'{name}_Volume'], 
        name="Volume", 
        marker_color='blue', 
    ),
    secondary_y=True
    )
    
    fig.add_trace(
            go.Scatter(
                x = df.index,
                y = df[f'{name}_Close'],
                mode = "lines",
                line=dict(width=1.5,color='blue'),
                name="Price",  
                ),
            secondary_y=False
        )
    
    max_vol = df[f'{name}_Volume'].max()
    fig.update_yaxes(
    title_text="Volume", 
    secondary_y=True, 
    range=[0, 5*max_vol],
    showgrid=False,
    )
    
    fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Price",
    template="plotly_white",
    hovermode="x unified", 
    hoverlabel=dict(
        bgcolor="white", 
        font_size=12
    ),
    )
    
    fig.update_xaxes(
    rangeselector=dict(
        buttons=list([
            dict(count=6, label="1w", step="day", stepmode="backward"),
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(step="all")
        ])
    ),
    showspikes=True, 
    spikemode="across", 
    spikesnap="cursor", 
    spikethickness=1,
    spikecolor="grey"
    )
    fig.update_yaxes(
    showspikes=True, 
    spikethickness=1,
    spikecolor="grey"
    )
    
    fig.update_layout(modebar_orientation="v")
    fig1.update_layout(modebar_orientation="v")
    p1 = fig.to_html(full_html=False, include_plotlyjs='cdn')
    p2 = fig1.to_html(full_html=False, include_plotlyjs='cdn')
    
    content_html = f"""
    <!DOCTYPE html>
    <html>
    <body>
    <div class="chart-box">
            {p1}
        <br>
            {p2}
        </div>
    </body>
    </html>    
    """
    with open(html_path, "w") as f:
        f.write(content_html)

#plot_graph("AAPL")
#test