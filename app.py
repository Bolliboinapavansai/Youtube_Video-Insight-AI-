import streamlit as st 
from dotenv import load_dotenv
load_dotenv()
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
genai.configure(api_key=os.getenv("GOOGLE_KEY"))

def get_prompt(video_title):
   return f"""
You are tasked with providing a detailed and insightful analysis of the video titled: '{video_title}'.
Your goal is to generate a comprehensive summary of the content, capturing the main points, key arguments,
important details, and any conclusions or recommendations made in the video. The summary should not exceed 750 words.

Please ensure that your analysis covers the following:

1. **Main Idea**: Provide a concise overview of the video’s core message or topic.
2. **Key Points**: Identify the most significant points and arguments presented.
3. **Supporting Details**: Highlight examples, statistics, or explanations that support the main points.
4. **Insights and Analysis**: Offer deeper insights into the video's content, discussing implications or connections to broader topics, if relevant.
5. **Conclusion/Recommendations**: Summarize any conclusions or actionable recommendations made in the video.

The summary should be structured, clear, and informative, offering a well-rounded perspective on the video’s content while remaining within the 750-word limit.
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