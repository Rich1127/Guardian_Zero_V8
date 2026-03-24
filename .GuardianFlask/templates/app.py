from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/home")
def home():
    return render_template("home.html", active_page="home")

@app.route("/foro")
def foro():
    return render_template("foro.html", active_page="foro")

@app.route("/reporte")
def reporte():
    return render_template("reporte.html", active_page="reporte")

@app.route("/capacitaciones")
def capacitaciones():
    return render_template("capacitaciones.html", active_page="capacitaciones")

@app.route("/perfil")
def perfil():
    return render_template("perfil.html", active_page="perfil")

if __name__ == "__main__":
    app.run(debug=True)