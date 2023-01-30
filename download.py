# In this file, we define download_model
# It runs during container build time to get model weights built into the container

# In this example: A Huggingface BERT model

import whisper
import torch
import whisper_vad.app as app


def download_model():
    model = app.WhisperTranscriber("medium")
    # model = whisper.load_model("medium")


if __name__ == "__main__":
    download_model()
