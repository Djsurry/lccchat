from flask import Flask, render_template, send_file, request
import sqlite3
import sys, os

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/downloads")
def downloads():
    return render_template("downloads.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/logo")
def logo():
    return send_file("/var/www/lccchat/lccchat/logo.png")
@app.route("/icon")
def icon():
    return send_file("/var/www/lccchat/lccchat/icon.png")
@app.route("/help")
def help():
    return render_template("help.html")

@app.route("/signup", methods=["POST"])
def signup():
    email = request.form["email"]
    conn = sqlite3.connect('/var/www/lccchat/lccchat/lccchat.db')
    c = conn.cursor()
    c.execute("insert or ignore into updates values (?)", (email,))
    conn.commit()
    conn.close()
    return "success"

@app.route("/verify")
def verify():
    token = request.args.get("token")
    if token == None:
        return "Bad Request", 404
    conn = sqlite3.connect('/var/www/lccchat/lccchat/lccchat.db')
    c = conn.cursor()

    r = [n for n in c.execute("select verified, hash from users")]
    print(f"r: {r}")
    user = None
    for row in r:
        print(row)
        v = row[0].split(' ')
        h = row[1].split(' ')
        if token in h:
            user = [v, h] 
    if not user:
        return "Bad token"
    print(user)
    if user[0][user[1].index(token)] == "0":
        n = user[0]
        n[user[1].index(token)] = "1"
    else:
        conn.close()
        return "Token Already Used"

    s = ''
    for i in n:
        s += i
        s += " "
    
    c.execute("update users set verified=? WHERE hash=?", (s, token)) 
    c.execute('update users set history="/home/histories/{}.json" WHERE hash=?'.format(token), (token,))
    os.system("touch /home/histories/{}.json".format(token))
    conn.commit()
    conn.close()
    return render_template("verify.html")
    
 
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
