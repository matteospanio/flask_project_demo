"""Routes di base che permettono la navigazione standard del server."""

from flask import Blueprint, render_template

views = Blueprint("views", __name__, url_prefix="/")


@views.get("/")
def home():
    return render_template("index.html")


@views.get("/login")
def login():
    return render_template("login.html")


@views.get("/signin")
def signin():
    return render_template("signin.html")
