from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
import os

app = FastAPI(title="Earn Money App AI Backend")

ከ Frontend ጋር መገናኘት እንዲችል CORS መፍቀድ
app.add_middleware(
CORSMiddleware,
allow_origins=["*"],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)

የ Google GenAI ክላይንት ማዋቀር (ከ Google AI Studio ሰነድ የተወሰደ)
ኑት: GEMINI_API_KEY በኮምፒውተርዎ ወይም በሰርቨርዎ Environment Variable ውስጥ መኖር አለበት
client = genai.Client(http_options={"api_version": "v1beta"})

class QuizRequest(BaseModel):
topic: str = "General knowledge and technology"

class ProofVerificationRequest(BaseModel):
taskDescription: str
userProof: str

1. አውቶማቲክ የዕለታዊ ጥያቄ ማመንጨት (Dynamic Quiz Generation)
@app.post("/api/ai/generate-quiz")
def generate_quiz(req: QuizRequest):
try:
interaction = client.interactions.create(
agent="antigravity-preview-09-2026",
input=f"Create a short quiz question about {req.topic} with 4 options and state the correct answer clearly.",
environment="remote"
)
return {
"success": True,
"quiz": interaction.output_text,
"interaction_id": interaction.id
}
except Exception as e:
raise HTTPException(status_code=500, detail=str(e))

2. የታስክ ማረጋገጫ በ AI ማስተካከል (AI Task Proof Verification)
@app.post("/api/ai/verify-proof")
def verify_proof(req: ProofVerificationRequest):
try:
prompt = (
f"Review this user task proof for an earn-money app.\n"
f"Task Description: {req.taskDescription}\n"
f"User Proof: {req.userProof}\n"
f"Analyze if this proof is valid. Reply with 'STATUS: APPROVED' or 'STATUS: REJECTED' and a brief note."
)

interaction = client.interactions.create(
agent="antigravity-preview-09-2026",
input=prompt,
environment="remote"
)

return {
"success": True,
"verificationResult": interaction.output_text
}
except Exception as e:
raise HTTPException(status_code=500, detail=str(e))

// ከ AI ሰርቨር ጋር የሚገናኝ አዲስ የ JavaScript ተግባር (Function)
async function fetchAIGeneratedQuiz() {
try {
const response = await fetch('http://localhost:8000/api/ai/generate-quiz', {
method: 'POST',
headers: { 'Content-Type': 'application/json' },
body: JSON.stringify({ topic: "Cryptocurrency and Online Income" })
});
const data = await response.json();
if (data.success) {
console.log("AI Generated Quiz:", data.quiz);
// ይህንን ጥያቄ በዌብ ገጹ ላይ ማሳየት ይቻላል
}
} catch (err) {
console.error("Failed to fetch AI quiz:", err);
}
}
