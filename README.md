# News Sentiment Analyzer with Hindi TTS

## Project Overview
This project is a **News Sentiment Analyzer with Hindi Text-to-Speech (TTS)** developed as an assignment submission. It fetches recent news articles about a specified company from Google News RSS, processes them to extract summaries, analyzes their sentiment (Positive, Negative, Neutral), identifies key topics, performs a comparative analysis, and generates a Hindi audio summary. Built using **Streamlit** for the frontend and **FastAPI** for the backend, this tool demonstrates web scraping, natural language processing (NLP), and text-to-speech capabilities.


## Features
- **News Fetching**: Retrieves up to 10 recent articles from Google News RSS based on a company name.
- **Summarization**: Generates concise 1-2 sentence summaries from article content.
- **Sentiment Analysis**: Classifies article sentiment using a pre-trained NLP model (Positive, Negative, Neutral).
- **Topic Extraction**: Identifies key topics from articles using noun-based keyword extraction.
- **Comparative Analysis**: Compares sentiment distribution, coverage differences, and topic overlap across articles.
- **Hindi TTS**: Produces an audio summary in Hindi using Google Text-to-Speech (gTTS).
- **User Interface**: Interactive Streamlit frontend for easy input and result visualization.

## Tech Stack
- **Frontend**: Streamlit
- **Backend**: FastAPI
- **Web Scraping**: BeautifulSoup, Requests
- **NLP**: NLTK, Transformers (Hugging Face)
- **TTS**: gTTS
- **Dependencies**: Managed via `requirements.txt`

## Setup Instructions
Follow these steps to run the project locally:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Gourav4534/News_Sentiment-Analyzer_with_Hindi-_TTS.git
   cd News_Sentiment-Analyzer_with_Hindi-_TTS

2. **Create and Activate Virtual Environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  

4. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt

5. **Run the Application:**  
**Open two terminals in the project directory.** 

    ```bash
    # Terminal 1 (API): 
    uvicorn api:app --reload
    
    # Terminal 2 (Frontend):
    streamlit run app.py

## Usage
- Open your browser and navigate to http://localhost:8501.
- Enter a company name (e.g., "Tesla") in the input field.
- Click Analyze to view:
- Article summaries, sentiments, and topics.
- Sentiment distribution and comparative analysis.
- A playable Hindi audio summary.
- Results are generated dynamically based on real-time news data.

# Author 
Gourav Yadav ([GitHub](https://github.com/Gourav4534))

