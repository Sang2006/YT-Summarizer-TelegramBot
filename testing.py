from telegram import Bot
from time import sleep
bot = Bot(token='5522976180:AAFzWAHrgs9T8I1WTG8mwQ9FgHDDe5Cz0hE')
chat_id = 1402412411

# Send a message to the user
message = bot.send_message(chat_id=chat_id, text="Original message")

# Get the message_id of the message
message_id = message.message_id
sleep(5)

# Edit the message using the message_id
bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="Edited message")