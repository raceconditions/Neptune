#!/usr/bin/env python
from os import environ, path

from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *
import pyaudio
import speechhandler

MODELDIR = "/usr/local/share/pocketsphinx/model"
CUSTOMMODELDIR = "model"
DATADIR = "test/data"

# Create a decoder with certain model
config = Decoder.default_config()
config.set_string('-hmm', path.join(MODELDIR, 'en-us/en-us'))
config.set_string('-lm', path.join(CUSTOMMODELDIR, '4743.lm.bin'))
config.set_string('-dict', path.join(CUSTOMMODELDIR, '4743.dic'))
decoder = Decoder(config)

# Decode streaming data.
decoder = Decoder(config)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
stream.start_stream()

in_speech_bf = False
decoder.start_utt()
while True:
    buf = stream.read(1024)
    if buf:
        decoder.process_raw(buf, False, False)
        if decoder.get_in_speech() != in_speech_bf:
            in_speech_bf = decoder.get_in_speech()
            if not in_speech_bf:
                decoder.end_utt()
                speechhandler.handleSpeech(decoder.hyp().hypstr)
                decoder.start_utt()
    else:
        break
decoder.end_utt()


