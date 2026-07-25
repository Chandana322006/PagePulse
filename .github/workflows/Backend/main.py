from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup
import time


app = FastAPI(
    title="PagePulse API",
    description="Website analysis tool",
    version="1.0"
)


# Allow Netlify frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://pagepulse-frontend-6gp3.onrender.com"],   # change to Netlify URL later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def home():
    return {
        "message": "PagePulse Backend is running 🚀"
    }



@app.get("/analyze")
def analyze(url: str = Query(..., description="Website URL to analyze")):

    try:

        # Start timer
        start_time = time.time()


        # Send request to website
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )


        # Response time
        end_time = time.time()

        response_time_ms = round(
            (end_time - start_time) * 1000,
            2
        )


        # Parse HTML
        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )


        # Title
        title = (
            soup.title.text.strip()
            if soup.title
            else "No title found"
        )


        # Meta description
        meta = soup.find(
            "meta",
            attrs={"name": "description"}
        )

        meta_description = (
            meta["content"]
            if meta and meta.get("content")
            else "No description found"
        )


        # Count H1 tags
        h1_count = len(
            soup.find_all("h1")
        )


        # Images without alt attribute
        images = soup.find_all("img")

        missing_alt = 0

        for img in images:
            if not img.get("alt"):
                missing_alt += 1



        # Word count
        text = soup.get_text(
            separator=" "
        )

        words = text.split()

        word_count = len(words)



        return {

            "status_code": response.status_code,

            "response_time_ms": response_time_ms,

            "title": title,

            "meta_description": meta_description,

            "h1_count": h1_count,

            "missing_alt": missing_alt,

            "word_count": word_count

        }


    except requests.exceptions.Timeout:

        return {
            "error": "Website took too long to respond"
        }


    except requests.exceptions.RequestException:

        return {
            "error": "Could not fetch website"
        }


    except Exception as e:

        return {
            "error": str(e)
        }