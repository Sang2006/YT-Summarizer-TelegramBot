from trans import transcript
import openai


openai.api_key = os.environ['OPEN_AI_API']

model_engine = "text-davinci-003"

stop = '~'
prompt = f"Summarize this YouTube video {transcript}~"
words = prompt.split()
word_count = len(words)

if word_count > 500:
    prompt = ' '.join(words[:500])
    prompt = prompt + '~'

def parse_response(completion):

    summary = completion['choices'][0]['text']
    return summary

try:
    completion = openai.Completion.create(engine=model_engine, prompt=prompt, max_tokens=200, stop=stop)
    #print(completion)
    summary = parse_response(completion)
    print(summary)
except Exception as e:
    print('Something went wrong')
    print(e)
