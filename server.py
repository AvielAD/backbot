from aiohttp import web
import chatterbot
import socketio
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import logging
from chatterbot import comparisons, response_selection

logger = logging.getLogger()
logger.setLevel(logging.INFO)

chatbot=None

sio = socketio.AsyncServer(cors_allowed_origins='*')
app = web.Application()
sio.attach(app)

@sio.event
def connect(sid, environ):
    global chatbot
    chatbot = ChatBot(sid,
        storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
        logic_adapters=[
            {
                'import_path': 'chatterbot.logic.BestMatch',
                'statement_comparison_function': comparisons.LevenshteinDistance,
                'response_selection_method': response_selection.get_first_response
            }
        ],
        database_uri='mongodb+srv://chatbot:Test1!@cluster0.or3lf.mongodb.net/test'
    )
    trainer = ChatterBotCorpusTrainer(chatbot)
    trainer.train(
        "./language/spanish"
#        "./language/spanish/comida.yml"
#        "./language/spanish/ai.yml",
#        "./language/spanish/saludos.yml"
    )

@sio.event
async def message(sid, data):
    global chatbot
    snd_message="nothing"
    if( chatbot is not None):
        snd_message=chatbot.get_response(data['message'])
        await sio.emit('response', { 'id': '2', 'name': 'Bot', 'message': str(snd_message) }, room=sid)

@sio.event
async def messageFeedback(sid, data):
    global chatbot
    if ( chatbot is not None):
        chatbot.learn_response(data['correct'], data['statement'])
    print('response added')

@sio.event
def disconnect(sid):
    print("disconect", sid)

if __name__ == '__main__':
    web.run_app(app, port=8080)