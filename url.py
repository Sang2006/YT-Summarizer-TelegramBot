from urllib.parse import urlparse
from tele_bot import get_link

# Replace YOUR_LINK with the YouTube link you want to use
link = 

# Parse the URL and get the video ID
parsed_url = urlparse(link)
query_params = parsed_url.query.split('&')
video_id = None
for param in query_params:
    if param.startswith('v='):
        try:
            video_id = param.split('=')[1]
            break
        except Exception as e:
            print('Something went worng')
            print(e)
            
            
