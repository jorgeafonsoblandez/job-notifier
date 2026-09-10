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


def format_message(title: str, jobs: list[dict]) -> list[str]:
    """Splits jobs into batches of 5 to avoid Telegram character limits."""
    chunks = []
    batch_size = 5
    for i in range(0, len(jobs), batch_size):
        batch = jobs[i:i + batch_size]
        lines = [f"{title} ({i+1}-{i+len(batch)} of {len(jobs)})", ""]
        for job in batch:
            lines.append(f"🔹 {job['title']}")
            bits = [b for b in [job.get("company"), job.get("location")] if b]
            if bits:
                lines.append(" · ".join(bits))
            lines.append(job["url"])
            lines.append("")
        chunks.append("\n".join(lines).strip())
    return chunks
