# -*- coding: utf-8 -*-
"""
Created on Fri May  3 00:40:01 2024

@author: Mariam
"""

from fastapi import FastAPI, HTTPException
from webscraper import WebScraper
from ai_assistant import Assistant

app = FastAPI()

@app.post("/process_document")
async def process_document(url: str):
    try:
        web_scraper = WebScraper(url)
        web_content = web_scraper.scrape_content()
        path = web_scraper.save_to_text_file(web_content)

        if path:
            ai_assistant = Assistant(path)
            result = ai_assistant.run_assistant()
            return {"result": result}
        else:
            raise HTTPException(status_code=400, detail="Failed to create PDF from the provided URL")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)