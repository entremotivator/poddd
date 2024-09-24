import streamlit as st
import numpy as np
from pydub import AudioSegment
from streamlit-audiorecorder import st_audiorec
import librosa
import librosa.display
import matplotlib.pyplot as plt
import noisereduce as nr
import soundfile as sf
import io
import os
import json

# Function to convert audio recording to AudioSegment
def audio_to_segment(audio_bytes):
    return AudioSegment.from_file(io.BytesIO(audio_bytes), format="wav")

# Function to trim audio
def trim_audio(audio, start, end):
    return audio[start*1000:end*1000]  # Time in milliseconds

# Function to apply EQ (simple example using low and high pass filters)
def apply_eq(audio, low_cut, high_cut):
    return audio.low_pass_filter(low_cut).high_pass_filter(high_cut)

# Function to add compression
def apply_compression(audio, threshold=-20.0, ratio=2.0):
    return audio.compress_dynamic_range(threshold=threshold, ratio=ratio)

# Function to apply reverb effect
def apply_reverb(audio, reverb_amount):
    return audio.fade_in(reverb_amount * 1000).fade_out(reverb_amount * 1000)

# Function to visualize audio as waveform
def display_waveform(audio_bytes):
    y, sr = librosa.load(io.BytesIO(audio_bytes), sr=None)
    st.write(f"Sample Rate: {sr}")
    st.write(f"Duration: {librosa.get_duration(y=y, sr=sr)} seconds")
    plt.figure(figsize=(10, 4))
    librosa.display.waveshow(y, sr=sr)
    st.pyplot()

# Function to apply noise reduction using noisereduce
def reduce_noise(audio_bytes, prop_decrease):
    y, sr = librosa.load(io.BytesIO(audio_bytes), sr=None)
    reduced_noise = nr.reduce_noise(y=y, sr=sr, prop_decrease=prop_decrease)
    output_buffer = io.BytesIO()
    sf.write(output_buffer, reduced_noise, sr, format='wav')
    return output_buffer.getvalue()

# Function to visualize audio as a spectrogram
def display_spectrogram(audio_bytes):
    y, sr = librosa.load(io.BytesIO(audio_bytes), sr=None)
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    plt.figure(figsize=(10, 6))
    librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    st.pyplot()

# Function to adjust pitch and speed using librosa
def change_pitch_speed(audio_bytes, pitch_factor, speed_factor):
    y, sr = librosa.load(io.BytesIO(audio_bytes), sr=None)
    y = librosa.effects.pitch_shift(y, sr, n_steps=pitch_factor)
    y = librosa.effects.time_stretch(y, speed_factor)
    output_buffer = io.BytesIO()
    sf.write(output_buffer, y, sr, format='wav')
    return output_buffer.getvalue()

# New Feature: Multi-track editing
def load_second_audio(uploaded_audio):
    return AudioSegment.from_file(io.BytesIO(uploaded_audio), format="wav")

# New Feature: Crossfade audio
def crossfade_audio(track1, track2, duration):
    return track1.append(track2, crossfade=duration * 1000)

# New Feature: Keyframe-based volume automation
def apply_keyframe_volume(audio, keyframes):
    for keyframe in keyframes:
        time, volume = keyframe
        start_ms = time * 1000
        audio = audio.fade(to_gain=volume, start=start_ms, duration=500)
    return audio

# New Feature: Save and Load Projects
def save_project(project_data, filename="project.json"):
    with open(filename, 'w') as f:
        json.dump(project_data, f)
    st.success("Project saved successfully!")

def load_project(filename="project.json"):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            project_data = json.load(f)
        return project_data
    else:
        st.error("No saved project found.")
        return None

# Streamlit app layout
st.title("Enhanced Podcast Editing and Sound Enhancements")

st.subheader("1. Record or Upload Your Audio")

# Audio recording or file upload
audio_bytes = st_audiorec()

uploaded_audio = st.file_uploader("Or Upload an Audio File", type=["wav", "mp3"])
if uploaded_audio:
    audio_bytes = uploaded_audio.read()

