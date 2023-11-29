from telegram.ext import CommandHandler,MessageHandler,ContextTypes,Application,filters
from telegram import Update
from typing import final
import requests
from openai import OpenAI

URL = "https://livescore-api.com/api-client/scores/live.json?key=Ui1fExCJ0iBWkL5s&secret=pg2U1DmxCTvil2LglNvZl8JlrkhM5mfv&competition_id=244" 



import os
    

API_KEY = os.getenv('OPENAIKEY')
client = OpenAI(api_key=API_KEY)
BOTUSERNAME = 'xander_helper_atp_bot'
messages = [{'role':'system','content':'you are a cool but intelligent classmate'}]

async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):
    start_text = "Hello how is life at the ATP going? tell me your difficulty and i will help you or press the /scores command to know what happened in the premier league"
    await update.message.reply_text(start_text)

def api_scores():
    data = requests.get(URL)
    data = data.json()
    n_matches = len(data['data']['match'])
    home_teams = []
    away_teams = []
    scores = []

    matches = data['data']['match']
    #print(matches[1]['away_id'])

    formatted_scores = []

    for i in range(n_matches):
        home_teams.append(matches[i]['home_name'])

    for i in range(n_matches):
        away_teams.append(matches[i]['away_name'])

    for i in range(n_matches):
        scores.append(matches[i]['score'])

    for i in range(n_matches):
        temp = home_teams[i] + " " + scores[i] + " " + away_teams[i] + " "
        formatted_scores.append(temp) 
    f ='Here are the live scores for the latest UCL matches \n\n'
    for i in range(n_matches):
        f = f + formatted_scores[i]+ "\n"
    return f    


async def scores(update:Update,context:ContextTypes.DEFAULT_TYPE):
    text:str = api_scores()
    await update.message.reply_text(text)

async def handle_response(message:str):
    if "what is les ap" in message:
        reply = "CFP les ap is a professional forming school at draggage yaounde. They have a variety of courses."
        return reply
    if "scores" in message:
        reply = api_scores()    
        return reply

    else:
        messages.append(
            {'role':'user','content':message}
        )
        chat = client.chat.completions.create(
            model = 'gpt-3.5-turbo',
            messages=messages
        )

        reply = chat.choices[0].message.content
        return reply

async def handle_message(update:Update,context:ContextTypes.DEFAULT_TYPE):
    message_type:str = update.message.chat.type
    text:str = update.message.text

    if message_type == 'group':
        if BOTUSERNAME in text:
            new_text:str = text.replace(BOTUSERNAME,'').strip()
            response:str = handle_response(new_text)
        else:
            return
    else:
        response:str = handle_response(text)
    
    await update.message.reply_text(await response)


async def error(update:Update,context:ContextTypes.DEFAULT_TYPE):
    print(f"Update{update} caused the error {context.error}")


def main():
    print('start polling...')

    TOKEN = os.getenv('BOTAPIKEY')
    app = Application.builder().token(TOKEN).read_timeout(35).write_timeout(20).build()

    #commands
    app.add_handler(CommandHandler('start',start))
    app.add_handler(CommandHandler('scores',scores))

    #messages
    app.add_handler(MessageHandler(filters.TEXT,handle_message))

    #error
    app.add_error_handler(error)

    print('Polling...')
    app.run_polling(poll_interval=3)

if __name__ == '__main__':
    main()