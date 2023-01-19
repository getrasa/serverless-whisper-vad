import torch
import whisper
import os
import base64
from io import BytesIO
import whisper_vad.app as app

# Init is ran on server startup
# Load your model to GPU as a global variable here using the variable name "model"


class AudioFile:
    def __init__(self, name) -> None:
        self.name = name


def init():
    # global model
    global transcriber

    # model = whisper.load_model("medium")
    transcriber = app.WhisperTranscriber("medium")

# Inference is ran for every server call
# Reference your preloaded global model variable here.


def inference(model_inputs: dict) -> dict:
    # global model

    # Parse out your arguments
    mp3BytesString = model_inputs.get('mp3BytesString', None)
    if mp3BytesString == None:
        return {'message': "No input provided"}

    mp3Bytes = BytesIO(base64.b64decode(mp3BytesString.encode("ISO-8859-1")))
    with open('input.mp3', 'wb') as file:
        file.write(mp3Bytes.getbuffer())

    # Run the model
    audio = AudioFile("input.mp3")
    result = transcriber.transcribe_webui_simple(
        "Japanese", None, [audio], None, "transcribe", "silero-vad", 5, 30, 1, 3)
    download, text, vtt = result
    output = {"text": vtt}
    # result = model.transcribe("input.mp3")
    # output = {"text": result["segments"]}
    os.remove("input.mp3")
    # Return the results as a dictionary
    return output


def main():
    print("Started")
    transcriber = app.WhisperTranscriber("medium")
    audio = AudioFile("./input.opus")
    result = transcriber.transcribe_webui_simple(
        "Japanese", None, [audio], None, "transcribe", "silero-vad", 5, 30, 1, 3)

    download, text, vtt = result
    print(text)


main()
