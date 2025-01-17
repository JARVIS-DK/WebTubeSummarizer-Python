import streamlit as st  # type: ignore
from dotenv import load_dotenv  # type: ignore
import os
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai  # type: ignore
from youtube_transcript_api import YouTubeTranscriptApi  # type: ignore
from random import randint
import re
from requests import get
from requests.exceptions import RequestException


# Navigation Logic
def navigate_to(page):
    st.session_state["current_page"] = page


# Initialize session state for navigation
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "home"

# Load environment variables from .env file
load_dotenv()

# Configure Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Global Prompt for YouTube Summarizer
youtube_prompt = """You are a Youtube video summarizer. You will take the transcript text and summarize the entire video in points within 250 words. 
In the start, give the title of the video in capitalized bold format (center aligned) in text, followed by a summary and then important points. 
Make it appealing with emojis and suggest proper image sources from trusted websites."""


# Navigation Logic
def navigate_to(page):
    st.session_state["current_page"] = page


# Initialize session state for navigation
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "home"

# Home Page
if st.session_state["current_page"] == "home":
    st.title("WebTube Summarizer!")

    st.markdown("""
    This app has two features:
    1. **YouTube Video Summarizer** - Summarize YouTube videos using transcripts.
    2. **Website Summarizer** - Summarize content from any website.
    """)

    if st.button("Go to YouTube Summarizer"):
        navigate_to("youtube")

    if st.button("Go to Website Summarizer"):
        navigate_to("website")

# YouTube Summarizer Page
elif st.session_state["current_page"] == "youtube":
    prompt = """You are a Youtube video summarizer. You will be taking the transcript text and summarizing the entire video and providing the important summary in points within 250 words. In the start, give the title of the video in capitalized bold format (center aligned) in text and then followed by summary and then important points. You are primarily used for educational purposes, so give it in a student-understanding way. Also, feel free to use emojis to make it fun and appealing. Provide proper image sources from trusted websites so people can study with pictures for better understanding. Here is your transcript: """


    class Generation:
        def create(self, prompt):
            try:
                return get(
                    url=f"https://image.pollinations.ai/prompt/{prompt}{randint(1, 10000)}",
                    timeout=30,
                ).content
            except RequestException as exc:
                raise RequestException("Unable to fetch the response.") from exc


    def extract_transcript_details(youtube_video_url):
        """Extracts the transcript from the YouTube video."""
        try:
            video_id = youtube_video_url.split("=")[1]
            transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

            transcript = ""
            for i in transcript_text:
                transcript += " " + i["text"]
            return transcript, video_id
        except Exception as e:
            raise e


    def generate_gemini_content(transcript_text, prompt):
        """Generates content using the Gemini model."""
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt + transcript_text)
        return response.text


    def clean_title(title):
        """Cleans the title to use it for image generation."""
        return re.sub(r'[^a-zA-Z0-9 ]', '', title)


    def get_one_word_title(title):
        """Gets a one-word title from the video title."""
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(
            "generate a single line about what the below paragraph explains\n" + transcript_text)
        # print(response.text)
        return response.text

        # words = title.split()
        # for word in words:
        #     cleaned_word = clean_title(word)
        #     if cleaned_word:  # Ensure it's not an empty string
        #         return cleaned_word.lower()  # Convert to lowercase for consistency
        # return "default"  # Fallback if no valid word found


    # Your Streamlit App
    st.title("The YouTube NoteMaker with Image Generator")

    # Input for YouTube Link
    youtube_link = st.text_input("Enter YouTube video link:")
    if st.button("Back to Home"):
        navigate_to("home")

    if youtube_link:
        video_id = youtube_link.split("=")[1]
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)

        # Button to Get Notes
        if st.button("Generate Notes and Image"):
            # Get transcript
            transcript_text, video_id = extract_transcript_details(youtube_link)

            # Generate summary using the Gemini model
            summary = generate_gemini_content(transcript_text, prompt)
            st.markdown("### Summary and Important Points:")
            st.write(summary)

            # Clean title for image generation
            cleaned_title = clean_title(summary.split('\n')[0])  # Use the first line as the title
            try:
                one_word_title = get_one_word_title(cleaned_title)
            except:
                one_word_title = "Error"

            # Image generation using the cleaned title
            gen = Generation()

            for i in range(4):
                try:
                    image = gen.create(cleaned_title)
                    # Save and show the generated image with a one-word filename
                    image_filename = f"images/{one_word_title}{i}.jpg"

                    with open(image_filename, "wb") as f:
                        f.write(image)
                    st.image(image_filename)
                except:
                    continue
                    # st.image(image_filename, caption=f"Generated image for '{one_word_title}'", use_container_width=True)

            # image2 = gen.create(cleaned_title)
            # image3 = gen.create(cleaned_title)
            # image4 = gen.create(cleaned_title)

            # # Save and show the generated image with a one-word filename
            # image_filename1 = f"images/{one_word_title}1.jpg"
            # image_filename2 = f"images/{one_word_title}2.jpg"
            # image_filename3 = f"images/{one_word_title}3.jpg"
            # image_filename4 = f"images/{one_word_title}4.jpg"
            # with open(image_filename1, "wb") as f:
            #     f.write(image1)
            # with open(image_filename1, "wb") as f:
            #     f.write(image1)
            # with open(image_filename2, "wb") as f:
            #     f.write(image2)
            # with open(image_filename3, "wb") as f:
            #     f.write(image3)
            # with open(image_filename4, "wb") as f:
            #     f.write(image4)

            # st.image(image_filename1, caption=f"Generated image for '{one_word_title}'", use_container_width=True)
            # st.image(image_filename2, caption=f"Generated image for '{one_word_title}'", use_container_width=True)
            # st.image(image_filename3, caption=f"Generated image for '{one_word_title}'", use_container_width=True)
            # st.image(image_filename4, caption=f"Generated image for '{one_word_title}'", use_container_width=True)



# Website Summarizer Page
elif st.session_state["current_page"] == "website":
    def fetch_website_content(url):
        """Fetches and extracts the main text content from the website."""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract all text within <p> tags
            paragraphs = soup.find_all('p')
            text = ' '.join(p.get_text() for p in paragraphs if p.get_text())
            # print(text)
            return text
        except Exception as e:
            return f"Error fetching content: {e}"


    def summarize_text(text):
        """Summarizes the given text using Google Generative AI."""
        try:
            if len(text) > 10000:  # Limit text length for the summarizer
                text = text[:10000]
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(
                f"Summarize this text in an innovative way to understand it in detail:\n{text}"
            )
            return response.text if response else "No summary generated."
        except Exception as e:
            return f"Error in summarization: {e}"


    # Streamlit App
    st.title("Website Summarizer")
    url = st.text_input("Enter Website URL:")
    if st.button("Back to Home"):
        navigate_to("home")

    if url:
        with st.spinner("Fetching and summarizing content..."):
            content = fetch_website_content(url)
            if "Error" not in content:
                summary = summarize_text(content)
                st.subheader("Summary:")
                st.write(summary)
            else:
                st.error(content)

