from flask import Flask, render_template, request, session, redirect, url_for

from dalle import *
import os

app = Flask(__name__, template_folder="../frontend/html/", static_folder="../frontend/static/")

app.static_folder

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/generate", methods=["GET"])
def generate():
    prompt = request.args.get("prompt")
    size = request.args.get("size")
    n = int(request.args.get("n"))
    image_urls = extract_image_url(generate_image(prompt, size = size, n = n))
    to = download_image_from(image_urls = image_urls, to = app.static_folder + "/img/")
    return render_template("index.html")