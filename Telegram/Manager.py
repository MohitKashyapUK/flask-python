from Message import message
from CallbackQuery import callback_query

def manager(data):
  if "message" in data:
    message(data)
  elif "callback_query" in data:
    callback_query(data)