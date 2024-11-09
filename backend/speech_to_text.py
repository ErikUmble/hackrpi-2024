from google.cloud import speech

stt_client = speech.SpeechClient()

def speech_to_text(audio_bytes):

    config = speech.RecognitionConfig(
        language_code="en",
    )
    audio = speech.RecognitionAudio(
        content=audio_bytes,
    )

    response = stt_client.recognize(config=config, audio=audio)

    # Synchronous speech recognition request
    response = stt_client.recognize(config=config, audio=audio)

    return response.results