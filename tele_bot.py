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
        context.bot.send_message(chat_id=chat_id, text="This is a chatbot that summarizes YouTube videos. When the chatbot receives a command to summarize a video, it prompts the user to input a YouTube link. It then extracts the video's transcript using the YouTubeTranscriptApi library, and sends the transcript to the OpenAI API to generate a summary of the video. Finally, the chatbot sends the summary back to the user and creates an audio file using the gTTS library.")

    def summarize(update, context):
        chat_id = update.effective_chat.id
        context.bot.send_message(chat_id=chat_id, text= "Please enter a YouTube link")

        return VIDEO_LINK_STATE

    def get_link(update, context):
        chat_id = update.effective_chat.id
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
                    print(f"Video link : {video_link}")
                    print(f"Video id : {video_id}")
                    break
                except Exception as e:
                    print('Something went worng')
                    print(e)
            elif AssertionError:
                print('User did not input a valid url')
                print('Asking the user to input a new url')
                context.bot.send_message(chat_id=chat_id, text=f"'{video_link}' is not a valid YouTube link!")
                context.bot.send_message(chat_id=chat_id, text='Please check the link and try again')
        chat_id = update.effective_chat.id

        # getting the trascript
        data = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = ""
        for d in data:
            transcript += d['text'] + " "

        # summarizing
        openai.api_key = "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"

        model_engine = "text-davinci-003"

        stop = '~!?`'
        prompt = f"Summarize this YouTube video and please ignore any sponsor segments{transcript}~!?`"
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
            print('Generating summary...')
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
        print('Uploaded audio file')
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

    print('Successfully started the bot :D')
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
