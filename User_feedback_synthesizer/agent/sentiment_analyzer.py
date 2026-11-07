"""
Sentiment Analysis and Temporal Shift Tracker.
Monitors sentiment trajectories across time and channels,
spotting inflection points and alerting on churn risk.
"""

from typing import List, Dict, Any
from datetime import datetime
import pandas as pd
import numpy as np

class SentimentShiftTracker:
    def __init__(self, anomaly_drop_threshold: float = -0.35):
        self.anomaly_threshold = anomaly_drop_threshold

    def analyze_timeseries(self, feedback_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Processes feedback items into daily and weekly sentiment time series,
        breaking down sentiment by channel and detecting critical inflection points.
        """
        if not feedback_items:
            return {
                "daily_trend": [],
                "channel_breakdown": {},
                "anomalies": [],
                "overall_avg": 0.0,
            }

        df = pd.DataFrame(feedback_items)
        df["datetime"] = pd.to_datetime(df["timestamp"])
        df["date"] = df["datetime"].dt.date
        df["week"] = df["datetime"].dt.tz_localize(None).dt.to_period("W").astype(str)

        # 1. Daily Average Sentiment
        daily_grp = df.groupby("date")["sentiment_score"].agg(["mean", "count"]).reset_index()
        daily_trend = [
            {
                "date": str(row["date"]),
                "avg_sentiment": round(float(row["mean"]), 3),
                "volume": int(row["count"]),
            }
            for _, row in daily_grp.iterrows()
        ]

        # 2. Channel-by-Channel Breakdown
        channel_grp = df.groupby("channel")["sentiment_score"].agg(["mean", "count"]).reset_index()
        channel_breakdown = {
            row["channel"]: {
                "avg_sentiment": round(float(row["mean"]), 3),
                "count": int(row["count"]),
            }
            for _, row in channel_grp.iterrows()
        }

        # 3. Detect Steep Drops (Anomalies)
        anomalies = []
        for i in range(1, len(daily_trend)):
            prev = daily_trend[i - 1]["avg_sentiment"]
            curr = daily_trend[i]["avg_sentiment"]
            diff = curr - prev
            if diff <= self.anomaly_threshold:
                anomalies.append({
                    "date": daily_trend[i]["date"],
                    "drop_amount": round(diff, 3),
                    "previous_sentiment": prev,
                    "new_sentiment": curr,
                    "severity": "CRITICAL" if diff <= -0.6 else "WARNING",
                    "description": f"Sharp sentiment drop of {round(diff, 2)} on {daily_trend[i]['date']}"
                })

        overall_avg = round(float(df["sentiment_score"].mean()), 3)

        return {
            "daily_trend": daily_trend,
            "channel_breakdown": channel_breakdown,
            "anomalies": anomalies,
            "overall_avg": overall_avg,
            "total_items": len(df),
        }

    def detect_sentiment_divergence(self, feedback_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Identifies channels that are diverging significantly (e.g. Discord complaining
        while public in-app survey hasn't caught on yet).
        """
        df = pd.DataFrame(feedback_items)
        if df.empty or "channel" not in df.columns:
            return {}

        channel_means = df.groupby("channel")["sentiment_score"].mean().to_dict()
        overall_mean = df["sentiment_score"].mean()

        divergences = {}
        for ch, ch_mean in channel_means.items():
            delta = ch_mean - overall_mean
            if abs(delta) >= 0.20:
                divergences[ch] = {
                    "channel_mean": round(ch_mean, 2),
                    "overall_mean": round(overall_mean, 2),
                    "divergence": round(delta, 2),
                    "direction": "MORE_NEGATIVE" if delta < 0 else "MORE_POSITIVE"
                }
        return divergences

