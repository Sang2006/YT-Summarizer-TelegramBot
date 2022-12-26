<<<<<<< HEAD
=======
from telegram import Bot
from time import sleep
bot = Bot(token=os.environ['BOT_TOKEN'])
chat_id = 1402412411

# Send a message to the user
message = bot.send_message(chat_id=chat_id, text="Original message")

# Get the message_id of the message
message_id = message.message_id
sleep(5)

# Edit the message using the message_id
bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="Edited message")
>>>>>>> 2707f5470eb9f0955816899b9e9f330d7d191a19