if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")
    
    # Load the recorded or uploaded audio as an AudioSegment
    audio = audio_to_segment(audio_bytes)
    
    # Waveform visualization
    st.subheader("Audio Waveform")
    display_waveform(audio_bytes)
    
    # Spectrogram visualization
    st.subheader("Audio Spectrogram")
    display_spectrogram(audio_bytes)
    
    # Trim Audio
    st.subheader("2. Trim Your Audio")
    start_time = st.slider("Start Time (seconds)", 0, int(len(audio) / 1000), 0)
    end_time = st.slider("End Time (seconds)", start_time, int(len(audio) / 1000), int(len(audio) / 1000))
    if st.button("Trim Audio"):
        trimmed_audio = trim_audio(audio, start_time, end_time)
        st.audio(trimmed_audio.export(format="wav"), format="audio/wav")
    
    # Equalization
    st.subheader("3. Apply Equalization (EQ)")
    low_cut = st.slider("Low Cut Frequency (Hz)", 20, 500, 100)
    high_cut = st.slider("High Cut Frequency (Hz)", 1000, 20000, 15000)
    if st.button("Apply EQ"):
        eq_audio = apply_eq(audio, low_cut, high_cut)
        st.audio(eq_audio.export(format="wav"), format="audio/wav")
    
    # Compression
    st.subheader("4. Apply Compression")
    threshold = st.slider("Threshold (dB)", -40.0, 0.0, -20.0)
    ratio = st.slider("Compression Ratio", 1.0, 10.0, 2.0)
    if st.button("Apply Compression"):
        compressed_audio = apply_compression(audio, threshold, ratio)
        st.audio(compressed_audio.export(format="wav"), format="audio/wav")
    
    # Reverb
    st.subheader("5. Apply Reverb")
    reverb_amount = st.slider("Reverb Amount (seconds)", 0.0, 5.0, 0.5)
    if st.button("Apply Reverb"):
        reverb_audio = apply_reverb(audio, reverb_amount)
        st.audio(reverb_audio.export(format="wav"), format="audio/wav")
    
    # Noise Reduction with adjustable parameter
    st.subheader("6. Apply Noise Reduction")
    prop_decrease = st.slider("Noise Reduction Amount", 0.0, 1.0, 0.5)
    if st.button("Reduce Noise"):
        noise_reduced_audio = reduce_noise(audio_bytes, prop_decrease)
        st.audio(noise_reduced_audio, format="audio/wav")
    
    # Pitch and Speed
    st.subheader("7. Adjust Pitch and Speed")
    pitch_factor = st.slider("Pitch Adjustment (in semitones)", -12, 12, 0)
    speed_factor = st.slider("Speed Adjustment (1.0 = normal speed)", 0.5, 2.0, 1.0)
    if st.button("Change Pitch and Speed"):
        pitch_speed_audio = change_pitch_speed(audio_bytes, pitch_factor, speed_factor)
        st.audio(pitch_speed_audio, format="audio/wav")
    
    # Multi-Track Editing
    st.subheader("8. Multi-Track Editing")
    uploaded_audio2 = st.file_uploader("Upload a Second Audio Track", type=["wav", "mp3"])
    if uploaded_audio2:
        second_audio = load_second_audio(uploaded_audio2.read())
        st.audio(second_audio.export(format="wav"), format="audio/wav")
        
        # Crossfade between two tracks
        crossfade_duration = st.slider("Crossfade Duration (seconds)", 1, 10, 5)
        if st.button("Apply Crossfade"):
            crossfaded_audio = crossfade_audio(audio, second_audio, crossfade_duration)
            st.audio(crossfaded_audio.export(format="wav"), format="audio/wav")
    
    # Keyframe-based volume control
    st.subheader("9. Volume Automation with Keyframes")
    keyframes = st.text_input("Enter keyframes (time, volume) separated by commas (e.g., 10,0.5, 20,-0.5)")
    if st.button("Apply Volume Automation"):
        keyframe_list = [tuple(map(float, k.split(','))) for k in keyframes.split()]
        automated_audio = apply_keyframe_volume(audio, keyframe_list)
        st.audio(automated_audio.export(format="wav"), format="audio/wav")
    
    # Save project
    st.subheader("10. Save and Load Projects")
    project_name = st.text_input("Enter project name:")
    if st.button("Save Project"):
        project_data = {
            "audio_bytes": audio_bytes.hex(),
            "start_time": start_time,
            "end_time": end_time,
            "low_cut": low_cut,
            "high_cut": high_cut,
            "threshold": threshold,
            "ratio": ratio,
            "reverb_amount": reverb_amount,
            "prop_decrease": prop_decrease,
            "pitch_factor": pitch_factor,
            "speed_factor": speed_factor,
        }
        save_project(project_data, filename=f"{project_name}.json")
    
    # Load project
    project_file = st.file_uploader("Load Project", type=["json"])
    if project_file:
        project_data = load_project(project_file.name)
        if project_data:
            st.write(f"Loaded project: {project_file.name}")
