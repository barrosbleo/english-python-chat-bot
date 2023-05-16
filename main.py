import openai as ai
import pyttsx3 as tts
import speech_recognition as sr

# main variables
OPENAI_KEY = "PLACE YOUR KEY HERE"
MODEL_ENGINE = "gpt-3.5-turbo"
messages = [
    {"role": "system", "content": "You are a chatbot made to help me learn English. You should talk with me so I can improve my English conversation skills. You should also start the conversation, considering that we just met at the street."},
    ]
result = ""

ai.api_key = OPENAI_KEY

engine = tts.init()

rate = engine.getProperty('rate')
engine.setProperty('rate', 125)
volume = engine.getProperty('volume')
engine.setProperty('volume', 1.0)
voices = engine.getProperty('voices')
# print(voices)
# exit()
engine.setProperty('voice', voices[1].id)

recognizer = sr.Recognizer()

# bot process function
def bot(messages):
    response = ai.ChatCompletion.create(
        model = MODEL_ENGINE,
        messages = messages,
        max_tokens = 1024,
        n = 1,
        stop = None,
        temperature = 0.5,
        top_p = 1
    )
    return response

# runs first bot iteration and catch the last message
bot_response = bot(messages).choices
bot_response = bot_response[len(bot_response) - 1]["message"]

# add bot response to messages list
messages.append(bot_response)

# print bot response and start speaking to the user'
print(bot_response["content"])
engine.say(bot_response["content"])
engine.runAndWait()
engine.stop()

# bot main loop
while True:

    # recognize speech
    try:
        # catch user speech
        # user_input = input("O que gostaria de dizer ao bot:")
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.7)

            print("Diga algo ao bot:")
            audio = recognizer.listen(source)

            #recognize text
            vtt = recognizer.recognize_google(audio, language='pt-BR')

            #create user response dictionary and adds it to messages list
            user_response = {"role": "user", "content": vtt}
            messages.append(user_response)
    except sr.UnknownValueError:
        print("Não foi possível reconhecer o que disse!")
    except sr.RequestError as err:
        print("Error: {0}".format(err))

    # process bot response acording to user input
    bot_response = bot(messages).choices
    bot_response = bot_response[len(bot_response) -1]["message"]

    # adds bot response to messages list
    messages.append(bot_response)

    # print bot response
    # print(bot_response["content"])
    engine.say(bot_response["content"])
    engine.runAndWait()
    engine.stop()
