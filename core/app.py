from flask import Flask, render_template, request, redirect, flash
from graphy import plot_graph, plot_graphy
from pathlib import Path
import sqlite3
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = os.urandom(24) 
BASE_DIR = Path(__file__).resolve().parent

# Dictionary of card data
def card_values(input_value):
    dir = BASE_DIR / "static" / "data" / "card_data.db"
    con = sqlite3.connect(dir)
    df = pd.read_sql(f"""SELECT * FROM Card_data where symbol like '{input_value}' """, con)
    info = df.to_dict(orient = "records")   
    return info 

#Saving user data
def save_data(fname, lname, email, password):
    dir = BASE_DIR / "static" / "data" / "user_data.db"
    con = sqlite3.connect(dir)
    cur = con.cursor()
    cur.execute("""
                create table if not exists user_data(
                email text primary key,
                fname text,
                lname text,
                password text
                )
                """)
    cur.executemany("""
                    insert or ignore into user_data(fname, lname, email, password)
                    values(?, ?, ?, ?)
                    """, [(fname, lname, email, password)]
                    )
    con.commit()
    
# login check
def login_check(email):
    dir = BASE_DIR / "static" / "data" / "user_data.db"
    con = sqlite3.connect(dir)
    cur = con.cursor()
    cur.execute("""
                select * from user_data
                """)
    data = cur.fetchall()
    for row in data:
        if row[0] == email:
            return True
    return False
    
# Signup page
@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    
    input_iemail = request.form.get("iemail")
    input_email = request.form.get("uemail")
    
    if input_email != None:
        input_fname = request.form.get("fname")
        input_lname = request.form.get("lname")
        input_pass = request.form.get("pass")
        save_data(input_fname, input_lname, input_email, input_pass)
        return redirect("/")
    elif input_iemail != None:
        input_ipass = request.form.get("ipass")
        if login_check(input_iemail):
            return redirect("/")
        else:
            flash("Account does not exist. Please Sign Up first.", "error")
            return redirect("/signup")
    return render_template("signup.html")

#Home page {main hub fro over all navigation}
@app.route('/', methods = ['GET', 'POST'])
def home_page():
    plot_graph("^NSEI")
    info = card_values("^NSEI")
    return render_template("home_page.html", info = info[0])

#About page
@app.route('/aboutus')
def about():
    return render_template("aboutusbrand.html")

#Trending page
@app.route('/trending', methods = ['GET', 'POST'])
def trending():
    plot_graphy("^NSEI")
    plot_graphy("^BSESN")
    plot_graphy("GOLDBEES.NS")
    info = card_values("^NSEI")
    info.append(card_values("^BSESN")[0])
    info.append(card_values("GOLDBEES.NS")[0])
    return render_template("trending.html", info = info[0], info1 = info[1], info2 = info[2])

#Selection page{Later use}
@app.route('/selection')
def home():
    return render_template("selection.html")

# Leading to actual analysis
@app.route('/Main', methods = ['GET', 'POST'])
def ok2():
    input_value = str(request.form.get("stock"))
    plot_graph(input_value)
    info = card_values(input_value)
    return render_template("Main.html", info = info[0])

if __name__ == ("__main__"):
    app.run(debug=True)