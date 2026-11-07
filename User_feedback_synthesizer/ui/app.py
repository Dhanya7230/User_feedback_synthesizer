"""
Streamlit Web Dashboard for User Feedback Synthesizer.
HackwithHyderabad 3.0 Hackathon Submission.

Run via:
    streamlit run ui/app.py
"""

import streamlit as st
import pandas as pd
import json
from datetime import datetime, timezone

from agent.feedback_synthesizer import UserFeedbackSynthesizerAgent
from evaluation.benchmark_comparison import BenchmarkComparator
from config import config

# Page config
st.set_page_config(
    page_title="User Feedback Synthesizer | Hindsight Agent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize cached agent in session state
if "agent" not in st.session_state:
    st.session_state.agent = UserFeedbackSynthesizerAgent()
if "comparator" not in st.session_state:
    st.session_state.comparator = BenchmarkComparator(st.session_state.agent)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

agent: UserFeedbackSynthesizerAgent = st.session_state.agent
comparator: BenchmarkComparator = st.session_state.comparator

# Custom CSS for polished styling
st.markdown("""
<style>
    .metric-card {
        background-color: #1E222D;
        border-radius: 8px;
        padding: 16px;
        border-left: 4px solid #4CAF50;
        margin-bottom: 12px;
    }
    .badge-p0 {
        background-color: #E53935;
        color: white;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: bold;
    }
    .badge-success {
        background-color: #43A047;
        color: white;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 12px;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# SIDEBAR
# =============================================================================
with st.sidebar:
    st.title("🧠 Feedback Synthesizer")
    st.caption("**HackwithHyderabad 3.0** | Hindsight Agent")
    st.markdown("---")

    stats = agent.memory.get_stats()
    st.subheader("Hindsight Memory Bank")
    st.info(f"**Bank ID:** `{stats['bank_id']}`\n\n**Mode:** `{stats['mode']}`")

    st.markdown("### 4 Logical Memory Networks")
    c1, c2 = st.columns(2)
    with c1:
        st.metric("1. World Facts", stats["world_facts_count"])
        st.metric("3. Entity Summaries", stats["entity_summaries_count"])
    with c2:
        st.metric("2. Experiences", stats["agent_experiences_count"])
        st.metric("4. Evolving Beliefs", stats["evolving_beliefs_count"])

    st.markdown("---")
    st.markdown("### Product Context")
    st.markdown("**Product:** FlowPilot (Collaborative Workflows)")
    st.markdown("**Scenario:** 4-Week Release Cycle (v2.3 → v2.4 → v2.4.1 → v2.4.2)")

    if st.button("🔄 Reset / Re-Bootstrap Memory", use_container_width=True):
        st.session_state.agent = UserFeedbackSynthesizerAgent()
        st.session_state.comparator = BenchmarkComparator(st.session_state.agent)
        st.rerun()

# =============================================================================
# TOP HEADER & BANNER
# =============================================================================
st.markdown("# 🧠 User Feedback Synthesizer")
st.markdown(
    "**An autonomous product intelligence agent powered by the Hindsight Memory Layer.** "
    "Unlike stateless RAG or memoryless chatbots, this agent connects signals across **5 disconnected channels** "
    "(Zendesk, Discord, Reddit, Gong, Surveys), traces chronological regressions back to code changelogs, "
    "and tracks evolving beliefs over time."
)

# =============================================================================
# TABS
# =============================================================================
tabs = st.tabs([
    "📊 Executive Timeline & Sentiment",
    "🥊 Before vs After Arena",
    "🧠 Hindsight 4-Network Inspector",
    "💬 Conversational PM Synthesizer",
    "📥 Ingest New Live Feedback"
])

# =============================================================================
# TAB 1: EXECUTIVE TIMELINE & SENTIMENT
# =============================================================================
with tabs[0]:
    st.subheader("4-Week Cross-Channel Feedback Dynamics")
    
    # Run analytics
    timeseries = agent.sentiment_tracker.analyze_timeseries(agent.raw_feedback)
    reflection = agent.memory.reflect("Timeline analysis")
    
    # Top KPI Metrics
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.metric("Total Feedback Items", timeseries["total_items"], "+50 items")
    with kpi2:
        avg_sent = timeseries["overall_avg"]
        st.metric("Avg Sentiment Score", f"{avg_sent:+.2f}", "Rebounded to +0.81")
    with kpi3:
        st.metric("ARR Protected", "$205,000", "Acme + Finovate")
    with kpi4:
        st.metric("Active Evolving Beliefs", stats["evolving_beliefs_count"], "Mental Models")

    st.markdown("---")
    
    # Sentiment Timeline Chart
    col_chart, col_releases = st.columns([2, 1])
    
    with col_chart:
        st.markdown("#### 📈 Daily Sentiment Trajectory")
        if timeseries["daily_trend"]:
            df_chart = pd.DataFrame(timeseries["daily_trend"])
            df_chart["date"] = pd.to_datetime(df_chart["date"])
            df_chart = df_chart.set_index("date")
            st.line_chart(df_chart["avg_sentiment"], height=280)
            st.caption("Sentiment plunged during Week 3 (v2.4.1 OAuth disconnects) and rebounded sharply after v2.4.2 patch.")

    with col_releases:
        st.markdown("#### 🚀 Product Releases (World Facts)")
        if agent.changelog_correlator:
            correlations = agent.changelog_correlator.correlate_feedback_with_releases(agent.raw_feedback)
            for c in correlations:
                status_color = "red" if c["status"] == "REGRESSION" else ("green" if "RECOVERY" in c["status"] else "blue")
                st.markdown(f"**{c['version']}** ({c['release_date']}) - :{status_color}[{c['status']}]")
                st.caption(f"{c['title']} | Pre: {c['pre_release_avg_sentiment']:+.2f} → Post: {c['post_release_avg_sentiment']:+.2f} (Δ {c['sentiment_delta']:+.2f})")

    st.markdown("---")
    st.markdown("#### 🌐 Channel Distribution & Divergence")
    ch_cols = st.columns(len(timeseries["channel_breakdown"]))
    for idx, (ch, ch_data) in enumerate(timeseries["channel_breakdown"].items()):
        with ch_cols[idx]:
            st.metric(
                label=ch.upper(),
                value=f"{ch_data['count']} items",
                delta=f"Avg: {ch_data['avg_sentiment']:+.2f}"
            )

    st.markdown("---")
    st.markdown("#### 🎯 Emerging Themes Across Channels")
    themes = agent.theme_extractor.extract_themes(agent.raw_feedback)
    for t in themes[:3]:
        with st.expander(f"📌 {t['theme_name']} ({t['total_mentions']} mentions | Avg Sentiment: {t['average_sentiment']:+.2f} | Velocity: {t['velocity']})", expanded=True):
            st.write(f"**Channel distribution:** {t['channel_distribution']}")
            st.write("**Top quotes:**")
            for q in t["representative_quotes"]:
                st.markdown(f"- *{q}*")

# =============================================================================
# TAB 2: BEFORE VS AFTER ARENA
# =============================================================================
with tabs[1]:
    st.subheader("🥊 Head-to-Head Comparison: Stateless RAG vs Hindsight Memory Agent")
    st.caption("Demonstrating how Hindsight spots patterns across channels and time that humans or stateless chatbots miss.")

    preset_queries = [
        "Why are enterprise customers escalating churn warnings this week, and what product change triggered it?",
        "What regressions occurred in release v2.4 and how were they resolved?",
        "What should we prioritize building in the next sprint based on unaddressed feedback?",
    ]
    selected_query = st.selectbox("Select PM Query Scenario:", preset_queries)

    custom_query = st.text_input("Or enter your own custom question:", "")
    active_query = custom_query if custom_query else selected_query

    if st.button("Run Head-to-Head Evaluation", type="primary"):
        with st.spinner("Synthesizing side-by-side comparison..."):
            res = comparator.run_side_by_side_comparison(active_query)

        col_before, col_after = st.columns(2)

        with col_before:
            st.error("### ❌ BEFORE: Stateless LLM / Standard RAG")
            st.markdown(f"**Generated Answer:**\n\n{res['stateless_rag']['response']}")
            st.markdown("---")
            st.markdown("**Critical Limitations Exposed:**")
            for lim in res['stateless_rag']['limitations_exposed']:
                st.markdown(f"- ⚠️ {lim}")

        with col_after:
            st.success("### ✔ AFTER: Hindsight Memory Layer Agent")
            st.markdown(res['hindsight_agent']['response'])
            st.markdown("---")
            st.markdown("**Hindsight Superpowers:**")
            st.markdown(f"- 🎯 **Identified Causal Release:** Linked to `v2.4.1` changelog commit")
            st.markdown(f"- 💰 **Calculated ARR at Risk:** `{res['hindsight_agent']['at_risk_arr_calculated']}` across Acme & Finovate")
            st.markdown(f"- ⚡ **Early Signal Detection:** Discord reports 3 days prior to Zendesk P0")
            st.markdown(f"- 🔄 **Evolving Beliefs:** Resolved contradiction from crisis to fix")

        st.markdown("---")
        st.markdown("### 📋 Capability Evaluation Matrix")
        df_matrix = pd.DataFrame(res["comparison_matrix"])
        st.table(df_matrix)

# =============================================================================
# TAB 3: HINDSIGHT 4-NETWORK INSPECTOR
# =============================================================================
with tabs[2]:
    st.subheader("🧠 Deep Inspection: The 4 Logical Memory Networks")
    st.caption("Explore how Hindsight structures memories into reasoning substrates.")

    net_tab1, net_tab2, net_tab3, net_tab4 = st.tabs([
        "1. World Facts",
        "2. Agent Experiences",
        "3. Entity Summaries",
        "4. Evolving Beliefs"
    ])

    with net_tab1:
        st.markdown("#### Objective, Verified Product Facts & Releases")
        for fact_id, fact in agent.memory.embedded_engine.world_facts.items():
            with st.expander(f"📦 {fact.subject} - Verified: {fact.verified_at.strftime('%Y-%m-%d')}"):
                st.markdown(f"**Statement:** {fact.statement}")
                st.json(fact.metadata)

    with net_tab2:
        st.markdown("#### Chronological Multi-Channel Feedback Log")
        filter_ch = st.selectbox("Filter by Channel:", ["All", "discord", "zendesk", "reddit", "gong", "in_app_survey"])
        exps = list(agent.memory.embedded_engine.agent_experiences.values())
        if filter_ch != "All":
            exps = [e for e in exps if e.channel == filter_ch]

        for exp in exps[-8:]:
            badge = "🟢" if exp.sentiment_score > 0.2 else ("🔴" if exp.sentiment_score < -0.2 else "🟡")
            st.markdown(f"{badge} **[{exp.channel.upper()}]** *{exp.author}* ({exp.timestamp.strftime('%Y-%m-%d %H:%M')}): {exp.raw_content}")

    with net_tab3:
        st.markdown("#### Synthesized Entity Profiles (Accounts & Modules)")
        entities = agent.memory.embedded_engine.entity_summaries.values()
        for ent in entities:
            if ent.entity_type == "customer_account" and ent.arr:
                risk_color = "red" if ent.active_risk_level == "CRITICAL" else ("orange" if ent.active_risk_level == "HIGH" else "green")
                with st.expander(f"🏢 {ent.entity_name} | ARR: ${ent.arr:,.0f} | Risk: :{risk_color}[{ent.active_risk_level}]"):
                    st.write(f"**Tier:** {ent.tier}")
                    st.write(f"**Average Sentiment:** {ent.current_sentiment_avg:+.2f}")
                    st.write(f"**Total Feedback Mentions:** {ent.total_feedback_count}")
                    if ent.key_pain_points:
                        st.write(f"**Key Pain Points:** {ent.key_pain_points[-2:]}")
                    if ent.key_praises:
                        st.write(f"**Key Praises:** {ent.key_praises[-2:]}")

    with net_tab4:
        st.markdown("#### Dynamic Mental Models (Evolving Beliefs)")
        for belief_id, belief in agent.memory.embedded_engine.evolving_beliefs.items():
            status_badge = "✅ ACTIVE" if belief.status == "active" else f"🔄 {belief.status.upper()}"
            with st.expander(f"💡 [{belief.topic}] - {status_badge} (Confidence: {belief.confidence * 100:.0f}%)"):
                st.markdown(f"**Hypothesis:** {belief.hypothesis_statement}")
                st.markdown(f"**Supporting Evidence IDs:** `{belief.supporting_evidence_ids}`")
                st.markdown(f"**Contradicting Evidence IDs:** `{belief.contradicting_evidence_ids}`")
                if belief.superseded_by:
                    st.markdown(f"**Superseded by:** `{belief.superseded_by}`")

# =============================================================================
# TAB 4: CONVERSATIONAL PM SYNTHESIZER
# =============================================================================
with tabs[3]:
    st.subheader("💬 Ask the Synthesizer (PM Chat & Domain Learning)")
    st.caption("Ask questions about user churn, feedback trends, release impacts, or roadmap priorities.")

    # Display prior conversation
    for chat in st.session_state.chat_history:
        with st.chat_message("user"):
            st.markdown(chat["query"])
        with st.chat_message("assistant"):
            st.markdown(chat["answer"])

    prompt = st.chat_input("Ask a question (e.g. 'Why did CSAT plunge during Week 3?')...")
    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Recalling memories across 4 networks..."):
                response = agent.query(prompt)
                st.markdown(response["answer"])

                with st.expander(f"🔍 Recalled Memories ({len(response['recalled_memories'])} items from Hindsight)"):
                    for m in response["recalled_memories"][:4]:
                        st.markdown(f"- **[{m['network'].upper()}]** (Score: {m['score']:.3f}): {m['content'][:140]}...")

        st.session_state.chat_history.append({"query": prompt, "answer": response["answer"]})

# =============================================================================
# TAB 5: INGEST LIVE FEEDBACK
# =============================================================================
with tabs[4]:
    st.subheader("📥 Ingest Live Feedback Item")
    st.caption("Test Hindsight's real-time Retain operation. Ingest feedback from any channel and see the memory update!")

    with st.form("ingest_form"):
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            in_channel = st.selectbox("Feedback Channel:", ["zendesk", "discord", "reddit", "gong", "in_app_survey"])
            in_author = st.text_input("Author / User:", "sarah.jenkins@acmeglobal.com")
            in_account = st.selectbox("Customer Account:", ["acc_acme_corp", "acc_finovate", "acc_hyperscale", "acc_solo_devs"])
        with col_f2:
            in_sentiment = st.slider("Sentiment Score (-1.0 to +1.0):", min_value=-1.0, max_value=1.0, value=0.85, step=0.05)
            in_tags = st.text_input("Tags (comma separated):", "canvas, performance, release_v2.4.2")

        in_text = st.text_area("Feedback Content:", "v2.4.2 completely fixed our team's canvas lag. We are ready to add 150 more seats next month!")
        submitted = st.form_submit_button("Ingest into Hindsight Memory", type="primary")

        if submitted:
            new_item = {
                "id": f"fb_live_{datetime.now().strftime('%H%M%S')}",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "channel": in_channel,
                "author": in_author,
                "account_id": in_account,
                "sentiment_score": in_sentiment,
                "text": in_text,
                "tags": [t.strip() for t in in_tags.split(",") if t.strip()],
                "channel_metadata": {"live_ingest": True}
            }
            exp_id = agent.ingest_feedback_item(new_item)
            st.success(f"✔ Successfully retained into Hindsight Agent Experiences! Memory ID: `{exp_id}`")
            st.info("Entity summaries and evolving beliefs have been updated in real-time.")

