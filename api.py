# api.py
from fastapi import FastAPI, HTTPException
from utils import NewsProcessor
from pydantic import BaseModel
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()
processor = NewsProcessor()

class CompanyRequest(BaseModel):
    company_name: str

@app.post("/analyze_company")
async def analyze_company(request: CompanyRequest):
    logger.info(f"Received request for company: {request.company_name}")
    try:
        result = processor.process_company_news(request.company_name)
        summary_text = f"{request.company_name} के बारे में नवीनतम समाचार: "
        sentiments = result['comparative_analysis']['sentiment_distribution']
        summary_text += f"सकारात्मक: {sentiments['Positive']}, नकारात्मक: {sentiments['Negative']}, तटस्थ: {sentiments['Neutral']}"
        audio_file = processor.generate_tts(summary_text)
        result['audio_file'] = audio_file
        return result
    except Exception as e:
        logger.error(f"Error in analyze_company: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")