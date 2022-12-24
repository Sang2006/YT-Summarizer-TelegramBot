from urllib.parse import urlparse

video_id = None
video_link =  input('Enter video link : ')

parsed_url = urlparse(video_link)
query_path = parsed_url.path.split('/')

netloc = parsed_url.netloc

if netloc == 'youtu.be':
    youtube_video = True
else:
    youtube_video = False
    
if youtube_video == True:
    video_id = query_path[1]
    print('This is a valid YoutTube link!')
    print(video_id)
    
try:
    assert isinstance(video_id, str), "`video_id` must be a string"
except AssertionError:
    print('User did not input a valid url')
    print('Asking the user to input a new url')