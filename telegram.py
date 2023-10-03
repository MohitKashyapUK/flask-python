def message(data):
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
  return "True"