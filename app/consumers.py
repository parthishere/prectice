import base64
from channels.generic.websocket import AsyncWebsocketConsumer
import cv2
import numpy as np
from PIL import Image

import asyncio


class FaceConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        print("Connected")
        await self.accept()
        
    async def disconnect(self, close_code):
        print('Disconnected!', close_code)
        
    async def receive(self, text_data):
        print(text_data)
        # print(text_data.get_audio_track())
        # print(type(bytes_data))
        # a = base64.b64decode(bytes_data)
        # jpg_original = base64.b64decode(text_data)
        # print(jpg_original)
        # jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
        # print(jpg_as_np)
        # img  = Image.fromarray(jpg_as_np.astype(np.uint8))
        # img = cv2.imdecode(jpg_as_np, flags=1)
        # print(img)
        # cv2.imshow('./0.jpg', jpg_as_np)
        # img = cv2.imdecode(nparr, flags=1)
        
        # cv2.imshow("win", img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # cv2.waitKey(1)
        # print(a)
        # cv2.imshow("frame" ,a)
        