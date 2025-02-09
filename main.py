from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "FastAPI is running on Render!"}


from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Endpoint
@app.get("/api/outline")
async def get_country_outline(country: str = Query(..., description="Country name to fetch data for")):
    try:
        # Construct Wikipedia URL
        wiki_url = f"https://en.wikipedia.org/wiki/{country.replace(' ', '_')}"
        
        # Fetch page content
        response = requests.get(wiki_url)
        if response.status_code != 200:
            return {"error": "Failed to fetch Wikipedia page"}
        
        # Parse HTML content
        soup = BeautifulSoup(response.text, "lxml")

        # Extract headings (H1 to H6)
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

        # Generate Markdown outline
        markdown_outline = "## Contents\n\n"
        for heading in headings:
            level = int(heading.name[1])  # Extract heading level (e.g., h2 -> 2)
            markdown_outline += f"{'#' * level} {heading.text.strip()}\n\n"

        return {"country": country, "outline": markdown_outline}
    
    except Exception as e:
        return {"error": str(e)}

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
