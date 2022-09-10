from flask import Flask, render_template, request
from chatterbot import ChatBot, logic
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer

app = Flask(__name__)

# 'chatterbot.logic.BestMatch', 'chatterbot.logic.MathematicalEvaluation'
#   logic_adapter=[
#       logic.TimeLogicAdapter
#   ],
CHATBOT_NAME = "Evy"
time_positive = ['what is the time right now', 'time', 'clock', 'what is the current time', 'what is the time now', 'what’s the time', 'what time is it',
                 'what time is it now', 'do you know what time it is', 'could you tell me the time, please', 'what is the time', 'will you tell me the time',
                 'tell me the time', 'time please', 'show me the time', 'what is time', 'whats on the clock', 'show me the clock',
                 'what is the time', 'what is on the clock', 'tell me time', 'time', 'clock', ]

time_negative = ['what are you doing', 'what’s up', 'when is time', 'who is time' 'could you', 'do you', 'what’s', 'will you', 'tell me', 'show me', 'current', 'do', 'now',
                 'will', 'show', 'tell', 'me', 'could', 'what', 'whats', 'i have time', 'who', 'who is', 'hardtime', 'when', 'what is', 'how',
                 'how is', 'when is', 'who is time', 'how is time', 'how is time', 'when is time']


chatbot = ChatBot(CHATBOT_NAME, storage_adapter='chatterbot.storage.SQLStorageAdapter',
                  logic_adapters=[
                      {
                          'import_path': 'chatterbot.logic.BestMatch',
                          'default_response': 'I am sorry, My responses are limited.',
                          'maximum_similarity_threshold': 0.7
                      },
                      {
                          'import_path': 'chatterbot.logic.TimeLogicAdapter',
                          'positive': time_positive,
                          'negative': time_negative,
                          'maximum_similarity_threshold': 0.8
                      }
                  ])

trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.english")

trainer.train("./data/small_talk.yml")

manualTrainer = ListTrainer(chatbot)

manualTrainer.train(["What is your name", f"My name is {CHATBOT_NAME}"])


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/chat")
def bot_response():
    message = request.args.get('message')
    print(message)
    return str(chatbot.get_response(message))


if (__name__ == "__main__"):
    app.run()
