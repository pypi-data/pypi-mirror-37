#  prosody

Python Prosody API: Emotion & Prosody sensitive TTS

## How To Use
### Installing

Install prosody using pip
```
python -m pip install prosody
```

### Creating a Client

From `prosody_api` package import `Client` class, then create a Client object with your valid username and password.
```python
from prosody.prosody_api import Client

cli = Client('your_id', 'your_password')
```

### Creating a Voice Item

In order to create a Voice item, which is needed for API server to generate actual WAV file, import `Voice` class from `voice_item` package and create an instance of `Voice` class.
There are five public attributes in `Voice` class, two of them are necessary, and the rest is optional.

#### Required Attributes
1. `text`: The text user wants to convert to a WAV file.
2. `actor`: User can choose the actor of generated voice.

#### Optional Attributes
1. `emotion`
2. `prosody`
3. `signature`: Users cannot set an arbitrary signature on their own. After registering the Voice, the server will automatically give a signature.

```python
from prosody.prosody_api import Client
from prosody.voice_item import Voice

# Creating a new client and a new Voice object.
cli = Client('your_id', 'your_password')
new_voice = Voice('안녕하세요', 'lady1')
registered_voice = cli.register_voice(new_voice)

# Updating the Voice object.
registered_voice.text = '반갑습니다'
cli.update_voice(registered_voice)

# Removing the Voice object.
cli.remove_voice(registered_voice)
```

### Generating WAV File
Then, you can call `generate_voice` to create actual WAV file.

```python
cli.generate_voice(registered_voice)
```

## Authors

* **Yuneui Jeong** - *Main contributor* - [laviande22](https://github.com/laviande22)
* **Suwon Shin** - *Boilerplates* - [shh1574](https://github.com/shh1574)
