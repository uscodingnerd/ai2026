from openai import OpenAI
from pathlib import Path

# Load API key
with open("../apikey.txt", "r") as file:
    api_key_str = file.read().strip()

client = OpenAI(api_key=api_key_str)

# Define the output path
speech_file_path = Path(__file__).parent / "speech.mp3"

# Create the speech and stream it to a file
with client.audio.speech.with_streaming_response.create(
    model="tts-1",          # or "tts-1-hd"
    voice="alloy",          # alloy, echo, fable, onyx, nova, shimmer
    input="The quick brown fox jumped over the lazy dog.",
    response_format="mp3",
) as response:
    response.stream_to_file(speech_file_path)
