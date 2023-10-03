from flask import Flask, request

app = Flask(__name__)

@app.get("/")
def hello_world():
  return "<p>Hello, World!</p>"

@app.route("/bot-handler/telegram", methods=["GET", "POST"])
def handler_telegram():
  # import "./bot-handler/telegram"
  import requests
  url = "https://sk-results.000webhostapp.com/do.php"
  params = { "data": request.get_data() }
  requests.get(url, params)
  return "True"

@app.get("/api/yt")
def yt_api():
  from urllib.parse import unquote
  from pytube import YouTube
  yt_url = request.args.get("url")
  if not yt_url: return "Please spacify YouTube URL"
  url = unquote(yt_url) # "https://youtu.be/FqAsaEVE2XY?si=Yp6_9nSdQpXJ4leP"
  yt = YouTube(url)
  streams = yt.streams
  for stream in streams:
    if stream.type == "video":
      print(f"Quality: {stream.resolution} Size: {stream.filesize_mb}mb FPS: {stream.fps} Audio: {stream.is_progressive}")
  return "Done!!!"

if __name__ == "__main__":
  app.run(debug=True)