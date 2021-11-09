from flask_app import app
from flask import render_template,request,redirect,session, flash
from flask_app.models.reg_login import Registration
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route("/")
def index():
    return render_template("reg_login.html")


@app.route("/validate_reg", methods=["POST"])
def register():
    if Registration.validate_reg(request.form):
        pw_hash = bcrypt.generate_password_hash(request.form["password"])
        data = {
            "first_name":request.form["first_name"],
            "last_name":request.form["last_name"],
            "email":request.form["email"],
            "password":pw_hash
        }
        user_id = Registration.register_user(data)
        session["user_id"] = user_id
        return redirect("/")
        flash("User created!")
    else:
        return redirect("/")


@app.route("/login", methods=["POST"])
def login():
    data = {
        "email":request.form["email"]
    }
    user_in_db = Registration.get_by_email(data)

    if not user_in_db:
        flash("Invalid Email or Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password,request.form["password"]):
        flash("Invalid Email or Password")
        return redirect("/")

    session["user_id"] = user_in_db.id
    return redirect("/userpage")


@app.route("/userpage")
def userpage():
    if "user_id" not in session:
        flash("You must be logged in!")
        return redirect("/")
    else:
        data = {
        "user_id":session["user_id"]
    }
        user = Registration.get_user(data)
        return render_template("user_page.html", user=user)


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out")
    return redirect("/")



