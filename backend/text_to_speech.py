from google.cloud import texttospeech

tts_client = texttospeech.TextToSpeechClient()

def text_to_speech(text):
    # configure request
    synthesis_input = texttospeech.SynthesisInput(text=text)
    # TODO: have users select voice gender
    voice = texttospeech.VoiceSelectionParams(language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    # Generate the audio content
    response = tts_client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

    return response.audio_content