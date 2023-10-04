def message(data):
  def log(t):
    requests.get("https://sk-results.000webhostapp.com/Log.php", { "data": t }, stream=True)
  log("Message")
  from pytube import YouTube, extract
  import os, json, requests
  Message = data["message"]
  message_id = Message["message_id"]
  chat_id = Message["from"]["id"]
  text = Message["text"]
  bot_api = "https://api.telegram.org"
  bot_token = os.environ.get("bot_token")
  method = "sendMessage"
  params = { "chat_id": chat_id }
  try:
    video_id = extract.video_id(text)
  except Exception as e:
    video_id = None
  url = f"{bot_api}/bot{bot_token}/{method}"
  if video_id:
    log("video_id")
    params["reply_markup"] = {
      "inline_keyboard": [
        [
          {
            "text": "Video",
            "callback_data": json.dumps({ "yt_v": video_id })
          }, {
            "text": "Audio",
            "callback_data": json.dumps({ "yt_a": video_id })
          }
        ], [
          {
            "text": "« Back",
            "callback_data": json.dumps({ "yt": video_id })
          }
        ]
      ]
    }
    resp = requests.post(url, data=params)
    print(resp.text)
  else:
    resp = requests.post(url, data={ "chat_id": chat_id, "text": data })
    print(resp.text)
  log("Message finished")
  return "True"