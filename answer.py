from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from telegram import Bot

bot = Bot(token=os.environ['BOT_TOKEN'])
VIDEO_LINK_STATE = 1

# Start

def start(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text="Hello I'm a YouTube video summarizer bot!\n\nPlease select an option.\n/start\n/help\n/summarize\n\n\nCreated by Sangeeth")
    
def help(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text="This is a YouTube video summarizer bot that uses video transcripts to generate a summarized version of the video")
    
def summarize(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text= "Please enter a YouTube link")
    
    return VIDEO_LINK_STATE

def get_link(update, context):
    video_link = update.message.text
    print(video_link)
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text=video_link)
    return ConversationHandler.END
    

conversation_handler = ConversationHandler(
  entry_points=[CommandHandler("summarize", summarize)],
  states={
      VIDEO_LINK_STATE: [MessageHandler(Filters.text, get_link)],
  },
  fallbacks=[]
)

updater = Updater(token=os.environ['BOT_TOKEN'], use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(conversation_handler)

start_handler = CommandHandler("start", start)
dispatcher.add_handler(start_handler)

help_handler = CommandHandler("help", help)
dispatcher.add_handler(help_handler)

summarize_handler = CommandHandler("summarize", summarize)
dispatcher.add_handler(summarize_handler)



updater.start_polling()
