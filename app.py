from flask import Flask
from flask import render_template, request, redirect, url_for
import sqlite3 as sql

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')
