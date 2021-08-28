from aiohttp import web
import socketio
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

chatbot=None

sio = socketio.AsyncServer(cors_allowed_origins='*')
app = web.Application()
sio.attach(app)

@sio.event
def connect(sid, environ):
    global chatbot
    chatbot = ChatBot(sid, logic_adapters=[
        "chatterbot.logic.BestMatch"
    ])
    trainer = ChatterBotCorpusTrainer(chatbot)
    trainer.train(
        "./language/spanish"
    )

@sio.event
async def message(sid, data):
    global chatbot
    snd_message="nothing"
    if( chatbot is not None):
        snd_message=chatbot.get_response(data['message'])
        await sio.emit('response', { 'id': '2', 'name': 'Bot', 'message': str(snd_message) }, room=sid)

@sio.event
def disconnect(sid):
    print("disconect", sid)

if __name__ == '__main__':
    web.run_app(app, port=8080)