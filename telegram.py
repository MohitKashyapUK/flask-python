def message(data):
  from pytube import YouTube, extract
  import os, json, requests
  Message = data["message"]
  message_id = Message["message_id"]
  chat_id = Message["from"]["id"]
  text = Message["text"]
  bot_api = "https://api.telegram.org"
  bot_token = os.getenv("bot_token")
  method = "sendMessage"
  params = { "chat_id": chat_id }
  try:
    video_id = extract.video_id(text)
  except Exception as e:
    video_id = None
  url = f"{bot_api}/bot{bot_token}/{method}"
  def send_message(msg):
    requests.post(url, data={ "chat_id": chat_id, "text": msg })
  if video_id:
    params["reply_markup"] = json.dumps({
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
    })
    params["text"] = "Select the type!!!"
    resp = requests.post(url, data=params)
    if not resp.json()["ok"]:
      send_message(resp.text)
  else:
    send_message(json.dumps(data))