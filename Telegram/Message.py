from pytube import extract
from Telegram.Methods import send_message
import os
import json
import requests

def message(data):
  Message = data["message"]
  chat_id = Message["from"]["id"]
  text = Message["text"]
  
  try:
    video_id = extract.video_id(text)
  except Exception as e:
    video_id = None
  
  if video_id:
    reply_markup = {
      "inline_keyboard": [
        [
          { "text": "Video", "callback_data": json.dumps({ "yt_v": video_id }) },
          { "text": "Audio", "callback_data": json.dumps({ "yt_a": video_id }) }
        ]
      ]
    }
    send_message(chat_id, "Select the type!!!", reply_markup)
  else:
    send_message(chat_id, json.dumps(data))

# Example usage:
# message({"message": {"from": {"id": "123"}, "text": "https://www.youtube.com/watch?v=abcd1234"}})
