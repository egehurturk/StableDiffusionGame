from flask import Flask, render_template, request, session, redirect, url_for

from dalle import *
import os

app = Flask(__name__, template_folder="../frontend/html/", static_folder="../frontend/static/")


@app.route("/", methods=["GET"])
def hello():
    return render_template("index.html")
