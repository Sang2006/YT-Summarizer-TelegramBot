from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from telegram import Bot
from urllib.parse import urlparse
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled
import openai
from gtts import gTTS
import os
from googleapiclient.discovery import build
import requests


bot = Bot(token= os.environ['BOT_TOKEN'])
VIDEO_LINK_STATE = 1
video_link = ''

def main():
    # Start
    def handle_transcripts_disabled(update, context):
        """Handle the TranscriptsDisabled error."""
        error = context.error
        if isinstance(error, TranscriptsDisabled):
            chat_id = update.effective_chat.id
            print("This video does not support transcript")
            print("Asking the user to input a valid url...")
            context.bot.send_message(chat_id=chat_id, text="Sorry, we were unable to retrieve a transcript for this video.")
            context.bot.send_message(chat_id=chat_id, text="Please make sure that subtitles are enabled for this video and try again.")

    def handle_assertion_error(update, context):
        """Handle an Assertion error"""
        error = context.error
        if isinstance(error, AssertionError):
            chat_id = update.effective_chat.id
            print("An Assertion Error has occurred")
            print("Asking the user to input a valid url...")
            context.bot.send_message(chat_id=chat_id, text="Sorry, the link you provided is not a valid YouTube link.")
            context.bot.send_message(chat_id=chat_id, text="Please check the link and try again.")
    
    def start(update, context):
        chat_id = update.effective_chat.id
        context.bot.send_message(chat_id=chat_id, text="Hello I'm a YouTube video summarizer bot!\n\nPlease select an option.\n\n/start\n/help\n/summarize\n\nIf you want to stop using the bot type /cancel at any point")

    def help(update, context):
        chat_id = update.effective_chat.id
        context.bot.send_message(chat_id=chat_id, text="This is a chatbot that summarizes YouTube videos. When the chatbot receives a command to summarize a video, it prompts the user to input a YouTube link. It then extracts the video's transcript using the YouTubeTranscriptApi library, and sends the transcript to the OpenAI API to generate a summary of the video. Finally, the chatbot sends the summary back to the user and creates an audio file using the gTTS library.\n\nCoded by - Sangeeth\nE-mail - sangeethudayanga123@gmail.com\nTelegram - @SangeethKarasinghe")

    def summarize(update, context):
        chat_id = update.effective_chat.id
        context.bot.send_message(chat_id=chat_id, text= "Please enter a YouTube link")

        return VIDEO_LINK_STATE

    def get_link(update, context):
        chat_id = update.effective_chat.id
        video_link = update.message.text

        if video_link == '/cancel':
            update.message.reply_text('Conversation canceled.')
            return ConversationHandler.END

        # getting the video id
        parsed_url = urlparse(video_link)
        query_params = parsed_url.query.split('&')
        video_id = None

        if parsed_url.netloc == 'youtu.be':
            video_id = parsed_url.path.split('/')[-1]
            print(f"Video link : {video_link}")
            print(f"Video id : {video_id}")
        else:
            for param in query_params:
                if param.startswith('v='):
                    try:
                        video_id = param.split('=')[1]
                        # ensure that video_id is a string
                        video_id = str(video_id)
                        print(f"Video link : {video_link}")
                        print(f"Video id : {video_id}")
                        break
                    except Exception as e:
                        print('Something went wrong')
                        print(e)
        
        chat_id = update.effective_chat.id

        # getting the trascript
        data = YouTubeTranscriptApi.get_transcript(video_id)
        
        # if yes continue
        
        transcript = ""
        for d in data:
            transcript += d['text'] + " "

        # summarizing
        openai.api_key = os.environ['OPEN_AI_API']

        model_engine = "text-davinci-003"

        stop = '~!?`'
        prompt = f"Summarize this YouTube video and please ignore any sponsor segments and ignore any self promotions{transcript}~!?`"
        words = prompt.split()
        word_count = len(words)

        if word_count > 500:
            prompt = ' '.join(words[:500])
            prompt = prompt + '~'

        def parse_response(completion):

            summary = completion['choices'][0]['text']
            return summary

        try:
            print('Generating summary...')
            sum_mes = context.bot.send_sticker(chat_id, 'CAACAgIAAxkBAAEHAbNjqSWVYVI1RgovTHecuzzfpUbmvwACBgADwDZPE8fKovSybnB2LAQ')
            completion = openai.Completion.create(engine=model_engine, prompt=prompt, max_tokens=200, stop=stop)
            #print(completion)
            summary = parse_response(completion)
            print(summary)
            api_key = os.environ['YOUTUBE_API_KEY']
            youtube = build('youtube', 'v3', developerKey=api_key)
            
            # getting the title
            def get_video_title(video_id):
                request = youtube.videos().list(part="snippet", id=video_id)
                response = request.execute()
                
                title = response['items'][0]['snippet']['title']
                return title
            
            # calling the function
            title = get_video_title(video_id)
            
        except Exception as e:
            print('Something went wrong')
            print(e)
            context.bot.send_message(chat_id=chat_id, text='An internal error has occured!\nPlease contact @SangeethKarasinghe for help.')

        # sneding summary to the user
        sending_sum = f"{title}\n\n{summary}"
        message_id = sum_mes.message_id
        bot.delete_message(chat_id=chat_id, message_id=message_id)
        # getting the youtube thumbnail
        response = requests.get(f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg")
        if response.status_code == 200:
            image_data = response.content
        
        with open("thumbnail.jpg", "wb") as image:
            image.write(image_data)
        
        with open('thumbnail.jpg', 'rb') as photo:
            context.bot.send_photo(chat_id=chat_id, photo=photo, caption=sending_sum)
            
        os.remove('thumbnail.mp3')

        # Generating an audio file    
        tts_text = summary
        tts = gTTS(tts_text)
        tts.save("summary.mp3")
        with open('summary.mp3', 'rb') as f:
            context.bot.send_audio(chat_id=chat_id, audio=f)
        print('Uploaded audio file')
        os.remove('summary.mp3')
        print('Audio file deleted')
        return ConversationHandler.END

    def cancel(update, context):
        update.message.reply_text('Conversation canceled.')
        return ConversationHandler.END

    conversation_handler = ConversationHandler(
    entry_points=[CommandHandler("summarize", summarize)],
    states={
        VIDEO_LINK_STATE: [MessageHandler(Filters.text, get_link)],
    },
    fallbacks=[CommandHandler('cancel', cancel)]
    )

    updater = Updater(token=os.environ['BOT_TOKEN'], use_context=True)
    dispatcher = updater.dispatcher
    
    dispatcher.add_error_handler(handle_assertion_error, AssertionError) # Error handler for assertion error

    dispatcher.add_handler(conversation_handler)

    dispatcher.add_error_handler(handle_transcripts_disabled, TranscriptsDisabled) # Error handler for transcript disabled

    start_handler = CommandHandler("start", start)
    dispatcher.add_handler(start_handler)

    help_handler = CommandHandler("help", help)
    dispatcher.add_handler(help_handler)

    summarize_handler = CommandHandler("summarize", summarize)
    dispatcher.add_handler(summarize_handler)

    cancel_handler = CommandHandler("cancel", cancel)
    dispatcher.add_handler(cancel_handler)

    print('Successfully started the bot :D')
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
