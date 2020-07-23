#Python libraries that we need to import for our bot
import random
from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)
ACCESS_TOKEN = 'EAAJ8sJvUO8IBABkbo77prvxuplvAhikHVBF8aYoeUNcPLZCnMOZBa6PfvIEJsY3JNeujZC7JuoQ6wzZBFYaJC8p7GOTiJ0VYzIoXoPG6PoSpZCxwMOQQf0p8vJIPkiFJCOKSAqj7uwdfOl42e7um4lxLnAGikmGKEyVugZAY15HPV5Y0oYL8gZCe2u48odHuCMZD'
VERIFY_TOKEN = 'TESTINGTOKEN'
bot = Bot(ACCESS_TOKEN)

#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
       output = request.get_json()
       print(output)
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                message_text = message['message'].get('text')
                if message_text:
                    response_sent_text = get_message(recipient_id, message_text)
                    # send_message(recipient_id, response_sent_text)
                #if user sends us a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    response_sent_nontext = get_message(recipient_id, message_text)
                    # send_message(recipient_id, response_sent_nontext)
    return "Message Processed"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

def Story(recipient_id):

    story = 'Hay un muchacho. Muchacho means boy.'
    part2 = 'Question (pregunta): How do you say boy en español? ¿Muchacho o muchacha?'

    return send_message(recipient_id,story),send_message(recipient_id,part2)

def instructions(recipient_id):
    response = 'Sometimes I’m going to tell you things and sometimes I’m going to ask you things. It’s okay if you don’t know all of the words. You’ll get a lot of repeticiones. That’s repetitions. Also you’ll notice that many words are the same or similar in English and Spanish like chocolate 🍫 televisión 📺 and música 🎶'
    return send_message(recipient_id, response)

#chooses a random message to send to the user
def get_message(recipient_id,text):
    sample_responses = ["Hola. Me llamo Shannon. Soy tu profesora.  That means I’m your teacher", 
    "We're proud of you.", "Keep on being you!", "We're greatful to know you :)"]
    print(text)
    if text == 'Yes' or text == 'yes':
        return send_message(recipient_id,'Today I’m going to tell you a story (un cuento). Is that okay? ¿Sí o no?')
    elif text == 'Si' or text == 'si':
        return send_message(recipient_id,'Fantástico!'),instructions(recipient_id),Story(recipient_id)
    elif text == 'no' or text == 'No':
        return send_message(recipient_id,'está bien. That’s okay. Let’s start whenever you’re ready')
    elif text == 'muchacho' or text == 'Muchacho':
        return send_message(recipient_id,'sí: ¡Excelente! You answered your first question! Sí. Hay un muchacho')
    elif text == 'muchacha' or text == 'Muchacha':
        return send_message(recipient_id,'try again. ¿Muchacho o muchacha?')

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run()