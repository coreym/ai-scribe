from google.cloud import speech
from google.cloud import storage

def audio_stream_generator(uri, chunk_size=8000):
    """
    Generates chunks of audio data from a file or GCS URI.
    Args:
        uri: The path to the audio file or the GCS URI.
        chunk_size: The size of each chunk in bytes.
    Yields:
        Chunks of audio data.
    """

    if uri[0:4] == "gs://" :
        storage_client = storage.Client()
        blob = storage.Blob.from_string(uri, storage_client)
        with blob.open("rb") as audio_file:
            data = audio_file.read(chunk_size)  # Read the first chunk
            while len(data) > 0:                       # Check if all data was read
                yield data                    # Yield the chunk
                data = audio_file.read(chunk_size) # Read the next chunk
    else: 
        with open(uri, "rb") as audio_file:
            data = audio_file.read(chunk_size)  # Read the first chunk
            while len(data) > 0:                       # Check if all data was read
                yield data                    # Yield the chunk
                data = audio_file.read(chunk_size) # Read the next chunk

def transcribe_streaming(audio_file):
    """
    Performs streaming transcription on an audio file.
    Args:
        audio_file: Path to the audio file.
    Returns:
        A generator that yields intermediate transcription results.
    """
    # TODO: parse the filename for encoding and inspect for sample rate
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=48000,
            language_code="en-US",
            model="medical_conversation",
        )

    streaming_config = speech.StreamingRecognitionConfig(config=config)

    requests = (
        speech.StreamingRecognizeRequest(audio_content=content) for content in audio_stream_generator(
            audio_file, 24000)
            )
    responses = client.streaming_recognize(streaming_config, requests)
    for response in responses:
        # Once the transcription has settled, the first result will contain the
        # is_final result. The other results will be for subsequent portions of
        # the audio.
        for result in response.results:
            alternatives = result.alternatives
            # The alternatives are ordered from most likely to least.
            for alternative in alternatives:
                # print(f"Confidence: {alternative.confidence}")
                yield(f"{alternative.transcript}")
        

def transcribe_gcs(gcs_uri: str) -> str:
    """Asynchronously transcribes the audio file specified by the gcs_uri.
    Args:
        gcs_uri: The Google Cloud Storage path to an audio file.
    Returns:
        The generated transcript from the audio file provided.
    """
    from google.cloud import speech

    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=16000,
        language_code="en-US",
        model="medical_conversation"
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=300)

    transcript_builder = []
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        st.write(result.alternatives[0].transcript)
        transcript_builder.append(result.alternatives[0].transcript)
        # transcript_builder.append(f"\nConfidence: {result.alternatives[0].confidence}")

    transcript = "".join(transcript_builder)
    # print(transcript)

    return transcript