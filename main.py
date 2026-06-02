from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

from database import get_db
from models import SalesLead
from agent import agent_app  # The AI Brain we built!

app = FastAPI(title="AI Lead Routing Agent")

# Pydantic model for incoming API requests
class WebhookPayload(BaseModel):
    customer_id: str
    message: str


@app.post("/api/v1/webhook/message")
async def receive_message(
    payload: WebhookPayload,
    db: AsyncSession = Depends(get_db),
):
    """
    1) Receives the webhook message
    2) Runs it through the LangGraph AI agent
    3) If it's a sales lead, saves extracted fields to SQLite
    """
    try:
        initial_state = {
            "customer_id": payload.customer_id,
            "message": payload.message,
            "category": "",
            "company_name": "Unknown",
            "budget": "Unknown",
            "final_response": "",
        }

        print(f"\n--- Processing Webhook for {payload.customer_id} ---")
        final_state = agent_app.invoke(initial_state)

        if final_state.get("category") == "sales":
            new_lead = SalesLead(
                customer_id=final_state["customer_id"],
                company_name=final_state["company_name"],
                budget=final_state["budget"],
                original_message=final_state["message"],
            )
            db.add(new_lead)
            await db.commit()
            print(f"✅ Saved new Sales Lead to database: {final_state['company_name']}")

        return {
            "status": "success",
            "category": final_state.get("category"),
            "response": final_state.get("final_response"),
        }

    except Exception as e:
        print(f"Error processing webhook: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# --- DASHBOARD ROUTES ---

@app.get("/api/v1/leads")
async def get_all_leads(db: AsyncSession = Depends(get_db)):
    """Fetches all processed sales leads from the database, newest first."""
    result = await db.execute(select(SalesLead).order_by(SalesLead.created_at.desc()))
    leads = result.scalars().all()
    return leads


@app.get("/")
async def serve_dashboard():
    """Serves the frontend HTML dashboard."""
    return FileResponse("index.html")
