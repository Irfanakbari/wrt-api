from flask import Flask
from src.routes import Routes

app = Flask(__name__)

Routes.run(app)
