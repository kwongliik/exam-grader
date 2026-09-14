import os
import base64

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from google import genai
from dotenv import load_dotenv

from database import save_result, init_db

load_dotenv()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set. Add it to your .env file.")

client = genai.Client(api_key=GEMINI_API_KEY)

app = FastAPI(title="Exam Grader API")

# Allow the frontend to call this API. Tighten allow_origins once you deploy
# for real (replace "*" with your actual frontend URL).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class GradeResult(BaseModel):
    extracted_answer: str = Field(description="What the student wrote, transcribed as plain text.")
    score: float = Field(description="Marks awarded for this answer.")
    max_score: float = Field(description="Maximum marks possible for this question.")
    feedback: str = Field(description="Short, specific feedback explaining the score.")


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def health_check():
    return {"status": "ok"}


@app.post("/grade", response_model=GradeResult)
async def grade_answer(
    image: UploadFile = File(...),
    question_text: str = Form(...),
    marking_scheme: str = Form(...),
    max_score: float = Form(...),
    student_id: str = Form(...),
    question_id: str = Form(...),
):
    image_bytes = await image.read()
    mime_type = image.content_type or "image/jpeg"

    prompt = f"""You are grading a student's handwritten answer for a school exam.

Question:
{question_text}

Marking scheme (award marks strictly according to this):
{marking_scheme}

Maximum marks for this question: {max_score}

Read the handwriting in the image carefully. Transcribe what the student wrote,
then award marks according to the marking scheme. Do not give marks for work
that is missing, illegible, or incorrect. Explain the score briefly and
specifically, referring to what the student did or did not show."""

    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input=[
            {"type": "text", "text": prompt},
            {
                "type": "image",
                "data": base64.b64encode(image_bytes).decode("utf-8"),
                "mime_type": mime_type,
            },
        ],
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": GradeResult.model_json_schema(),
        },
    )

    try:
        result = GradeResult.model_validate_json(interaction.output_text)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Could not parse grading result: {e}")

    save_result(
        student_id=student_id,
        question_id=question_id,
        score=result.score,
        max_score=result.max_score,
        extracted_answer=result.extracted_answer,
        feedback=result.feedback,
    )

    return result
