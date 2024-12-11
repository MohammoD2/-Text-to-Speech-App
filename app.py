import os
import asyncio
import streamlit as st
import edge_tts

# Custom mapping for voices with friendly labels
VOICE_OPTIONS = {
    "Deep Male Voice": "en-US-GuyNeural",
    "Calm Female Voice": "en-US-JennyNeural",
    "Energetic Female Voice": "en-US-AriaNeural",
    "Friendly Male Voice": "en-US-EricNeural",
}

# Async function for TTS
async def text_to_speech(text, voice):
    output_file = "voice_output.mp3"
    print(f"Using voice: {voice}, text: {text}")  # Debugging log
    tts = edge_tts.Communicate(text=text, voice=voice)

    try:
        await tts.save(output_file)
        return output_file
    except Exception as e:
        raise RuntimeError(f"TTS generation failed: {e}")

# Run async task
def run_async_task(coro):
    return asyncio.run(coro)

# Main app
def main():
    st.set_page_config(page_title="Text-to-Speech App", page_icon="🎤", layout="wide")

    # Custom HTML & CSS for UI
    html_content = """
    <style>
        body {
            font-family: 'Poppins', sans-serif;
            background-color: #f0f4f8;
        }
        .app-title {
            color: #333;
            text-align: center;
        }
        .stTextInput, .stSelectbox, .stButton {
            width: 100%;
            margin-bottom: 20px;
        }
        .stButton button {
            background-color: #007bff;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            border: none;
            cursor: pointer;
        }
        .stButton button:hover {
            background-color: #0056b3;
        }
        .stAudio {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 20px;
        }
    </style>
    """
    st.components.v1.html(html_content, height=0)

    st.title("🎤 Text-to-Speech App")
    st.write("Convert your text into speech with customizable voices!")

    text_input = st.text_area("Enter the text you want to convert to speech:")
    voice_label = st.selectbox("Choose a voice:", list(VOICE_OPTIONS.keys()))
    selected_voice = VOICE_OPTIONS[voice_label]

    if st.button("Convert to Speech"):
        if text_input.strip():
            if len(text_input.strip()) < 5:
                st.error("Text is too short. Please enter at least 5 characters.")
                return

            st.write("Processing... Please wait.")

            try:
                output_file = run_async_task(text_to_speech(text_input, selected_voice))
                st.success("Audio generated successfully!")
                st.audio(output_file, format="audio/mp3")
            except RuntimeError as e:
                st.error(f"An error occurred: {e}")
            except Exception as e:
                st.error(f"Unexpected error: {e}")
        else:
            st.error("Please enter some text before converting.")

if __name__ == "__main__":
    main()
