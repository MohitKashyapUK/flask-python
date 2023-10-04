from flask import Flask, request

app = Flask(__name__)

@app.get("/")
def hello_world():
  return "<p>Hello, World!</p>"

@app.route("/bot-handler/telegram", methods=["GET", "POST"])
def handler_telegram():
  # Sending the JSON data
  import requests
  base_url = "https://sk-results.000webhostapp.com"
  url = base_url + "/do.php"
  params = { "data": request.get_data() }
  requests.get(url, params, stream=True)
  
  # Handling request
  import telegram
  data = request.get_json(force=True, silent=True)
  log_url = base_url + "/Log.php"
  def log(t):
    requests.get(log_url, { "data": t }, stream=True)
  log("App:")
  log("Line 25: Handling request")
  if data:
    log("Line 27: Handling data")
    if data.get("message"):
      log("Line 29: Handling message")
      try:
        telegram.message(data)
      except Exception as e:
        log(str(e))
  else:
    print("Wrong request data!")
  log("App: finishing")
  return "True"

if __name__ == "__main__":
  import sys
  from gunicorn.app.wsgiapp import run
  sys.argv = "gunicorn --bind 0.0.0.0:5151 app:app".split()
  sys.exit(run())