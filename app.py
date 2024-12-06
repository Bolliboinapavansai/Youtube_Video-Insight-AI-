import streamlit as st 
from dotenv import load_dotenv
load_dotenv()
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
genai.configure(api_key=os.getenv("GOOGLE_KEY"))

def get_prompt(video_title):
    return f"""
    You are tasked with providing an in-depth analysis of the video titled: '{video_title}'.
    Your goal is to generate a comprehensive summary that captures the main points, key arguments,
    and supporting details within a 750-word limit. Please thoroughly analyze the transcript text
    provided and offer a detailed summary, ensuring to cover all relevant aspects of the video:
    """
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("v=")[1]
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([item['text'] for item in transcript_data])
        return transcript
    except Exception as e:
        st.error(f"Error fetching transcript: {e}")
        return None
def generate_gemini_content(transcript_text, prompt):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt + transcript_text)
        return response.text
    except Exception as e:
        st.error(f"Error generating summary: {e}")
        return None
st.title("GEN-AI YouTube Video Summarizer")
youtube_link = st.text_input("Enter the YouTube Video URL:")

if youtube_link:
    video_id = youtube_link.split("v=")[1]
    st.image(f"https://img.youtube.com/vi/{video_id}/0.jpg", use_container_width =True)

if st.button("Get Detailed Notes"):
    transcript_text = extract_transcript_details(youtube_link)
    if transcript_text:
        st.info("Generating detailed notes. This might take a moment...")
        summary = generate_gemini_content(transcript_text, get_prompt("Video"))
        if summary:
            st.markdown("## Detailed Notes:")
            st.write(summary)