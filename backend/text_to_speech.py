from google.cloud import texttospeech

tts_client = texttospeech.TextToSpeechClient()

def text_to_speech(text, language_code):
    # configure request
    synthesis_input = texttospeech.SynthesisInput(text=text.replace('*', ''))
    # TODO: have users select voice gender
    voice = texttospeech.VoiceSelectionParams(language_code=language_code, ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    # Generate the audio content
    response = tts_client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

    return response.audio_content

def sorry_message_in_language(language_code):
    try:
        with open(f'backend/sorry_{language_code}.mp3', 'rb') as audio_file:
            # return audio bytes
            return audio_file.read()
    except IOError:
        return text_to_speech('Sorry, we do not have any experiences for that location yet', 'en-us')