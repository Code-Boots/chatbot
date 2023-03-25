from fastapi import FastAPI
from chatbot.chat import chatbot

app = FastAPI()


@app.post("/suggestions/")
def suggestions(suggestion: str):
    bot = chatbot()
    return bot.getSuggestions(suggestion)


@app.post("/answer/")
def answers(question: str, credit_score: int, num_card: int):
    bot = chatbot()
    return bot.getAns(credit_score, num_card, question)
