import requests

# Send a request to the URL
video_id = '7yyjFudHYuw'
response = requests.get(f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg")

# Check that the request was successful
if response.status_code == 200:
  # Retrieve the image data
  image_data = response.content
  
  # Save the image data to a file
  with open("image.jpg", "wb") as f:
    f.write(image_data)

