from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from llm import story_from_themes, continue_story, get_three_options
from text_analysis import lix_calculator
import database as db


# Create FastAPI instance
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",  # Vue dev server
        "http://192.168.0.195:8080",  # Network access
    ],
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "PUT",
        "DELETE",
        "OPTIONS",
    ],
    allow_headers=["Content-Type", "Authorization"],
    max_age=3600,
)


# Define input model
class InputData(BaseModel):
    text: str
    user_id: int
    story_id: int


# Define the endpoint
@app.post("/generate_new_story")
async def generate_new_story(data: InputData):
    """Generate a story from the provided text prompt."""
    prompt_response = await story_from_themes(data.text, data.user_id, data.story_id)
    return {"result": prompt_response[1]}


@app.post("/generate_three_options")
async def generate_three_options(data: InputData):
    """Generate three options for the story."""
    choice_list = await get_three_options(data.user_id, data.story_id)
    return {"result": choice_list}


@app.post("/chat")
async def post_chat(data: InputData):
    """Process chat input and return AI-generated response."""
    generated_text = await continue_story(data.text, data.user_id, data.story_id)
    return {"result": generated_text[1]}


@app.post("/analyze")
async def analyze_text(data: InputData):
    """Analyze text and return readability score."""
    readability_score = lix_calculator(data.text)
    return {"result": readability_score}


@app.get("/get_new_story_id/{user_id}")
async def get_new_story_id(user_id: int):
    """Get a new story ID for a specific user."""
    story_id = db.get_new_story_id(user_id)
    return {"story_id": story_id or 1}  # Return 1 if no previous stories exist
