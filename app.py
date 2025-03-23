# app.py
import streamlit as st
import requests
import os

st.title("News Sentiment Analyzer with Hindi TTS")
st.write("Enter a company name to analyze recent news coverage")

company_name = st.text_input("Company Name", "Tesla")
analyze_button = st.button("Analyze")

if analyze_button:
    with st.spinner("Analyzing news..."):
        api_url = "http://localhost:8000/analyze_company"
        try:
            response = requests.post(api_url, json={"company_name": company_name}, timeout=15)
            response.raise_for_status()
            result = response.json()
            
            st.subheader(f"Analysis for {company_name}")
            for i, article in enumerate(result['articles'], 1):
                st.write(f"**Article {i}: {article['title']}**")
                st.write(f"Summary: {article['summary']}")
                st.write(f"Sentiment: {article['sentiment']}")
                st.write(f"Topics: {', '.join(article['topics'])}")
                st.write("---")
            
            st.subheader("Comparative Analysis")
            sentiment_dist = result['comparative_analysis']['sentiment_distribution']
            st.write("Sentiment Distribution:")
            st.write(f"Positive: {sentiment_dist['Positive']}")
            st.write(f"Negative: {sentiment_dist['Negative']}")
            st.write(f"Neutral: {sentiment_dist['Neutral']}")
            st.write("Coverage Differences:")
            for diff in result['comparative_analysis']['coverage_difference']:
                st.write(f"- {diff}")
            st.write("Topic Overlap:")
            common = result['comparative_analysis']['topic_overlap']['common_topics']
            st.write(f"Common Topics: {', '.join(common) if common else 'None'}")
            for article, topics in result['comparative_analysis']['topic_overlap']['unique_topics'].items():
                st.write(f"{article}: {', '.join(topics) if topics else 'None'}")
            
            st.subheader("Hindi Audio Summary")
            audio_file_path = result.get('audio_file')
            if audio_file_path and os.path.exists(audio_file_path):
                with open(audio_file_path, 'rb') as audio_file:
                    st.audio(audio_file.read(), format='audio/mp3', start_time=0)
                os.remove(audio_file_path)
            else:
                st.warning("Audio file could not be generated")
        except requests.exceptions.RequestException as e:
            st.error(f"Error processing request: {str(e)}")