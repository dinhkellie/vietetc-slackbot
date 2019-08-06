import os
from flask import Flask, request, make_response, render_template
from Startbot import Startbot

app = Flask(__name__)
@app.route("/", methods=["GET"])
def home():
  """This route renders a hello world text."""
  #rendering text
  return 'Vietcetera Analytics Bot connected and running!'
if __name__ == '__main__':
  bot = Startbot()
  bot.run()
  