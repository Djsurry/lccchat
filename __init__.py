from flask import Flask, render_template, send_file, request
import sqlite3, string, random
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
        return render_template("verify.html", msg="Bad request")
    conn = sqlite3.connect('/var/www/lccchat/lccchat/lccchat.db')
    c = conn.cursor()
    a = list(c.execute('select email, verified, hash from users;'))
    def construct(n):
        email = n[0]
        vers = n[1].split()
        tokens = n[2].split()
        return {"email": email, "vers": vers, "tokens": tokens}
    users = [construct(n) for n in a]
    for user in users:
        if token in user["tokens"]:
            found = user
            break
    else:
        return render_template("verify.html", msg="Bad token")

    if found["vers"][found['tokens'].index(token)] == "1":
        return render_template("verify.html", msg="Token Already Used")

    found["vers"][found['tokens'].index(token)] = "1"
    new = ' '.join(found["vers"])
    if len(found["tokens"]) == 1:
        addr = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
        c.execute('update users set history="/home/histories/{}.json" WHERE email=?'.format(addr), (found["email"],))
    c.execute("update users set verified=? WHERE email=?", (new, found["email"])) 
    conn.commit()
    conn.close()
    return render_template("verify.html", msg="Your account has been verified")
    
 
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
