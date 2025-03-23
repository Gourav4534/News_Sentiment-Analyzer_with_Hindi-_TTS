# utils.py
import requests
from bs4 import BeautifulSoup
from transformers import pipeline
from gtts import gTTS
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag
import re
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

class NewsProcessor:
    def __init__(self):
        logger.info("Initializing NewsProcessor")
        self.sentiment_analyzer = pipeline("sentiment-analysis")
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        self.stop_words = set(stopwords.words('english'))
        self.common_publishers = {'google', 'reuters', 'times', 'india', 'hindustan', 'express', 'today', 'mint', 'rediffmail', 'finshots', 
                                 'moneycontrol', 'deccan', 'herald', 'ndtv', 'benzinga', 'forbes', 'economic'}
        logger.info("NewsProcessor initialized")

    def fetch_articles(self, company_name, num_articles=10):
        logger.info(f"Fetching articles for {company_name}")
        try:
            search_url = f"https://news.google.com/rss/search?q={company_name}"
            response = requests.get(search_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'lxml-xml')
            items = soup.find_all('item')[:num_articles]
            articles = [{'title': item.title.text, 'link': item.link.text, 'pub_date': item.pubDate.text} for item in items]
            logger.info(f"Found {len(articles)} articles")
            return articles
        except Exception as e:
            logger.error(f"Error fetching articles: {str(e)}")
            return []

    def extract_content(self, url, title_as_fallback=""):
        logger.info(f"Extracting content from {url}")
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            for elem in soup(["script", "style", "nav", "footer", "header", "aside", "form"]):
                elem.decompose()
            
            # Try multiple content selectors
            for selector in ['article', 'div[class*=article]', 'div[class*=content]', 'div[class*=post]', 'section', 'div[class*=story]']:
                article = soup.select_one(selector)
                if article:
                    paragraphs = article.find_all('p')
                    if paragraphs and len(paragraphs) > 1:
                        break
            else:
                paragraphs = soup.find_all('p')
            
            text = " ".join(p.get_text(strip=True) for p in paragraphs[:5]) if paragraphs else soup.get_text(strip=True)
            cleaned_text = re.sub(r'\s+', ' ', text).strip()
            if len(cleaned_text) > 100:
                logger.info(f"Extracted content length: {len(cleaned_text)}")
                return cleaned_text
            logger.warning(f"Insufficient content extracted, falling back to title: {title_as_fallback}")
            return title_as_fallback
        except Exception as e:
            logger.error(f"Error extracting content from {url}: {str(e)}")
            return title_as_fallback

    def summarize_text(self, text):
        logger.info("Summarizing text")
        try:
            sentences = sent_tokenize(text)
            if len(sentences) >= 2:
                return " ".join(sentences[:2])
            elif len(sentences) == 1:
                return sentences[0]
            return text[:200] if len(text) > 50 else "Content unavailable for summary"
        except Exception:
            logger.warning("Summarization failed")
            return text[:200] if len(text) > 50 else "Content unavailable for summary"

    def analyze_sentiment(self, text):
        logger.info("Analyzing sentiment")
        try:
            result = self.sentiment_analyzer(text[:512])[0]
            label = result['label'].lower()
            sentiment = 'Positive' if label == 'positive' else 'Negative' if label == 'negative' else 'Neutral'
            logger.info(f"Sentiment determined: {sentiment}")
            return sentiment
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {str(e)}")
            return 'Neutral'

    def extract_topics(self, text):
        logger.info("Extracting topics")
        try:
            words = word_tokenize(re.sub(r'[^a-zA-Z\s]', ' ', text.lower()))  # Clean text
            tagged = pos_tag(words)
            nouns = [word for word, pos in tagged if pos.startswith('NN') and len(word) > 4 and word not in self.stop_words]
            freq = nltk.FreqDist(nouns)
            topics = [word for word, _ in freq.most_common(5) if word not in self.common_publishers]
            return topics if topics else ['no specific topics']
        except Exception:
            logger.warning("Topic extraction failed")
            return ['no specific topics']

    def generate_tts(self, text, filename='output.mp3'):
        logger.info("Generating TTS")
        try:
            tts = gTTS(text=text, lang='hi', slow=False)
            tts.save(filename)
            logger.info(f"TTS saved to {filename}")
            return filename
        except Exception as e:
            logger.error(f"Error generating TTS: {str(e)}")
            return None

    def process_company_news(self, company_name):
        logger.info(f"Processing news for {company_name}")
        articles = self.fetch_articles(company_name)
        processed_articles = []

        for article in articles:
            content = self.extract_content(article['link'], article['title'])
            summary = self.summarize_text(content)
            sentiment = self.analyze_sentiment(content)
            topics = self.extract_topics(content)
            processed_articles.append({
                'title': article['title'],
                'summary': summary,
                'sentiment': sentiment,
                'topics': topics
            })

        sentiment_dist = {
            'Positive': sum(1 for a in processed_articles if a['sentiment'] == 'Positive'),
            'Negative': sum(1 for a in processed_articles if a['sentiment'] == 'Negative'),
            'Neutral': sum(1 for a in processed_articles if a['sentiment'] == 'Neutral')
        }

        return {
            'company': company_name,
            'articles': processed_articles,
            'comparative_analysis': {
                'sentiment_distribution': sentiment_dist,
                'coverage_difference': self._generate_coverage_diff(processed_articles),
                'topic_overlap': self._analyze_topic_overlap(processed_articles)
            }
        }

    def _generate_coverage_diff(self, articles):
        if len(articles) >= 2:
            return [
                f"Article 1 ({articles[0]['sentiment']}): {articles[0]['summary'][:50]}...",
                f"Article 2 ({articles[1]['sentiment']}): {articles[1]['summary'][:50]}...",
                f"Impact: {self._assess_impact(articles)}"
            ]
        return ["Insufficient articles for comparison"]

    def _assess_impact(self, articles):
        sentiments = [a['sentiment'] for a in articles[:2]]
        return f"Consistent {sentiments[0].lower()} coverage" if sentiments[0] == sentiments[1] else "Mixed coverage affecting perception"

    def _analyze_topic_overlap(self, articles):
        all_topics = [t for a in articles for t in a['topics'] if t != 'no specific topics']
        if not articles or not all_topics:
            return {'common_topics': [], 'unique_topics': {}}
        common = set.intersection(*[set(a['topics']) for a in articles if a['topics']])
        return {
            'common_topics': list(common),
            'unique_topics': {f"Article {i+1}": list(set(a['topics']) - common) 
                            for i, a in enumerate(articles) if a['topics']}
        }