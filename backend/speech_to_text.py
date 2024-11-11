from google.cloud import speech
from google.api_core.exceptions import InvalidArgument, PermissionDenied, ResourceExhausted

stt_client = speech.SpeechClient()

def speech_to_text(audio_bytes):

    '''
    config = speech.RecognitionConfig(
        language_code="en",
    )
    '''

    config = speech.RecognitionConfig(
        language_code='en-US',
        alternative_language_codes=["es-ES", "fr-FR", "zh-CN"],
    )

    audio = speech.RecognitionAudio(
        content=audio_bytes,
    )

    try:
        return stt_client.recognize(config=config, audio=audio)
    except InvalidArgument:
        return "Sorry, there was a server error processing that audio."
    except PermissionDenied:
        return "Sorry, there was a server permissions error."
    except ResourceExhausted:
        return "Sorry, we've exhausted our resources. Try again later."