from flask import Flask, request, render_template, redirect, url_for, flash, jsonify
from src.routes import Routes

app = Flask(__name__)

Routes.run(app)
