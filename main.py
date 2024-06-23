import streamlit as st
# from audiorecorder import audiorecorder
from google.cloud import speech
from utils import prompt_template as pt
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part
import vertexai.preview.generative_models as generative_models
from utils import recognition
# List of audio files to select from
FILELIST=["sample_wavs/GAS0007.wav",
          "sample_wavs/RES0029.wav",
          "sample_wavs/RES0091.wav",
          "sample_wavs/RES0142.wav"
          ]

#List of AI Models to pick from
MODELLIST=["gemini-1.5-flash-001",
            "gemini-1.5-pro-001",
            "gemini-1.0-pro-002",
           "gemini-1.0-pro-001"
]


st.title("AI Scribe with Google Medical ASR and Gemini")
st.header("Summary")
st.write("In this demo, we take recorded patient consults from [a public research dataset](https://www.nature.com/articles/s41597-022-01423-1#Sec3)"
        " and use the Gemini API to generate a summarized clinical note in the SOAP format. "
        "We make use of few-shot prompting with both a negative and positive example of "
        "the items to be summarized in the sections of the note,"
         " as well as role prompting in the context. ")
st.image('assets/architecture.png')

# pin the prompt template to the sidebar
with st.sidebar:
    st.header("Prompt Template:")
    system_prompt = st.expander("System Prompt")
    #system_prompt.write(pt.system_prompt)
    ptemplate=system_prompt.text_area("Enter Prompt",'''You are a doctor. Your job is to summarize doctor/patient conversations using the SOAP format (Subjective Objective Assessment Plan) in the following sections",
"1. Subjective – The history section Include symptom dimensions, chronological narrative of patient’s complains, and information obtained from other sources (always identify source if not the patient.Pertinent past medical history,Pertinent review of body parts, for example, “Patient has not had any stiffness or loss of motion of other joints.”
Current medications (list with daily dosages).
2. Objective - any empirical or quantitative measurements observed during the visit. If none were observed, write "N/A"
difficulty speaking
vital signs/observations at clinic
3. Assessment/Problem List – Your assessment of the patient’s problems
Assessment: A one sentence description of the patient's chief complaint and any potential diagnoses found in the text. If there was no diagnosis, write "N/A"
Problem list: A numerical list of problems identified. All listed problems need to be supported by findings in subjective and objective areas above.
4. Plan - the care plan and next steps for the patient. If there are no next steps identified in the text, write "N/A"
Any tests ordered
Any recommendations for the patient to try next.
Output all text in Markdown format.''',height=500)
    few_shot_1 = st.expander("Few shot Example #1")
    few_shot_1.write(pt.few_shot_1)
    few_shot_2 = st.expander("Few Shot Example #2")
    few_shot_2.write(pt.few_shot_2)
    project_id = st.text_input("Google Cloud ProjectId") #Input Text for ProjectID
# audio = audiorecorder("Click to record", "Click to stop recording")

# if len(audio) > 0:
#     # To play audio in frontend:
#     st.audio(audio.export().read())  

#     # To save audio to a file, use pydub export method:
#     audio.export("audio.wav", format="wav")

#     # To get audio properties, use pydub AudioSegment properties:
#     st.write(f"Frame rate: {audio.frame_rate}, Frame width: {audio.frame_width}, Duration: {audio.duration_seconds} seconds")


def transcribe(audiofile):
    # Instantiates a client
    client = speech.SpeechClient()

    # The name of the audio file to transcribe
    gcs_uri = audiofile

    audio = speech.RecognitionAudio(uri=gcs_uri)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=16000,
        language_code="en-US",
        model="medical_conversation"
    )

    # Detects speech in the audio file
    response = client.recognize(config=config, audio=audio)
    return response
    # for result in response.results:
    #     print(f"Transcript: {result.alternatives[0].transcript}")

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

audiofile = st.selectbox(
    label='Select an audio file for transcription:',
    options=(FILELIST),
    format_func=lambda x: x.split('/')[-1] # display only the filename
)

#Gemini Model Selector
modelselection=st.selectbox(
    label="Select the Gemini Model you would like to use:",
    options=(MODELLIST)
)

#Audio Player
if st.button('Play Audio'):
    st.audio(audiofile,format="audio/wav")




if st.button('Transcribe'):
    st.session_state['audiofile'] = audiofile
    st.session_state['transcript'] = ""

    with st.status("Generating transcript...", expanded=True) as status:
        st.session_state['transcript'] = st.write_stream(recognition.transcribe_streaming(audiofile))
        status.update(label="Completed transcription", state="complete")


    
# [START speech_transcribe_sync]


def SOAPify(transcript):
    full_text = ptemplate + pt.few_shot_1 + pt.few_shot_2 + pt.end.format(input_text=transcript) #Add modified prompt
    generation_config = {
    "max_output_tokens": 8192,
    "temperature": 0,
    "top_p": 0.95,
}
    vertexai.init(project=project_id, location="us-central1")
    model = GenerativeModel(modelselection)
    response = model.generate_content(full_text,
                                      generation_config=generation_config)
    st.markdown(response.text) 

# if 'audiofile' in st.session_state: 
#     st.session_state['transcript'] = transcribe_gcs(audiofile)

    
        

if st.button('Generate Note'):
    if 'transcript' in st.session_state:
        with st.status("Completed transcription", expanded=False, state="complete") as transcribe_status:
            st.write(st.session_state['transcript'])
        with st.status("Generating SOAP note..", expanded=True) as soap_status: 
            st.write(SOAPify(st.session_state['transcript']))
            soap_status.update(label="Note complete.")
    else: 
        st.error("No transcript available")


