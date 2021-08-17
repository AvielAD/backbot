from chatbot import chatbot
from chatterbot.trainers import ChatterBotCorpusTrainer

trainer = ChatterBotCorpusTrainer(chatbot)

trainer.train(
        "chatterbot.corpus.english"
)


while(KeyboardInterrupt):
    question = input("question: ")
    response = chatbot.get_response(question)
    print(response)

SystemExit




