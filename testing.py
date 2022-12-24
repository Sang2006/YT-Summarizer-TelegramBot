from urllib.parse import urlparse

video_link =  input('Enter video link : ')

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

# handle the AssertionError
try:
    assert isinstance(video_id, str), "`video_id` must be a string"
except AssertionError:
    print('User did not input a valid url')
    print('Asking the user to input a new url')