from config import Configuration
from flask import Flask


app = Flask(__name__)

app.secret_key = 'some secret key'

app.config.from_object(Configuration)
