from pytube import extract
import os
import json
import requests

def send_message(chat_id, text, reply_markup=None):
  bot_api = "https://api.telegram.org"
  bot_token = os.getenv("bot_token")
  method = "sendMessage"
  url = f"{bot_api}/bot{bot_token}/{method}"
  params = { "chat_id": chat_id, "text": text }
  if reply_markup:
    params["reply_markup"] = json.dumps(reply_markup)
  resp = requests.post(url, data=params)
  if not resp.json()["ok"]:
    print(resp.text)

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
