import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
from pydub import AudioSegment
from scipy.io.wavfile import write
import noisereduce as nr
from audiorecorder import audiorecorder
import json
import io

# Function to save project
def save_project(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f)

# Function to load project
def load_project(filename):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("Project file not found")
        return None

# Audio Recording Integration
st.title("Audio Recorder and Editor")

# Audio recording with prompts
audio = audiorecorder(start_prompt="Click to record", stop_prompt="Click to stop", show_visualizer=True)

# Check if an audio segment is returned
if len(audio) > 0:
    st.success("Recording successful!")
    
    # Convert to AudioSegment for further processing
    audio_wav = audio.export(format="wav")
    audio_segment = AudioSegment.from_file(io.BytesIO(audio_wav.read()), format="wav")

    # Play the recorded audio in the Streamlit frontend
    st.audio(audio.export().read(), format="audio/wav")

    # Save the recorded audio to a file
    audio.export("audio.wav", format="wav")

    # Display audio properties
    st.write(f"Frame rate: {audio.frame_rate} Hz")
    st.write(f"Frame width: {audio.frame_width} bytes")
    st.write(f"Duration: {audio.duration_seconds:.2f} seconds")

    # Load the audio into Librosa for waveform and spectrogram
    y, sr = librosa.load("audio.wav")
    
    # Waveform visualization
    st.write("### Waveform:")
    fig, ax = plt.subplots()
    librosa.display.waveshow(y, sr=sr, ax=ax)
    st.pyplot(fig)
    
    # Spectrogram visualization
    st.write("### Spectrogram:")
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    fig, ax = plt.subplots()
    img = librosa.display.specshow(D, sr=sr, x_axis="time", y_axis="log", ax=ax)
    fig.colorbar(img, ax=ax, format="%+2.0f dB")
    st.pyplot(fig)
    
    # Audio trimming feature
    st.write("### Trim the Audio:")
    start_trim = st.slider("Start Trim (seconds):", 0.0, audio_segment.duration_seconds, 0.0)
    end_trim = st.slider("End Trim (seconds):", 0.0, audio_segment.duration_seconds, audio_segment.duration_seconds)
    trimmed_audio = audio_segment[start_trim * 1000:end_trim * 1000]  # Convert to milliseconds

    # Play trimmed audio
    st.audio(trimmed_audio.export(format="wav").read(), format="audio/wav")
    
    # Audio effects
    st.write("### Apply Effects:")
    eq_gain = st.slider("Equalization Gain (dB):", -20.0, 20.0, 0.0)
    compression_ratio = st.slider("Compression Ratio:", 1.0, 10.0, 1.0)
    reverb_amount = st.slider("Reverb Amount:", 0.0, 100.0, 0.0)

    # Noise reduction
    st.write("### Noise Reduction:")
    prop_decrease = st.slider("Noise Reduction Strength:", 0.0, 1.0, 0.5)
    reduced_noise = nr.reduce_noise(y=y, sr=sr, prop_decrease=prop_decrease)

    # Apply pitch and speed adjustment
    st.write("### Adjust Pitch and Speed:")
    pitch_factor = st.slider("Pitch Factor:", -12, 12, 0)
    speed_factor = st.slider("Speed Factor:", 0.5, 2.0, 1.0)
    y_pitch = librosa.effects.pitch_shift(y, sr, n_steps=pitch_factor)
    y_speed = librosa.effects.time_stretch(y_pitch, speed_factor)
    
    # Play the final processed audio
    final_audio = io.BytesIO()
    write(final_audio, sr, (y_speed * 32767).astype(np.int16))
    st.audio(final_audio.getvalue(), format="audio/wav")

    # Save and load projects
    project_name = st.text_input("Enter project name to save:")
    if st.button("Save Project"):
        project_data = {
            "audio": y_speed.tolist(),
            "sr": sr,
            "eq_gain": eq_gain,
            "compression_ratio": compression_ratio,
            "reverb": reverb_amount,
            "noise_reduction": prop_decrease,
            "pitch_speed": (pitch_factor, speed_factor),
        }
        save_project(project_data, f"{project_name}.json")
    
    # Load project
    project_to_load = st.text_input("Enter project name to load:")
    if st.button("Load Project"):
        project = load_project(f"{project_to_load}.json")
        if project:
            st.write(project)

else:
    st.info("Click the button to start recording audio.")
