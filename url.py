from urllib.parse import urlparse

# getting the video id
video_link = input('Please enter your link : ')
parsed_url = urlparse(video_link)
query_params = parsed_url.query.split('&')
global video_id
video_id = None
for param in query_params:
    if param.startswith('v='):
        try:
            video_id = param.split('=')[1]
            # Ensure that video_id is a string
            video_id = str(video_id)
            print(f"Video link : {video_link}")
            print(f"Video id : {video_id}")
            break
        except Exception as e:
            print('Something went wrong')
            print(e)
    # else:
    #     try:
    #         video_id = video_link[17:]
    #         print(f"Video link : {video_link}")
    #         print(f"Video id : {video_id}")
    #         break
    #     except Exception as e:
    #         print('Something went wrong')
    #         print(e)
            
 
