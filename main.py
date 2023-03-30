import openai as ai

# main variables
OPENAI_KEY = "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"
# MODEL_ENGINE = "text-davinci-003"
MODEL_ENGINE = "gpt-3.5-turbo"
# messages = [{"role": "system", "content": "You are a chatbot"}]
messages = []
result = ""

ai.api_key = OPENAI_KEY

# first prompt to start bot
first_prompt = "Please talk to me in english so I can improve my english conversation skills."
first_prompt_dict = {"role": "user", "content": first_prompt}
messages.append(first_prompt_dict)

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

# print bot response
print(bot_response["content"])

# bot main loop
while True:
    # catch user input
    user_input = input("O que gostaria de dizer ao bot:")

    #create user response dictionary and adds it to messages list
    user_response = {"role": "user", "content": user_input}
    messages.append(user_response)

    # process bot response acording to user input
    bot_response = bot(messages).choices
    bot_response = bot_response[len(bot_response) -1]["message"]

    # adds bot response to messages list
    messages.append(bot_response)

    # print bot response
    print(bot_response["content"])


#https://blog.devgenius.io/chatgpt-how-to-use-it-with-python-5d729ac34c0d