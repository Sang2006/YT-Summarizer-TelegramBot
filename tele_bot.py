from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from telegram import Bot
from urllib.parse import urlparse
from youtube_transcript_api import YouTubeTranscriptApi
import openai
from gtts import gTTS
import os

bot = Bot(token='5522976180:AAFzWAHrgs9T8I1WTG8mwQ9FgHDDe5Cz0hE')
VIDEO_LINK_STATE = 1
video_link = ''

def main():
    # Start

    def start(update, context):
        chat_id = update.effective_chat.id
        context.bot.send_message(chat_id=chat_id, text="Hello I'm a YouTube video summarizer bot!\n\nPlease select an option.\n\n/start\n/help\n/summarize\n\n\nCreated by Sangeeth")

    def help(update, context):
        chat_id = update.effective_chat.id
        context.bot.send_message(chat_id=chat_id, text="This is a YouTube video summarizer bot that uses video transcripts to generate a summarized version of the video")

    def summarize(update, context):
        chat_id = update.effective_chat.id
        context.bot.send_message(chat_id=chat_id, text= "Please enter a YouTube link")

        return VIDEO_LINK_STATE

    def get_link(update, context):
        video_link = update.message.text

        # getting the video id
        parsed_url = urlparse(video_link)
        query_params = parsed_url.query.split('&')
        global video_id
        video_id = None
        for param in query_params:
            if param.startswith('v='):
                try:
                    video_id = param.split('=')[1]
                    break
                except Exception as e:
                    print('Something went worng')
                    print(e)
        chat_id = update.effective_chat.id

        # getting the trascript
        data = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = ""
        for d in data:
            transcript += d['text'] + " "

        # summarizing
        openai.api_key = "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"

        model_engine = "text-davinci-003"

        stop = '~'
        prompt = f"Summarize this YouTube video and please ignore any sponsor segments{transcript}~"
        words = prompt.split()
        word_count = len(words)

        if word_count > 500:
            prompt = ' '.join(words[:500])
            prompt = prompt + '~'

        def parse_response(completion):

            summary = completion['choices'][0]['text']
            return summary

        try:
            completion = openai.Completion.create(engine=model_engine, prompt=prompt, max_tokens=100, stop=stop)
            #print(completion)
            summary = parse_response(completion)
            print(summary)
        except Exception as e:
            print('Something went wrong')
            print(e)

        context.bot.send_message(chat_id=chat_id, text=summary)
        # Generating an audio file    
        tts_text = summary
        tts = gTTS(tts_text)
        tts.save("summary.mp3")
        with open('summary.mp3', 'rb') as f:
            context.bot.send_audio(chat_id=chat_id, audio=f)
        return ConversationHandler.END

    conversation_handler = ConversationHandler(
    entry_points=[CommandHandler("summarize", summarize)],
    states={
        VIDEO_LINK_STATE: [MessageHandler(Filters.text, get_link)],
    },
    fallbacks=[]
    )

    updater = Updater(token="5522976180:AAFzWAHrgs9T8I1WTG8mwQ9FgHDDe5Cz0hE", use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(conversation_handler)

    start_handler = CommandHandler("start", start)
    dispatcher.add_handler(start_handler)

    help_handler = CommandHandler("help", help)
    dispatcher.add_handler(help_handler)

    summarize_handler = CommandHandler("summarize", summarize)
    dispatcher.add_handler(summarize_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
