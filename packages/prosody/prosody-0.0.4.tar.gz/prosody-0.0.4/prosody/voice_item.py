"""Abstract & validate voice items."""
import wave


class Voice():
    """Class for a single voice item."""
    payload = {}
    wavfile = None

    def __init__(self, text, actor, emotion='', prosody='', signature=''):
        self.text = text
        self.actor = actor
        self.emotion = emotion
        self.prosody = prosody
        self.signature = signature
        self.registered = False
        self.modified = False
        if self.signature:
            self.registered = True

    def register(self, signature):
        """After registering a voice item, save the signature for it."""
        self.signature = signature
        self.registered = True
        self.modified = False

    # TODO: Fix save_wav()
    def save_wav(self):
        """Saves the generated WAV to an actual WAV file."""
        filename = self.signature + '.wav'
        wavfile = wave.open(filename, 'w')
        wavfile.setparams((1, 2, 24000, 0, 'NONE', 'Uncompressed'))
        wavfile.writeframesraw(self.wavfile)
        wavfile.close()
        print('Generated {}'.format(filename))

    def __setattr__(self, name, value):
        self.validate(name, value)
        super().__setattr__(name, value)
        if name in ('text', 'actor', 'emotion', 'prosody', 'signature'):
            self.payload[name] = str(value)
        if name not in ('registered', 'modified'):
            self.modified = True

    def __str__(self):
        template = 'text: {}\nactor: {}\nemotion: {}\nprosody: {}\nsignature: {}'
        return template.format(self.text, self.actor, self.emotion, self.prosody, self.signature)

    @staticmethod
    def validate(name, value):
        """Voice validator"""
        # Type-check.
        if name in ('text', 'actor', 'signature'):
            assert isinstance(value, str)
        elif name in ('emotion', 'prosody'):
            assert isinstance(value, list) or value == ''
        # text
        if name == 'text':
            assert len(value) <= 50
