from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer


bot = ChatBot('cloudworkersbot', read_only=True)
trainer = ChatterBotCorpusTrainer(bot)
trainer.train("chatterbot.corpus.crazy dsite")



#Testing bot
while True:
    request = input("You: ")
    response = bot.get_response(request)
    print('Bot:', response)
