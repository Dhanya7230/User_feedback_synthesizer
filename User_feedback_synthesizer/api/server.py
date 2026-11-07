"""
FastAPI Backend Server for User Feedback Synthesizer.
Provides REST and Webhook endpoints for production integrations:
- Zendesk / Discord / Slack webhooks
- Product Manager query endpoint
- Timeline and sentiment analytics
- Executive briefing generator
"""

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import uvicorn

from agent.feedback_synthesizer import UserFeedbackSynthesizerAgent
from agent.report_generator import ExecutiveReportGenerator
from config import config

app = FastAPI(
    title="User Feedback Synthesizer API",
    version=config.version,
    description="Autonomous product intelligence agent powered by Hindsight Agent Memory Layer. HackwithHyderabad 3.0."
)

# Initialize agent singleton
agent = UserFeedbackSynthesizerAgent()
report_generator = ExecutiveReportGenerator(agent)

class IngestFeedbackRequest(BaseModel):
    channel: str = Field(..., description="Channel: zendesk, discord, reddit, gong, in_app_survey")
    author: str = Field(..., description="Author username or email")
    text: str = Field(..., description="Raw text content of the feedback")
    sentiment_score: Optional[float] = Field(0.0, ge=-1.0, le=1.0, description="Sentiment score from -1.0 to +1.0")
    account_id: Optional[str] = Field(None, description="Customer account ID (e.g. acc_acme_corp)")
    tags: Optional[List[str]] = Field(default_factory=list, description="Extracted topic tags")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Channel metadata")

class PMQueryRequest(BaseModel):
    query: str = Field(..., description="Question from the Product Manager")

@app.get("/health")
def health_check():
    """Returns memory bank stats and system health."""
    stats = agent.memory.get_stats()
    return {
        "status": "online",
        "app_name": config.app_name,
        "hackathon": config.hackathon,
        "hindsight_bank": stats,
    }

@app.post("/api/v1/agent/query")
def query_agent(req: PMQueryRequest):
    """Query the agent with long-term memory retrieval and reflection."""
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    result = agent.query(req.query)
    return result

@app.post("/api/v1/feedback/ingest")
def ingest_feedback(req: IngestFeedbackRequest):
    """Ingest new feedback item in real-time into Hindsight memory."""
    import uuid
    feedback_id = f"fb_{uuid.uuid4().hex[:8]}"
    item = {
        "id": feedback_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "channel": req.channel,
        "author": req.author,
        "account_id": req.account_id,
        "sentiment_score": req.sentiment_score,
        "text": req.text,
        "tags": req.tags,
        "channel_metadata": req.metadata,
    }
    exp_id = agent.ingest_feedback_item(item)
    return {
        "status": "retained",
        "feedback_id": feedback_id,
        "hindsight_experience_id": exp_id,
        "timestamp": item["timestamp"],
    }

@app.get("/api/v1/agent/timeline")
def get_timeline():
    """Retrieve 4-week timeline analytics, sentiment curves, and release impacts."""
    timeseries = agent.sentiment_tracker.analyze_timeseries(agent.raw_feedback)
    correlations = []
    if agent.changelog_correlator:
        correlations = agent.changelog_correlator.correlate_feedback_with_releases(agent.raw_feedback)
    return {
        "daily_trend": timeseries["daily_trend"],
        "channel_breakdown": timeseries["channel_breakdown"],
        "anomalies": timeseries["anomalies"],
        "overall_avg_sentiment": timeseries["overall_avg"],
        "release_correlations": correlations,
    }

@app.get("/api/v1/agent/beliefs")
def get_evolving_beliefs():
    """Retrieve all evolving beliefs from the mental models network."""
    beliefs = agent.memory.embedded_engine.evolving_beliefs
    return {
        "total_count": len(beliefs),
        "beliefs": [b.model_dump() for b in beliefs.values()],
    }

@app.get("/api/v1/agent/report")
def get_executive_report():
    """Generate and return an executive synthesis report in Markdown."""
    markdown_report = report_generator.generate_markdown_report()
    return {
        "format": "markdown",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "content": markdown_report,
    }

if __name__ == "__main__":
    uvicorn.run("api.server:app", host="0.0.0.0", port=8000, reload=True)

