FROM python:3.9-slim
WORKDIR /ai-scribe
COPY . ./
RUN pip install -r requirements.txt
EXPOSE 8080
ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8080", "--server.address=0.0.0.0"]