from flask import Flask, request
from gunicorn.app.wsgiapp import WSGIApplication

app = Flask(__name__)

@app.get("/")
def hello_world():
  return "<b>/bot-handler/telegram</b>"

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
  if data:
    if data.get("message"):
      telegram.message(data)
    elif data.get("callback_query"):
      telegram.callback_query(data)
  else:
    print("Wrong request data!")
  return "True"
  
def run_gunicorn():
    gunicorn_app = WSGIApplication(app.wsgi_app, host="0.0.0.0", port=8000)
    gunicorn_server = gunicorn.GunicornWSGIServer(gunicorn_app)
    gunicorn_server.serve()

if __name__ == "__main__":
    run_gunicorn()