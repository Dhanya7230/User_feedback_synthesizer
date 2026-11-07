"""
Data models and schemas for Hindsight's 4 Logical Memory Networks:
1. World Facts
2. Agent Experiences
3. Synthesized Entity Summaries
4. Evolving Beliefs
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field
from enum import Enum

class MemoryNetworkType(str, Enum):
    WORLD_FACT = "world_facts"
    AGENT_EXPERIENCE = "agent_experiences"
    ENTITY_SUMMARY = "entity_summaries"
    EVOLVING_BELIEF = "evolving_beliefs"

class FeedbackChannel(str, Enum):
    ZENDESK = "zendesk"
    DISCORD = "discord"
    REDDIT = "reddit"
    GONG = "gong"
    IN_APP_SURVEY = "in_app_survey"
    INTERNAL_NOTE = "internal_note"

class WorldFact(BaseModel):
    """Objective, verified product, technical, or business facts."""
    fact_id: str
    category: str  # e.g., "release", "spec", "architecture", "pricing", "sla"
    subject: str
    statement: str
    verified_at: datetime
    source: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    tags: List[str] = Field(default_factory=list)

class AgentExperience(BaseModel):
    """Chronological episodic memory of feedback events or agent-PM dialogues."""
    experience_id: str
    timestamp: datetime
    channel: str
    author: str
    account_id: Optional[str] = None
    raw_content: str
    sentiment_score: float = 0.0  # -1.0 to 1.0
    detected_entities: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    channel_metadata: Dict[str, Any] = Field(default_factory=dict)
    linked_release_version: Optional[str] = None

class EntitySummary(BaseModel):
    """Dynamic profile for key customers, accounts, or product modules."""
    entity_id: str  # e.g., "acc_acme_corp" or "module_auth"
    entity_name: str
    entity_type: str  # "customer_account" or "product_module"
    tier: Optional[str] = None
    arr: Optional[float] = None
    total_feedback_count: int = 0
    sentiment_history: List[Dict[str, Any]] = Field(default_factory=list)
    current_sentiment_avg: float = 0.0
    key_pain_points: List[str] = Field(default_factory=list)
    key_praises: List[str] = Field(default_factory=list)
    feature_requests: List[str] = Field(default_factory=list)
    last_updated: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    active_risk_level: str = "LOW"  # LOW, MEDIUM, HIGH, CRITICAL

class EvolvingBelief(BaseModel):
    """
    Dynamic mental models that update as new feedback arrives,
    resolving contradictions and tracking hypothesis confidence.
    """
    belief_id: str
    topic: str
    hypothesis_statement: str
    confidence: float = 0.5  # 0.0 to 1.0
    supporting_evidence_ids: List[str] = Field(default_factory=list)
    contradicting_evidence_ids: List[str] = Field(default_factory=list)
    evolution_history: List[Dict[str, Any]] = Field(default_factory=list)
    last_revised: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    status: str = "active"  # "active", "superseded", "confirmed", "refuted"
    superseded_by: Optional[str] = None

class RecallResult(BaseModel):
    """Result of multi-network retrieval with reranking scores."""
    item_id: str
    network_type: MemoryNetworkType
    content: str
    timestamp: Optional[datetime] = None
    score: float
    relevance_breakdown: Dict[str, float] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ReflectResult(BaseModel):
    """Structured high-level synthesis generated across memories."""
    query: str
    executive_summary: str
    cross_channel_patterns: List[str]
    sentiment_shift_detected: Dict[str, Any]
    linked_product_changes: List[Dict[str, Any]]
    account_impacts: List[Dict[str, Any]]
    actionable_recommendations: List[str]
    retrieved_memory_count: int
    confidence_score: float
    temporal_span: str

