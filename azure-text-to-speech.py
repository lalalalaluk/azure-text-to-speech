import os
import azure.cognitiveservices.speech as speechsdk

SPEECH_KEY=""
SPEECH_REGION="eastus"

file_name = "Alpaca_2_1"

# This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)

print(file_name + '.xml')
ssml_string = open(file_name + '.xml', "r", encoding='utf-8').read()
result = synthesizer.speak_ssml_async(ssml_string).get()

stream = speechsdk.AudioDataStream(result)
stream.save_to_wav_file(file_name + ".wav")
