from flask import Flask, render_template, request
from graphy import plot_graph
from pathlib import Path
import sqlite3
import pandas as pd

app = Flask(__name__)
@app.route('/')

def ok():
    return render_template("home.html")

@app.route('/Main', methods = ['GET', 'POST'])
def ok2():
    input_value = str(request.form.get("stock"))
    BASE_DIR = Path(__file__).resolve().parent
    dir = BASE_DIR / "static" / "data" / "card_data.db"
    plot_graph(input_value)
    con = sqlite3.connect(dir)
    cur = con.cursor()
    df = pd.read_sql(f"""SELECT * FROM Card_data where symbol like "{input_value}" """, con)
    info = df.to_dict(orient = "records")
    return render_template("Main.html", info = info[0])

if __name__ == ("__main__"):
    app.run(debug=True)