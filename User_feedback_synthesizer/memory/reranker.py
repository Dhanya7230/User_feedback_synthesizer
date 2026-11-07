"""
Multi-dimensional reranking engine modeled after Hindsight's hs-rerank-1 architecture.
Balances:
1. Semantic relevance (content similarity)
2. Keyword matching (domain terminology)
3. Temporal distance / freshness weighting
4. Entity significance (ARR, account tier, module criticality)
"""

import math
import re
from datetime import datetime, timezone
from typing import List, Dict, Any
from memory.memory_models import RecallResult

def _normalize_datetime(dt: datetime) -> datetime:
    if dt is None:
        return datetime.now(timezone.utc)
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)

class HindsightReranker:
    def __init__(
        self,
        weight_semantic: float = 0.40,
        weight_keyword: float = 0.25,
        weight_temporal: float = 0.20,
        weight_entity_arr: float = 0.15,
        half_life_days: float = 14.0
    ):
        self.w_semantic = weight_semantic
        self.w_keyword = weight_keyword
        self.w_temporal = weight_temporal
        self.w_entity = weight_entity_arr
        self.half_life_days = half_life_days

    def _tokenize(self, text: str) -> set:
        """Tokenize text into lowercase alphanumeric words."""
        return set(re.findall(r"\b[a-zA-Z0-9_\-\.]{2,}\b", text.lower()))

    def _compute_keyword_score(self, query: str, document_text: str) -> float:
        """Computes Jaccard/overlap score between query tokens and document tokens."""
        q_tokens = self._tokenize(query)
        if not q_tokens:
            return 0.5
        d_tokens = self._tokenize(document_text)
        if not d_tokens:
            return 0.0
        overlap = q_tokens.intersection(d_tokens)
        return len(overlap) / len(q_tokens)

    def _compute_temporal_score(
        self,
        doc_time: datetime,
        reference_time: datetime,
        time_focus_mode: str = "recent"
    ) -> float:
        """
        Computes exponential temporal decay score.
        If time_focus_mode == 'recent', newer memories get higher scores.
        If reference_time is provided (e.g., around an incident), proximity gets higher score.
        """
        if not doc_time:
            return 0.5
        d_time = _normalize_datetime(doc_time)
        r_time = _normalize_datetime(reference_time)
        delta_days = abs((r_time - d_time).total_seconds()) / (24 * 3600)
        # Half-life exponential decay: e^(-lambda * delta)
        decay_constant = math.log(2) / max(self.half_life_days, 1.0)
        score = math.exp(-decay_constant * delta_days)
        return min(max(score, 0.05), 1.0)

    def _compute_entity_weight(self, metadata: Dict[str, Any]) -> float:
        """Calculates entity priority based on enterprise tier, ARR, or severity."""
        base_score = 0.4
        tier = str(metadata.get("tier", "")).lower()
        if "enterprise" in tier:
            base_score += 0.35
        elif "growth" in tier or "team" in tier:
            base_score += 0.20
        elif "pro" in tier:
            base_score += 0.10

        arr = metadata.get("arr", 0)
        if arr and isinstance(arr, (int, float)):
            if arr >= 100000:
                base_score += 0.25
            elif arr >= 50000:
                base_score += 0.15
            elif arr > 0:
                base_score += 0.05

        priority = str(metadata.get("priority", "")).lower()
        if priority in ["urgent", "p0", "high"]:
            base_score += 0.15

        return min(base_score, 1.0)

    def rerank(
        self,
        query: str,
        candidates: List[RecallResult],
        reference_time: datetime = None,
        top_k: int = 15
    ) -> List[RecallResult]:
        """
        Reranks raw candidates across semantic, keyword, temporal, and entity dimensions.
        """
        if reference_time is None:
            reference_time = datetime.utcnow()

        reranked_results = []
        for cand in candidates:
            # Semantic score is passed from candidate generator
            semantic_score = cand.score

            # Keyword overlap
            keyword_score = self._compute_keyword_score(query, cand.content)

            # Temporal score
            temporal_score = self._compute_temporal_score(cand.timestamp, reference_time)

            # Entity weight
            entity_score = self._compute_entity_weight(cand.metadata)

            # Combined weighted score
            final_score = (
                (self.w_semantic * semantic_score) +
                (self.w_keyword * keyword_score) +
                (self.w_temporal * temporal_score) +
                (self.w_entity * entity_score)
            )

            cand.score = round(final_score, 4)
            cand.relevance_breakdown = {
                "semantic": round(semantic_score, 3),
                "keyword": round(keyword_score, 3),
                "temporal": round(temporal_score, 3),
                "entity": round(entity_score, 3)
            }
            reranked_results.append(cand)

        # Sort descending by composite score
        reranked_results.sort(key=lambda x: x.score, reverse=True)
        return reranked_results[:top_k]

