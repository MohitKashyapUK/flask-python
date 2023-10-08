from flask import Flask, request
from gunicorn.app.wsgiapp import WSGIApplication

app = Flask(__name__)

@app.get("/")
def hello_world():
  return "<b>/bot-handler/telegram</b>"

@app.get("/file")
def file():
  with open("output", "w") as f:
    f.write("hello")
  with open("output", "r") as f:
    return f.read()

@app.route("/bot-handler/telegram", methods=["GET", "POST"])
def handler_telegram():
  # Sending the JSON data
  import requests
  base_url = "https://sk-results.000webhostapp.com"
  url = base_url + "/do.php"
  params = { "data": request.get_data() }
  requests.get(url, params, stream=True)
  
  from Telegram.Manager import manager
  manager(request.get_json(force=True, silent=True))
  return "True"
  
import sys
from gunicorn.app.wsgiapp import run
if __name__ == '__main__':
  sys.argv = "gunicorn --bind 0.0.0.0:5151 app:app".split()
  sys.exit(run())