import wave

import asyncio
import aiohttp
import requests


class Client(object):
    VOICE_END_POINT = 'http://127.0.0.1:8000/ttsapi/voicegens/'
    CLIENT_ID = 'Eixtb3dBKxKL58WScivEdK6QamXVuYBj8KEbDW1H'

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.token = self.issue_token()
        self.auth_header = {'Authorization': 'Bearer {}'.format(self.token)}

    def __str__(self):
        return self.username

    def issue_token(self):
        payload = {
            'client_id': self.CLIENT_ID,
            'grant_type': 'password',
            'username': self.username,
            'password': self.password
        }
        header = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post('http://127.0.0.1:8000/o/token/', data=payload, headers=header)
        return response.json()['access_token']

    def get_voice_list(self):
        response = requests.get(self.VOICE_END_POINT, headers=self.auth_header)
        return response.json()

    def get_detail_of_voice(self, signature):
        detail_end_point = self.VOICE_END_POINT + signature
        response = requests.get(detail_end_point, headers=self.auth_header)
        return response.json()

    def register_voice(self, text, actor, emotion='', prosody=''):
        emotion = str(emotion)
        prosody = str(prosody)
        payload = {
            'text': text,
            'actor': actor,
            'emotion': emotion,
            'prosody': prosody,
            'wavfile': ''
        }
        response = requests.post(self.VOICE_END_POINT, data=payload, headers=self.auth_header)
        return response.json()['signature']

    async def async_generate_voice(self, signature):
        async with aiohttp.ClientSession() as session:
            generate_end_point = self.VOICE_END_POINT + signature + '/generate/'
            async with session.get(generate_end_point, headers=self.auth_header) as response:
                file_name = signature + '.wav'
                wave_file = wave.open(file_name, 'w')
                wave_file.setparams((1, 2, 24000, 0, 'NONE', 'Uncompressed'))
                wave_file.writeframesraw(await response.read())
                wave_file.close()
                print("Generate {}".format(file_name))

    def generate_voice(self, signature):
        task_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(task_loop)
        task_loop.run_until_complete(asyncio.wait([self.async_generate_voice(signature)]))
        task_loop.close()

    async def register_and_generate_voice(self, text, actor, emotion='', prosody=''):
        signature_response = self.register_voice(text, actor, emotion, prosody)
        if signature_response:
            signature = signature_response['signature']
            await self.async_generate_voice(signature)

    # TODO: Determine the parameters
    def generate_voices(self, emotionX, emotionY, actor, *texts):
        task_list = [self.register_and_generate_voice(str_emotion, actor, text) for text in texts]
        task_loop = asyncio.get_event_loop()
        task_loop.run_until_complete(asyncio.wait(task_list))
        task_loop.close()
