<img src="ai_scribe.webp" width="200">
# AI Scribe demo with Google Medical Speech Recognition and Gemini
### @coreymaher
In this demo, we take recorded patient consults from [a public research dataset](https://www.nature.com/articles/s41597-022-01423-1#Sec3) and use the Gemini API to generate a summarized clinical note in the SOAP format. 
We make use of few-shot prompting with both a negative and positive example of the items to be summarized in the sections of the note, as well as role prompting in the context. 

## Architecture
(architecture.png)
Single page web application using the [Streamlit](https://streamlit.io/) Python library, with [Google's Medical ASR model](https://cloud.google.com/speech-to-text/docs/medical-models) performing the transcription of recorded calls. The transcription is then passed to [Vertex Gemini Pro 1.5 Flash](https://console.cloud.google.com/vertex-ai) for constructing a SOAP note. 

## Deployment 
### Local: 
1. Clone the repo, setup and switch to a new python virtual environment
2. pip install -r requirements.txt
3. The Vertex python clients depend on the gcloud SDK for authentication, so follow the steps to download the gcloud CLI and authorize your development environment here: [https://cloud.google.com/docs/authentication/provide-credentials-adc#google-idp](https://cloud.google.com/docs/authentication/provide-credentials-adc#google-idp). This will prompt you for a Google Cloud project ID and region, which the client libraries will use when making requests to the GCP APIs. 
4. Run `streamlit run main.py` in the root directory of this repository to launch the web server and open a browser window for the application