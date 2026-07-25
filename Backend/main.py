from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import time
from bs4 import BeautifulSoup
app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def home():
    return{"message":"WELCOME TO PAGE PULSE"}
@app.get("/analyze")
def analyze(url: str):
    try:
        start_time = time.time()
        response = requests.get(url, timeout=10)
        status_code = response.status_code
        response_time = round((time.time() - start_time) * 1000, 2)
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string.strip() if soup.title else "No title found"
        meta = soup.find("meta", attrs={"name": "description"})
        meta_description = meta["content"] if meta and meta.get("content") else "No meta description"
        h1_count = len(soup.find_all("h1"))
        images = soup.find_all("img")
        missing_alt = sum(1 for img in images if not img.get("alt"))
        text = soup.get_text(separator=" ", strip=True)
        word_count = len(text.split())
        content_type = response.headers.get("Content-Type", "")

        if "text/html" not in content_type:
            return {
                "error": "The provided URL is not an HTML webpage."
  }
        
        return {
            "status_code": status_code,
            "response_time_ms": response_time,
            "title": title,
            "meta_description": meta_description,
            "h1_count": h1_count,
            "missing_alt": missing_alt,
            "word_count": word_count

}
    except requests.exceptions.MissingSchema:
        return {
            "error": "Invalid URL. Please include http:// or https://"
    }

    except requests.exceptions.Timeout:
        return {
            "error": "The request timed out."
    }

    except requests.exceptions.RequestException as e:
        return {
            "error": str(e)
    }