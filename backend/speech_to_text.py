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

    return stt_client.recognize(config=config, audio=audio).results
    

class AudioConversion():
    def __init__(self, success, transcript, language_code):
        self.success = success
        self.transcript = transcript
        self.language_code = language_code
        
def get_text_transcript_and_language_code(audio_bytes) -> AudioConversion:
    try:
        text_results = speech_to_text(audio_bytes)
        print(text_results)
        if len(text_results) == 0:
            return AudioConversion(False, "Sorry, we had trouble converting that audio.", 'en-us')
        text_transcript = ''.join([result.alternatives[0].transcript for result in text_results]) # take the most confident text result
        language_code = text_results[0].language_code
        return AudioConversion(True, text_transcript, language_code)
    except InvalidArgument:
        return AudioConversion(False, "Sorry, we had trouble converting that audio.", 'en-us')
    except PermissionDenied:
        return AudioConversion(False, "Sorry, there was a server permissions error.", 'en-us')
    except ResourceExhausted:
        return AudioConversion(False, "Sorry, we've exhausted our resources. Try again later.", 'en-us')        