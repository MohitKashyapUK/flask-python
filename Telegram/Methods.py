import os, json, requests

bot_api = "https://api.telegram.org"
bot_token = os.getenv("bot_token")
url = f"{bot_api}/bot{bot_token}/"

def editMessageText(chat_id, message_id, text, reply_markup=None):
  method = "editMessageText"
  params = { "chat_id": chat_id, "message_id": message_id, "text": text }
  if reply_markup:
    params["reply_markup"] = json.dumps(reply_markup)
  resp = requests.post(url + method, data=params)
  if not resp.json()["ok"]:
    print(resp.text)
    return False
  return True

def send_message(chat_id, text, reply_markup=None):
  method = "sendMessage"
  params = { "chat_id": chat_id, "text": text }
  if reply_markup:
    params["reply_markup"] = json.dumps(reply_markup)
  resp = requests.post(url + method, data=params)
  if not resp.json()["ok"]:
    print(resp.text)
    return False
  return True