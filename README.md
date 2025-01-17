# WebTube Summarizer

## Overview

WebTube Summarizer is a Python-based web application built with Streamlit to simplify the process of summarizing YouTube videos and website content. The app leverages Google Generative AI and other APIs to provide concise, easy-to-understand summaries. Additionally, it includes an image generation feature to enhance the understanding of content visually.

---

## Features

### 1. YouTube Video Summarizer

- Summarizes YouTube video transcripts into a brief, student-friendly format.
- Includes video title, key points, and emoji-enhanced summaries.
- Provides trusted image source suggestions to complement the summary.

### 2. Website Summarizer

- Extracts and summarizes content from any given website.
- Uses AI-powered summarization to deliver concise and detailed insights.

### 3. Image Generator

- Generates images based on video titles or extracted content using the Pollinations API.

---

## Technologies Used

- **Streamlit**: For building the web interface.
- **YouTube Transcript API**: For fetching YouTube video transcripts.
- **Google Generative AI**: For AI-powered text summarization.
- **Pollinations API**: For image generation.
- **BeautifulSoup**: For web scraping.
- **dotenv**: For managing environment variables.

---

## Installation

### Prerequisites

- Python 3.8 or above
- Conda environment setup

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/JARVIS-DK/WebTubeSummarizer-Python.git
   cd WebTubeSummarizer-Python
   ```

2. Create and activate a Conda environment:

   ```bash
   conda create -n myenv
   conda activate myenv
   ```

3. Install dependencies:

   ```bash
   conda install -n myenv streamlit youtube_transcript_api google-generativeai python-dotenv pathlib bs4
   ```

4. Add your Google API Key in a `.env` file:

   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

---

## Usage

1. Run the application:

   ```bash
   streamlit run app.py
   ```

2. Access the application in your browser at `http://localhost:8501`.

3. Navigate between the following pages:

   - **Home**: Overview of the app features.
   - **YouTube Summarizer**: Enter a YouTube link to get a summary and generated images.
   - **Website Summarizer**: Enter a website URL to summarize its content.

---

## Project Structure

```
WebTubeSummarizer-Python/
|-- app.py                 # Main Streamlit app script
|-- .env                   # Environment variables
|-- requirements.txt       # List of Python dependencies
|-- images/                # Directory to store generated images
|-- README.md              # Project documentation

```

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Contact

For any inquiries or issues, please contact [JARVIS-DK](https://github.com/JARVIS-DK).

