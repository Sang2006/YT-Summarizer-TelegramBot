YT-Summarizer

A chatbot that summarizes YouTube videos. When the chatbot receives a command to summarize a video, it prompts the user to input a YouTube link. It then extracts the video's transcript using the YouTubeTranscriptApi library, and sends the transcript to the OpenAI API to generate a summary of the video. Finally, the chatbot sends the summary back to the user and creates an audio file using the gTTS library.
