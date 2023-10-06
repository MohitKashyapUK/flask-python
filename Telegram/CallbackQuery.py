from pytube import YouTube
import json
import os
import requests

def callback_query(data):
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
  is_audio_or_video = get_video or get_audio
  video_id = is_audio_or_video or callback_data
  yt_url = f"https://m.youtube.com/watch?v={video_id}"
  
  if is_audio_or_video:
    reply_markup = { "inline_keyboard": [] }
    yt = YouTube(yt_url)
    fmt_streams = yt.streams.filter(type=("video" if get_video else "audio"))
    reso = "resolution" if get_video else "abr"
    
    for stream in fmt_streams:
      resolution = getattr(stream, reso)
      filesize_mb = stream.filesize_mb
      subtype = stream.subtype
      itag = stream.itag
      item = {
        "text": f"{resolution}, {filesize_mb}mb, {subtype}",
        "callback_data": itag
      }
      reply_markup["inline_keyboard"].append([item])
    back_btn = {
      "text": "« Back",
      "callback_data": video_id
    }
    reply_markup["inline_keyboard"].append([back_btn])
    reply_markup["text"] = f"Here are all the { 'video' if get_video else 'audio' }s!"
  else: # Back
    reply_markup = {
      "inline_keyboard": [
        [
          {
            "text": "Video",
            "callback_data": json.dumps({ "yt_v": video_id })
          }, {
            "text": "Audio",
            "callback_data": json.dumps({ "yt_a": video_id })
          }
        ]
      ]
    }
    params["text"] = "Select the type!"
  
  params["reply_markup"] = json.dumps(reply_markup)
  resp = requests.post(url, data=params)
  if not resp.json()["ok"]:
    print(resp.text)