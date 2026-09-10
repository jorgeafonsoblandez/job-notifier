import os
import requests

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")


def send_telegram(message: str):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        raise ValueError("Missing TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID secrets.")
        return
    resp = requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        data={"chat_id": TELEGRAM_CHAT_ID, "text": message, "disable_web_page_preview": True},
        timeout=10,
    )
    resp.raise_for_status()


def format_message(title: str, jobs: list[dict]) -> str:
    """jobs: list of {"title", "company", "location", "url"}"""
    lines = [f"{title} ({len(jobs)} new)", ""]
    for job in jobs:
        lines.append(f"🔹 {job['title']}")
        bits = [b for b in [job.get("company"), job.get("location")] if b]
        if bits:
            lines.append(" · ".join(bits))
        lines.append(job["url"])
        lines.append("")
    return "\n".join(lines).strip()
