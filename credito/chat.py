import openai
import re
import os
def test():
    return "hello"

class chatbot:
    def __init__(self) -> None:
        openai.api_key=os.getenv("api_key")
        self.questionBank = []
        self.suggestionQues=['Check my credit score','What is credit score?','What are credit cards?','How to improve my score?','Requirements for getting a credit card?','How to increase credit limit?','']
    def getAns(self,credit_score: int, num_cards: int, question: str) -> str:
        personal_info = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role":"system", "content":"You are a helpful assistant. Give very short definitive yes or no answers"},
                {"role":"user", "content":"Does the question '"+question+"' require personal information?"}
            ],
            temperature=0.2
        )['choices'][0]['message']['content']

        if(personal_info=="Yes."):
            # print("Personal info detected. resetted")
            message=[
                    {"role": "system", "content": "You are a helpful assistant who gives good credit advice.Give short definitive answers.My credit score is "+str(credit_score)+" and I have "+str(num_cards)+"credit cards."},
                    {"role": "user", "content": question}
                ]
            response =openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=message
            )
            message.append(response['choices'][0]['message'])
            self.questionBank=[message]

        elif re.match(r'^no',personal_info, re.IGNORECASE):
            # print("Personal info NOT detected")
            if len(self.questionBank)==0:
                message=[{"role": "system", "content": "You are a helpful assistant who gives good credit advice.Give short definitive answers.My credit score is "+str(credit_score)+" and I have "+str(num_cards)+"credit cards."}]
            else:
                message=self.questionBank[0]
            message.append({"role": "user", "content": question})
            # print(message)
            response =openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=message
            )
            message.append({"role":"assistant", "content":response['choices'][0]['message']['content']})
            self.questionBank.append(message)
        else:
            return personal_info
        return response['choices'][0]['message']['content']

    def getSuggestions(self, topic: str) -> list[str]:
        response =openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role":"system", "content":"Pick 3 questions from the given list which relate the most to the given topic-\n"+("\n").join(self.suggestionQues)},
                {"role":"user", "content":"credit card"},
                {"role":"assistant", "content":"What are credit cards?,Requirements for getting a credit card?,How to increase credit limit?"},
                {"role": "user", "content":topic}
            ]
            )
        return response['choices'][0]['message']['content'].split(", ")
    
if __name__=="__main__":
    bot = chatbot()
    print(bot.getSuggestions("credit score"))
    