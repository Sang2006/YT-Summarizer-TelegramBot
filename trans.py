from url import video_id
from youtube_transcript_api import YouTubeTranscriptApi

data = YouTubeTranscriptApi.get_transcript(video_id)

transcript = ""
for d in data:
    transcript += d['text'] + " "

# for element in data:
#     print(element['text'])