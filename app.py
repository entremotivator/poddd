import streamlit as st
from audiorecorder import audiorecorder

# Title of the application
st.title("Audio Recorder")

# Audio recording with prompts
audio = audiorecorder(start_prompt="Click to record", stop_prompt="Click to stop", show_visualizer=True)

# Check if an audio segment is returned
if len(audio) > 0:
    st.success("Recording successful!")

    # Play the recorded audio in the Streamlit frontend
    st.audio(audio.export().read(), format="audio/wav")

    # Save the recorded audio to a file
    audio.export("audio.wav", format="wav")

    # Display audio properties
    st.write(f"Frame rate: {audio.frame_rate} Hz")
    st.write(f"Frame width: {audio.frame_width} bytes")
    st.write(f"Duration: {audio.duration_seconds:.2f} seconds")
else:
    st.info("Click the button to start recording audio.")
