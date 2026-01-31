from openai import OpenAI

with open("../apikey.txt", "r") as file:
    api_key_str = file.read().strip()
client = OpenAI(
    api_key=api_key_str
)

# Open the audio file in binary read mode
with open("speech.mp3", "rb") as audio_file:
    # Call the Whisper translation endpoint
    transcript = client.audio.translations.create(
        model="whisper-1",
        file=audio_file
    )

# Print the translated output
print(transcript.text)
