import os
from flask import Flask, request, make_response, render_template
from startbot import Startbot

app = Flask(__name__)
@app.route("/", methods=["GET"])
def home():
  """This route renders a hello world text."""
  bot = Startbot()
  bot.run()
  return 'Vietcetera Analytics Bot connected and running!'
home()
  