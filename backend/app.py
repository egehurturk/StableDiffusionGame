from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from dalle import *

import os


# engine = create_engine("postgresql://egehurturk:egehurturk@localhost:5432/sessiontest")
# db = scoped_session(sessionmaker(bind=engine))

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/", methods=["GET"])
def reset():
    return render_template("../frontend/html/ndex.html")

@app.route("/api", method=["POST"])
def api():
    download_image_from(extract_image_url(dalle.generate_image(request.form.get("prompt")))
    return render_template("../frontend/html/result.html")
