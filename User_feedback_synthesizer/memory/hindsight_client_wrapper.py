"""
Unified Hindsight Client Wrapper.
Provides a clean, polymorphic interface to either:
1. Live Hindsight daemon / Hindsight Cloud (via official hindsight-client or HTTP REST)
2. Embedded HindsightMemoryEngine (zero-setup local fallback for hackathon demos)
"""

import httpx
from typing import List, Dict, Any, Optional
from datetime import datetime

from config import config
from memory.hindsight_engine import HindsightMemoryEngine
from memory.memory_models import (
    MemoryNetworkType,
    RecallResult,
    ReflectResult,
    AgentExperience,
    WorldFact,
)

class HindsightMemoryClient:
    def __init__(self, mode: Optional[str] = None, bank_id: Optional[str] = None):
        self.mode = mode or config.hindsight_mode
        self.bank_id = bank_id or config.hindsight_bank_id
        self.base_url = config.hindsight_base_url
        self.api_key = config.hindsight_api_key

        # Embedded engine instance
        self.embedded_engine = HindsightMemoryEngine(bank_id=self.bank_id)

        # Attempt to detect live server if configured
        self._is_server_available = False
        if self.mode == "server":
            self._check_server_health()

    def _check_server_health(self) -> bool:
        """Check if external Hindsight server is reachable."""
        try:
            with httpx.Client(timeout=2.0) as client:
                res = client.get(f"{self.base_url}/health")
                if res.status_code == 200:
                    self._is_server_available = True
                    return True
        except Exception:
            self._is_server_available = False
        return False

    def retain(
        self,
        content: str,
        channel: str = "internal_note",
        author: str = "system",
        sentiment_score: float = 0.0,
        account_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
        detected_entities: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None,
    ) -> AgentExperience:
        """
        Retain new experience/feedback in Hindsight memory bank.
        """
        if self.mode == "server" and self._is_server_available:
            try:
                # Call live Hindsight REST / SDK
                payload = {
                    "bank_id": self.bank_id,
                    "content": content,
                    "metadata": {
                        "channel": channel,
                        "author": author,
                        "account_id": account_id,
                        "sentiment_score": sentiment_score,
                        "tags": tags or [],
                        "detected_entities": detected_entities or [],
                        **(metadata or {})
                    }
                }
                headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
                with httpx.Client(timeout=10.0) as client:
                    client.post(f"{self.base_url}/v1/memory/{self.bank_id}/retain", json=payload, headers=headers)
            except Exception as e:
                print(f"Server retain failed, writing to embedded engine fallback: {e}")

        # Always retain into embedded engine for local analytics & fast UI rendering
        import uuid
        exp_id = f"exp_{uuid.uuid4().hex[:8]}"
        return self.embedded_engine.retain_experience(
            experience_id=exp_id,
            channel=channel,
            author=author,
            raw_content=content,
            sentiment_score=sentiment_score,
            timestamp=timestamp,
            account_id=account_id,
            detected_entities=detected_entities or [],
            tags=tags or [],
            channel_metadata=metadata or {},
        )

    def recall(
        self,
        query: str,
        network_types: Optional[List[MemoryNetworkType]] = None,
        channel_filter: Optional[str] = None,
        account_filter: Optional[str] = None,
        top_k: int = 12,
    ) -> List[RecallResult]:
        """
        Recall memories across Hindsight's 4 Logical Networks with multi-dimensional reranking.
        """
        return self.embedded_engine.recall(
            query=query,
            network_types=network_types,
            channel_filter=channel_filter,
            account_filter=account_filter,
            top_k=top_k,
        )

    def reflect(self, query: str) -> ReflectResult:
        """
        Execute high-level Hindsight reflection across memory networks.
        """
        return self.embedded_engine.reflect(query=query)

    def get_stats(self) -> Dict[str, Any]:
        """Return memory network sizes and active bank status."""
        return {
            "bank_id": self.bank_id,
            "mode": self.mode,
            "live_server_connected": self._is_server_available,
            "world_facts_count": len(self.embedded_engine.world_facts),
            "agent_experiences_count": len(self.embedded_engine.agent_experiences),
            "entity_summaries_count": len(self.embedded_engine.entity_summaries),
            "evolving_beliefs_count": len(self.embedded_engine.evolving_beliefs),
        }

