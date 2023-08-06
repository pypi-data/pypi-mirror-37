"""Module for the client of Prosody TTS API."""
import asyncio

import aiohttp
import requests

from prosody.util import server_required
from prosody.voice_item import Voice


class Client():
    """Client of Prosody TTS API.

    A Client object provides a user with the python programming interface of REST API
    including CRUD operations. This object internally saves Voice objects which is
    an abstraction of the voice item of the actual TTS API.

    Attributes:
        repository: A dictionary (signature: str, voice_item: Voice) of Voice objects.
        VOICE_END_POINT: A string constant indicating the main endpoint of the API.
        TOKEN_END_POINT: A string constant indicating the token issuing endpoint of the API.
        CLIENT_ID: A string constant indicating the OAuth2 client id of the API.
        username: A string containing username of a user.
        password: A string containing password of a user.
        token: A string of issued OAuth2 token.
        auth_header: A dictionary which is used as a HTTP header for the authentication.
    """
    repository = {}
    SERVER_URL = 'https://tts.humelo.com/ttsapi/'

    DEBUG = False
    if DEBUG:
        SERVER_URL = 'http://127.0.0.1:8000/ttsapi/'

    VOICE_END_POINT = SERVER_URL + 'voicegens/'
    TOKEN_END_POINT = SERVER_URL + 'token/'

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.token = self.issue_token()
        self.auth_header = {'Authorization': 'Token {}'.format(self.token)}
        self.list_voice()

    def __str__(self):
        template = 'username: {}\ncontents: {}'
        contents = ''
        for _, voice in self.repository.items():
            contents += '\n\n'
            contents += str(voice)
        return template.format(self.username, contents)

    @server_required
    def issue_token(self):
        """Issues a new token using username and password.

        Returns:
            A string of issued OAuth2 token.

        Raises:
            ValueError: An error occurred during token-issuing procedure.
            ConnectionError: An error occurred during connecting to the API server.
        """
        payload = {
            'username': self.username,
            'password': self.password
        }
        response = requests.post(self.TOKEN_END_POINT, data=payload)
        token = response.json().get('token', '')
        if not token:
            raise ValueError('Authentication Failed.')
        return response.json()['token']

    @server_required
    def list_voice(self):
        """Fetches voice items from database and save them as Voice objects.

        Returns:
            Saves a list of Voice objects in `repository` attribute, and returns it.
        """
        if not self.repository:
            response = requests.get(self.VOICE_END_POINT, headers=self.auth_header).json()
            for voice in response['results']:
                new_voice = Voice(
                    voice['text'],
                    voice['actor'],
                    emotion=voice['emotion'],
                    prosody=voice['prosody'],
                    signature=voice['signature'],
                )
                self.repository[new_voice.signature] = new_voice
        return self.repository

    @server_required
    def remove_voice(self, voice_item):
        """Removes a voice item from database and `repository`.

        Args:
            voice_item: A Voice object or the signature of the Voice object
                which user wants to remove.
        """
        signature = voice_item
        if isinstance(voice_item, Voice):
            signature = voice_item.signature
        if signature not in self.repository:
            raise KeyError('The voice does not exist in the voice list.')
        signature += '/'
        detail_end_point = self.VOICE_END_POINT + signature
        requests.delete(detail_end_point, headers=self.auth_header)
        del self.repository[signature]

    @server_required
    def update_voice(self, voice_item: Voice):
        """Updates contents of a Voice item and applies it to the database.

        Args:
            voice_item: A Voice object a user wants to update.
        """
        if not voice_item.modified:
            raise NoChangeError('There is no change in the Voice object.')
        detail_end_point = self.VOICE_END_POINT + voice_item.signature + '/'
        requests.put(detail_end_point, headers=self.auth_header, data=voice_item.payload)
        voice_item.modified = False

    @server_required
    def register_voice(self, voice_item: Voice):
        """Registers a new Voice to the inner dictionary and the database.

        A user passes a new Voice objects to this method, then it gets a `signature`
        from API, and saves the signature to the Voice object.

        Args:
            voice_item: A Voice object which is to be registered.

        Returns:
            The registered Voice object.
        """
        if voice_item.registered:
            err = 'This voice has already been registered. How about call `update_voice()` instead?'
            raise VoiceAlreadyRegisteredError(err)
        payload = voice_item.payload
        response = requests.post(self.VOICE_END_POINT, data=payload, headers=self.auth_header)
        voice_item.register(response.json()['signature'])
        self.repository[voice_item.signature] = voice_item
        return voice_item

    @server_required
    async def generate_voice_helper(self, voice_item: Voice, auto_register=False):
        """A coroutine which generates actual WAV file from a registered Voice object.

        Calls GET method to the generation endpoint asynchronously, and saves generated WAV data
        to `voice_item.wavfile`.
        """
        if not voice_item.registered:
            if auto_register:
                voice_item = self.register_voice(voice_item)
            else:
                raise VoiceNotRegisteredError('This voice is not registered yet.')
        if voice_item.wavfile and not voice_item.modified:
            raise NoChangeError('There is already a WAV file for it.')
        async with aiohttp.ClientSession() as session:
            generate_end_point = self.VOICE_END_POINT + voice_item.signature + '/generate/'
            async with session.get(generate_end_point, headers=self.auth_header) as response:
                voice_item.wavfile = await response.read()

    def generate_voice(self, voice_item: Voice, auto_register=False):
        """Create an async loop for generating WAV for a registered Voice object."""
        task_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(task_loop)
        task_loop.run_until_complete(asyncio.wait([self.generate_voice_helper(voice_item, auto_register)]))
        task_loop.close()

    def generate_voice_multiple(self, list_of_voices, auto_register=False):
        """Create an async loop for generating WAV for multiple unregistered Voice objects."""
        if not list_of_voices:
            raise ValueError('`list_of_voices` should not be empty.')
        task_list = [self.generate_voice_helper(voice, auto_register) for voice in list_of_voices]
        task_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(task_loop)
        task_loop.run_until_complete(asyncio.wait(task_list))
        task_loop.close()


### Exceptions


class VoiceAlreadyRegisteredError(Exception):
    """Raise an exception when a user tries to register an already registered voice."""
    pass


class VoiceNotRegisteredError(Exception):
    """Raise an exception when a user tries to generate a voice which is not registered."""
    pass


class NoChangeError(Exception):
    """Raise an exception when a user tries to update a Voice while there is no change."""
    pass
