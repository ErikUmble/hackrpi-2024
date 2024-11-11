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
    
    
def get_text_transcript_and_language_code(audio_bytes):
    try:
        text_results = speech_to_text(audio_bytes)
        print(text_results)
        if len(text_results) == 0:
            return {
                'success': False,
                'transcript': "Sorry, we had trouble converting that audio.",
                'language': 'en-us',
            }
        text_transcript = ''.join([result.alternatives[0].transcript for result in text_results]) # take the most confident text result
        language_code = text_results[0].language_code
        return {
            'success': True,
            'transcript': text_transcript,
            'language': language_code,
        }
    except InvalidArgument:
        return {
            'success': False,
            'transcript': "Sorry, we had trouble converting that audio.",
            'language': 'en-us',
        }
    except PermissionDenied:
        return {
            'success': False,
            'transcript': "Sorry, there was a server permissions error.",
            'language': 'en-us',
        }
    except ResourceExhausted:
        return {
            'success': False,
            'transcript': "Sorry, we've exhausted our resources. Try again later.",
            'language': 'en-us',
        }
        