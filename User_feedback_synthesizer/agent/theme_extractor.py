"""
Cross-Channel Emerging Theme Extractor.
Clusters feedback across Discord, Zendesk, Reddit, Gong, and Surveys
to discover cross-cutting patterns and track theme velocity over time.
"""

from typing import List, Dict, Any
from collections import defaultdict
import re

class ThemeExtractor:
    def __init__(self):
        # Known semantic theme mappings
        self.theme_rules = {
            "Canvas Engine Performance": ["canvas", "webgl", "gpu", "zoom", "lag", "fps", "buttery", "infinite canvas", "memory_leak"],
            "Enterprise SSO & Authentication": ["sso", "okta", "azure", "saml", "login", "logged out", "token", "refresh", "disconnect", "session"],
            "Export & Handoff Stability": ["export", "pdf", "svg", "png", "vector", "worker timeout", "hangs"],
            "Figma & Design Tool Integrations": ["figma", "frame", "notion", "import", "integration", "mermaid"],
            "Enterprise Access Control (RBAC)": ["rbac", "permissions", "roles", "workspace", "admin", "view-only", "soc2", "audit"],
            "Data Loss & Offline Save": ["lost", "unsaved", "data_loss", "localstorage", "indexeddb", "offline", "backup"],
        }

    def extract_themes(self, feedback_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Groups feedback items into structured theme dossiers with:
        - Volume & channel distribution
        - Average sentiment
        - Timeline velocity (growing vs fading)
        - Key user quotes
        - High-impact accounts affected
        """
        theme_buckets = defaultdict(lambda: {
            "items": [],
            "channels": defaultdict(int),
            "accounts": set(),
            "sentiment_scores": [],
            "dates": []
        })

        for item in feedback_items:
            text = (item.get("text", "") + " " + " ".join(item.get("tags", []))).lower()
            matched_themes = []

            for theme_name, keywords in self.theme_rules.items():
                if any(kw in text for kw in keywords):
                    matched_themes.append(theme_name)

            if not matched_themes:
                matched_themes.append("General Usability & Feedback")

            for theme in matched_themes:
                b = theme_buckets[theme]
                b["items"].append(item)
                b["channels"][item.get("channel", "unknown")] += 1
                if item.get("account_id"):
                    b["accounts"].add(item.get("account_id"))
                b["sentiment_scores"].append(item.get("sentiment_score", 0.0))
                b["dates"].append(item.get("timestamp", "")[:10])

        theme_summaries = []
        for theme_name, data in theme_buckets.items():
            count = len(data["items"])
            avg_sent = round(sum(data["sentiment_scores"]) / max(count, 1), 2)
            
            # Determine velocity: compare first half of dates to second half
            dates_sorted = sorted(data["dates"])
            midpoint = len(dates_sorted) // 2
            first_half = dates_sorted[:midpoint]
            second_half = dates_sorted[midpoint:]
            velocity = "ACCELERATING" if len(second_half) > len(first_half) * 1.2 else ("FADING" if len(second_half) < len(first_half) * 0.8 else "STEADY")

            # Extract 2-3 most representative quotes
            representative_quotes = [
                f"[{it['channel'].upper()}] \"{it['text'][:120]}...\""
                for it in sorted(data["items"], key=lambda x: abs(x.get("sentiment_score", 0)), reverse=True)[:3]
            ]

            theme_summaries.append({
                "theme_name": theme_name,
                "total_mentions": count,
                "average_sentiment": avg_sent,
                "sentiment_status": "CRITICAL" if avg_sent <= -0.4 else ("WARNING" if avg_sent < 0.1 else "POSITIVE"),
                "velocity": velocity,
                "channel_distribution": dict(data["channels"]),
                "affected_accounts_count": len(data["accounts"]),
                "representative_quotes": representative_quotes,
            })

        # Sort themes by urgency: most negative & highest mention count first
        theme_summaries.sort(key=lambda x: (x["average_sentiment"], -x["total_mentions"]))
        return theme_summaries

