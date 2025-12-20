from flask import Flask, render_template, request
from graphy import plot_graph
from pathlib import Path
import json
app = Flask(__name__)
@app.route('/')

def ok():
    return render_template("home.html")

@app.route('/Main', methods = ['GET', 'POST'])
def ok2():
    if request.method == 'POST':
        input_value = str(request.form.get("stock"))
        print(f"Value received: {input_value}")
    BASE_DIR = Path(__file__).resolve().parent
    dir = BASE_DIR / "static" / "data" / "card_data.json"
    plot_graph(input_value)
    with open(dir,"r") as f:
        all_detl = json.load(f)
    for stock in all_detl:
        if stock['symbol'] == input_value:
            info = stock
    print(stock)
    return render_template("Main.html", info = info)

if __name__ == ("__main__"):
    app.run(debug=True)