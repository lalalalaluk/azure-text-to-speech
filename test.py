# pip install azure-cognitiveservices-speech
import azure.cognitiveservices.speech as speechsdk

def text_to_speech(subscription_key, region, text, output_file):
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    result = synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        stream = speechsdk.AudioDataStream(result)
        stream.save_to_wav_file(output_file)
        print(f"Audio file saved to {output_file}.")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speechsdk.SpeechSynthesisCancellationDetails(result)
        print(f"Speech synthesis canceled: {cancellation_details.reason}")

if __name__ == "__main__":
    subscription_key = "YOUR_SUBSCRIPTION_KEY_HERE"
    region = "YOUR_REGION_HERE"
    text = "Hello, this is a demo of text-to-speech using Azure Speech Services."
    output_file = "output.wav"

    text_to_speech(subscription_key, region, text, output_file)