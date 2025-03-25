import json
from channels.generic.websocket import AsyncWebsocketConsumer

class QueueConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.queue_name = self.scope['url_route']['kwargs']['queue_name']
        await self.channel_layer.group_add(self.queue_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.queue_name, self.channel_name)

    async def queue_update(self, event):
        await self.send(text_data=json.dumps(event["message"]))
