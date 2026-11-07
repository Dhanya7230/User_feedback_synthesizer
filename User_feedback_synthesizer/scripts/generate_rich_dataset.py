"""
Deterministic generator to enrich synthetic feedback dataset with realistic, high-signal records
spanning 4 weeks across 5 distinct channels.
"""

import json
from datetime import datetime, timedelta

def enrich_dataset():
    with open("data/synthetic_feedback.json", "r", encoding="utf-8") as f:
        existing = json.load(f)
    
    additional_items = [
        # Week 1: High praise & feature ideas
        {
            "id": "fb_031",
            "timestamp": "2026-10-02T16:30:00Z",
            "channel": "reddit",
            "author": "u/devops_ninja",
            "account_id": "acc_solo_devs",
            "category": "praise",
            "sentiment_score": 0.85,
            "text": "Switched from Miro to FlowPilot for Kubernetes topology diagrams. The speed difference is night and day.",
            "tags": ["canvas", "performance", "praise"],
            "channel_metadata": {"subreddit": "r/devops", "upvotes": 67}
        },
        {
            "id": "fb_032",
            "timestamp": "2026-10-04T11:00:00Z",
            "channel": "gong",
            "author": "Elena Rostova",
            "account_id": "acc_hyperscale",
            "category": "account_review",
            "sentiment_score": 0.80,
            "text": "Transcript snippet: 'Our 45 designers are really enjoying FlowPilot. The shared cursors make design crits lively. If we could get Figma frame sync and role permissions, this will be our default design board.'",
            "tags": ["figma", "rbac", "hyperscale", "praise"],
            "channel_metadata": {"call_id": "gong_8790", "arr": 24000, "stage": "Customer Success QBR"}
        },
        {
            "id": "fb_033",
            "timestamp": "2026-10-05T14:15:00Z",
            "channel": "in_app_survey",
            "author": "sam@fintechhub.com",
            "account_id": "acc_solo_devs",
            "category": "feature_request",
            "sentiment_score": 0.70,
            "text": "Would love an option to export boards to SVG code or embed directly in Notion docs.",
            "tags": ["export", "svg", "notion"],
            "channel_metadata": {"nps_score": 9, "role": "Product Lead"}
        },
        {
            "id": "fb_034",
            "timestamp": "2026-10-06T18:20:00Z",
            "channel": "discord",
            "author": "maya_ux",
            "account_id": "acc_solo_devs",
            "category": "feature_request",
            "sentiment_score": 0.75,
            "text": "Any roadmap updates on Mermaid.js import and Figma component paste? Would save hours of rework.",
            "tags": ["figma", "mermaid", "feature_request"],
            "channel_metadata": {"channel_name": "#ideas", "reactions": {"heart": 15}}
        },
        {
            "id": "fb_035",
            "timestamp": "2026-10-07T09:10:00Z",
            "channel": "zendesk",
            "author": "admin@cloudtech.co",
            "account_id": "acc_solo_devs",
            "category": "ticket",
            "sentiment_score": 0.60,
            "text": "Is there a webhook triggered whenever an architectural board is finalized or tagged as 'Approved'?",
            "tags": ["webhooks", "integration", "enterprise"],
            "channel_metadata": {"ticket_id": "ZD-4115", "priority": "normal", "tier": "Pro"}
        },

        # Week 2: Post v2.4 (Oct 10-15) subtle degradation & memory leak whispers
        {
            "id": "fb_036",
            "timestamp": "2026-10-11T16:40:00Z",
            "channel": "reddit",
            "author": "u/chrome_watcher",
            "account_id": "acc_solo_devs",
            "category": "early_warning",
            "sentiment_score": -0.10,
            "text": "Anyone experiencing fans spinning up at max RPM after opening FlowPilot boards on v2.4? Activity monitor shows 'Google Chrome Helper (GPU)' pinned at 100%.",
            "tags": ["canvas", "gpu", "memory_leak"],
            "channel_metadata": {"subreddit": "r/chrome", "upvotes": 19}
        },
        {
            "id": "fb_037",
            "timestamp": "2026-10-12T13:25:00Z",
            "channel": "in_app_survey",
            "author": "architect_bob@enterprise.com",
            "account_id": "acc_acme_corp",
            "category": "complaint",
            "sentiment_score": -0.30,
            "text": "Board feels slightly jittery when zooming into large diagrams with 400+ nodes. Exporting to PDF failed twice today.",
            "tags": ["canvas", "export", "performance"],
            "channel_metadata": {"nps_score": 5, "role": "Senior Cloud Architect"}
        },
        {
            "id": "fb_038",
            "timestamp": "2026-10-13T11:05:00Z",
            "channel": "discord",
            "author": "liam_frontend",
            "account_id": "acc_solo_devs",
            "category": "bug_report",
            "sentiment_score": -0.35,
            "text": "On Firefox 131, the v2.4 WebWorker crashes with NS_ERROR_OUT_OF_MEMORY during zoom-out.",
            "tags": ["canvas", "firefox", "memory_leak"],
            "channel_metadata": {"channel_name": "#bugs", "replies": 5}
        },
        {
            "id": "fb_039",
            "timestamp": "2026-10-14T17:15:00Z",
            "channel": "zendesk",
            "author": "ops@fintechscale.com",
            "account_id": "acc_solo_devs",
            "category": "ticket",
            "sentiment_score": -0.40,
            "text": "High priority: PDF export hangs at 99%. Our executives need board presentations by tomorrow 9 AM.",
            "tags": ["export", "pdf", "priority_high"],
            "channel_metadata": {"ticket_id": "ZD-4172", "priority": "high", "tier": "Pro"}
        },
        {
            "id": "fb_040",
            "timestamp": "2026-10-15T12:00:00Z",
            "channel": "gong",
            "author": "Sarah Jenkins",
            "account_id": "acc_acme_corp",
            "category": "cs_sync",
            "sentiment_score": -0.20,
            "text": "Transcript snippet: 'We noticed some browser slowdowns during our quarterly planning mapping. The team loves the tool but our enterprise architects need reassurance that canvas memory stability is under control.'",
            "tags": ["acme", "canvas", "stability_concern"],
            "channel_metadata": {"call_id": "gong_8892", "arr": 120000, "stage": "Mid-Contract Health Check"}
        },

        # Week 3: Post v2.4.1 (Oct 16-22) SSO Crisis & Escalations
        {
            "id": "fb_041",
            "timestamp": "2026-10-17T16:50:00Z",
            "channel": "in_app_survey",
            "author": "security_analyst@finovate.com",
            "account_id": "acc_finovate",
            "category": "csat_drop",
            "sentiment_score": -0.95,
            "text": "Kicked out to login screen while editing threat model. Lost all unsaved notes. Completely unacceptable for an enterprise product. Score: 0/10.",
            "tags": ["auth", "sso", "data_loss", "finovate"],
            "channel_metadata": {"nps_score": 0, "role": "IT Security Analyst"}
        },
        {
            "id": "fb_042",
            "timestamp": "2026-10-18T11:30:00Z",
            "channel": "zendesk",
            "author": "it_admin@acmeglobal.com",
            "account_id": "acc_acme_corp",
            "category": "p0_escalation",
            "sentiment_score": -0.90,
            "text": "ZD-4201 update: Our Okta SSO logs indicate FlowPilot is making auth token refresh calls every 45 minutes with invalid state parameters, triggering a forced session revocation. Fix this immediately or we will shut down the integration.",
            "tags": ["auth", "sso", "okta", "p0_escalation"],
            "channel_metadata": {"ticket_id": "ZD-4201-UPD", "priority": "urgent", "tier": "Enterprise Tier 1"}
        },
        {
            "id": "fb_043",
            "timestamp": "2026-10-19T14:10:00Z",
            "channel": "reddit",
            "author": "u/sre_daily",
            "account_id": "acc_solo_devs",
            "category": "criticism",
            "sentiment_score": -0.70,
            "text": "FlowPilot engineering shipped a hotfix (v2.4.1) that somehow tied session renewal to a fixed 45m timer without background refresh mutex. If you have 3 tabs open, tab 2 revokes tab 1's token. Classic race condition.",
            "tags": ["auth", "race_condition", "sso"],
            "channel_metadata": {"subreddit": "r/devops", "upvotes": 95}
        },
        {
            "id": "fb_044",
            "timestamp": "2026-10-20T17:00:00Z",
            "channel": "discord",
            "author": "chloe_dev",
            "account_id": "acc_solo_devs",
            "category": "frustration",
            "sentiment_score": -0.65,
            "text": "Lost my diagram twice today because of the session expired modal. At least auto-save to IndexedDB or localStorage so work isn't wiped!",
            "tags": ["auth", "data_loss", "offline_save"],
            "channel_metadata": {"channel_name": "#bugs", "reactions": {"crying": 18}}
        },
        {
            "id": "fb_045",
            "timestamp": "2026-10-21T09:30:00Z",
            "channel": "zendesk",
            "author": "elena.r@hyperscale.io",
            "account_id": "acc_hyperscale",
            "category": "escalation",
            "sentiment_score": -0.75,
            "text": "Our designers are refusing to use FlowPilot until the session logout issue is fixed. Several team members had to redo their wireframes from scratch.",
            "tags": ["sso", "adoption_blocker", "hyperscale"],
            "channel_metadata": {"ticket_id": "ZD-4235", "priority": "high", "tier": "Growth"}
        },

        # Week 4: Post v2.4.2 (Oct 24-29) Relief, Recovery, and Evolving Long-Term Roadmap
        {
            "id": "fb_046",
            "timestamp": "2026-10-25T14:20:00Z",
            "channel": "discord",
            "author": "vikram_fintech",
            "account_id": "acc_solo_devs",
            "category": "praise",
            "sentiment_score": 0.80,
            "text": "Ran a 4-hour uninterrupted sprint on v2.4.2 today. No logouts, no tab lag. Huge thank you to the team for fixing the token race condition so fast!",
            "tags": ["release_v2.4.2", "auth_fixed", "praise"],
            "channel_metadata": {"channel_name": "#general", "reactions": {"rocket": 25, "clap": 19}}
        },
        {
            "id": "fb_047",
            "timestamp": "2026-10-26T15:30:00Z",
            "channel": "in_app_survey",
            "author": "security_analyst@finovate.com",
            "account_id": "acc_finovate",
            "category": "csat_rebound",
            "sentiment_score": 0.85,
            "text": "Session stability has been rock solid over 48 hours of testing. CSAT back to 9/10. Ready for contract sign-off.",
            "tags": ["csat_rebound", "finovate", "sso_fixed"],
            "channel_metadata": {"nps_score": 9, "role": "IT Security Analyst"}
        },
        {
            "id": "fb_048",
            "timestamp": "2026-10-27T10:15:00Z",
            "channel": "zendesk",
            "author": "sarah.jenkins@acmeglobal.com",
            "account_id": "acc_acme_corp",
            "category": "strategic_inquiry",
            "sentiment_score": 0.82,
            "text": "Now that v2.4.2 has resolved our enterprise stability concerns, we'd like to schedule a call with your Product team to discuss our Q1 expansion: workspace-level RBAC and audit logging for SOC2.",
            "tags": ["rbac", "soc2", "enterprise_expansion", "acme"],
            "channel_metadata": {"ticket_id": "ZD-4280", "priority": "normal", "tier": "Enterprise Tier 1"}
        },
        {
            "id": "fb_049",
            "timestamp": "2026-10-28T16:00:00Z",
            "channel": "gong",
            "author": "Elena Rostova",
            "account_id": "acc_hyperscale",
            "category": "account_review",
            "sentiment_score": 0.88,
            "text": "Transcript snippet: 'The v2.4.2 update completely saved our team's workflow. Export is instant and nobody gets kicked out anymore. We are expanding from 45 to 80 seats next month. Please prioritize the Figma import!'",
            "tags": ["expansion", "hyperscale", "figma", "praise"],
            "channel_metadata": {"call_id": "gong_9045", "arr": 42000, "stage": "Expansion Agreement"}
        },
        {
            "id": "fb_050",
            "timestamp": "2026-10-29T18:00:00Z",
            "channel": "reddit",
            "author": "u/saas_veteran",
            "account_id": "acc_solo_devs",
            "category": "review_update",
            "sentiment_score": 0.82,
            "text": "Updating my previous complaint: FlowPilot dev team pushed v2.4.2 which squashed both bugs cleanly and added offline persistence. Staying with them, great engineering turnaround.",
            "tags": ["praise", "turnaround", "retention"],
            "channel_metadata": {"subreddit": "r/SaaS", "upvotes": 112}
        }
    ]
    
    # Merge existing with new ensuring no duplicate IDs
    existing_ids = {x["id"] for x in existing}
    for item in additional_items:
        if item["id"] not in existing_ids:
            existing.append(item)
            existing_ids.add(item["id"])
            
    # Sort chronologically
    existing.sort(key=lambda x: x["timestamp"])
    
    with open("data/synthetic_feedback.json", "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2)
        
    print(f"Successfully generated and saved {len(existing)} enriched feedback items.")

if __name__ == "__main__":
    enrich_dataset()

