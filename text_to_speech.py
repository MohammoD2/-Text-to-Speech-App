import os
import edge_tts

async def text_to_speech(text, output_folder="voices"):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Count the existing voice files to name the new one
    existing_files = [f for f in os.listdir(output_folder) if f.startswith("voice") and f.endswith(".mp3")]
    next_index = len(existing_files) + 1
    output_file = os.path.join(output_folder, f"voice{next_index}.mp3")

    # TTS configuration
    voice = "en-US-GuyNeural"
    tts = edge_tts.Communicate(text=text, voice=voice)

    print(f"Starting TTS for text: {text}")
    await tts.save(output_file)

    print(f"Audio saved as {output_file}")

if __name__ == "__main__":
    import asyncio

    # Example input text
    text = input("Enter the text to convert to speech: ")
    asyncio.run(text_to_speech(text))
