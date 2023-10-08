from pytube import YouTube
from Telegram.Methods import editMessageText
import json
import os
import requests

def callback_query(data):
  CallbackQuery = data["callback_query"]
  callback_data = json.loads(CallbackQuery["data"])
  get_video = callback_data.get("yt_v")
  get_audio = callback_data.get("yt_a")
  back = callback_data.get("back")
  is_audio_or_video = get_video or get_audio
  video_id = is_audio_or_video or back
  yt_url = "https://www.youtube.com/watch?v=" + video_id
  chat_id = CallbackQuery["from"]["id"]
  message_id = CallbackQuery["message"]["message_id"]
  reply_markup = { "inline_keyboard": [] }
  
  if is_audio_or_video:
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
        "callback_data": json.dumps({ "itag": itag, "id": video_id })
      }
      reply_markup["inline_keyboard"].append([item])
    back_btn = {
      "text": "« Back",
      "callback_data": json.dumps({ "back": video_id })
    }
    reply_markup["inline_keyboard"].append([back_btn])
    text = f"Here are all the { 'video' if get_video else 'audio' }s!"
  elif back: # Back
    item = [
      {
        "text": "Video",
        "callback_data": json.dumps({ "yt_v": video_id })
      }, {
        "text": "Audio",
        "callback_data": json.dumps({ "yt_a": video_id })
      }
    ]
    reply_markup["inline_keyboard"].append(item)
    text = "Select the type!"
  
  editMessageText(chat_id, message_id, text, reply_markup)