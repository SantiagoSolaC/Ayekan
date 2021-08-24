from flask import render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import login_user, login_required, logout_user, current_user
from . import auth


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
       
        user = User.query.filter_by(username = username).first()
        
        if user:
            if check_password_hash(user.password, password):
                flash("Ingresado correctamente!", category = "success")
                login_user(user, remember = True)
                return redirect(url_for("views.home"))
            else:
                flash("Contrasenia incorrecta.", category = "danger")
        else:
            flash("Nombre de usuario incorrecto.", category = "danger")
    
    else:
        return render_template("login.html", user = current_user)
    
    
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
    

def register():
    # username = request.form.get("username")
    # password = request.form.get("password")
    username = "poto"
    password = "poto"
    new_user = User(username = username, password = generate_password_hash(password, method="sha256"))
    db.session.add(new_user)
    db.session.commit()
    print("Cuenta creada")
    # flash("Account created!", category="success")
    # return redirect(url_for("views.home"))
