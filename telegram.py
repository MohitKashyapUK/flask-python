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

def callback_query(data):
  from pytube import YouTube
  import json, requests, os
  CallbackQuery = data["callback_query"]
  message_id = CallbackQuery["message"]["message_id"]
  chat_id = CallbackQuery["from"]["id"]
  callback_data = json.loads(CallbackQuery["data"])
  bot_api = "https://api.telegram.org"
  bot_token = os.getenv("bot_token")
  method = "editMessageReplyMarkup"
  url = f"{bot_api}/bot{bot_token}/{method}"
  params = { "chat_id": chat_id, "message_id": message_id }
  get_video = callback_data.get("yt_v")
  get_audio = callback_data.get("yt_a")
  if get_video:
    reply_markup = { "inline_keyboard": [] }
    yt = YouTube("https://m.youtube.com/watch?v=" + get_video)
    fmt_streams = yt.fmt_streams
    i = 0
    fmt_streams_len = len(fmt_streams)
    while i < fmt_streams_len:
      stream = fmt_streams[i]
      resolution = stream.resolution
      filesize_mb = stream.filesize_mb
      sub_type = stream.sub_type
      is_progressive = stream.is_progressive
      if resolution:
        reply_markup["inline_keyboard"].append([{
          "text": f"{resolution},{filesize_mb}mb,{sub_type},Audio: {is_progressive}",
          "url": stream.url
        }])
      i += 1
    params["reply_markup"] = json.dumps(reply_markup)
  """elif get_audio:
    
  else:
  """
  resp = requests.post(url, data=params)
  if not resp.json()["ok"]:
    print(resp.text)