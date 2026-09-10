"""
Job Aggregator — checks Trade Me for new listings matching IT and
temporary/casual work searches, and sends a Telegram digest per category
for anything not seen before.

Runs daily via .github/workflows/check.yml
"""
import os
import sys

from config import IT_KEYWORDS, TEMP_KEYWORDS, REMOTE_HINTS, LOCATION_HINTS
from sources.trademe import search_jobs, AUCKLAND_REGION_ID
from state import load_seen, save_seen
from notifier import send_telegram, format_message


def job_url(listing_id: int) -> str:
    api_base = os.environ.get("TRADEME_API_BASE", "https://api.trademe.co.nz/v1")
    web_domain = "https://www.tmsandbox.co.nz" if "tmsandbox" in api_base else "https://www.trademe.co.nz"
    return f"{web_domain}/a/jobs/listing/{listing_id}"


def to_job_dict(raw: dict) -> dict:
    return {
        "id": raw["ListingId"],
        "title": raw.get("Title", "Untitled"),
        "company": raw.get("Company") or (raw.get("Agency") or {}).get("Name"),
        "location": raw.get("JobLocation"),
        "url": job_url(raw["ListingId"]),
    }


def matches_it_location(raw: dict) -> bool:
    haystack = " ".join(
        str(raw.get(field, "")) for field in ("Title", "JobLocation", "Body")
    ).lower()
    return any(h in haystack for h in LOCATION_HINTS) or any(
        h in haystack for h in REMOTE_HINTS
    )


def collect_it_jobs() -> dict:
    """Returns {listing_id: job_dict} for IT keyword matches in Auckland/remote."""
    results = {}
    for keyword in IT_KEYWORDS:
        try:
            raw_jobs = search_jobs(keyword)
        except Exception as e:
            print(f"IT search failed for '{keyword}': {e}", file=sys.stderr)
            continue
        for raw in raw_jobs:
            if matches_it_location(raw):
                job = to_job_dict(raw)
                results[job["id"]] = job
    return results


def collect_temp_jobs() -> dict:
    """Returns {listing_id: job_dict} for temp keyword matches in Auckland."""
    results = {}
    for keyword in TEMP_KEYWORDS:
        try:
            raw_jobs = search_jobs(keyword, region=AUCKLAND_REGION_ID)
        except Exception as e:
            print(f"Temp search failed for '{keyword}': {e}", file=sys.stderr)
            continue
        for raw in raw_jobs:
            job = to_job_dict(raw)
            results[job["id"]] = job
    return results


def main():
    seen = load_seen()
    seen_it = set(seen.get("it", []))
    seen_temp = set(seen.get("temp", []))

    it_jobs = collect_it_jobs()
    temp_jobs = collect_temp_jobs()

    new_it = [job for jid, job in it_jobs.items() if jid not in seen_it]
    new_temp = [job for jid, job in temp_jobs.items() if jid not in seen_temp]

    if new_it:
        print(f"{len(new_it)} new IT job(s)")
        for chunk in format_message("💼 IT jobs", new_it):
            send_telegram(chunk)
    else:
        print("No new IT jobs.")

    if new_temp:
        print(f"{len(new_temp)} new temp/casual job(s)")
        for chunk in format_message("🧰 Temp/casual jobs", new_temp):
            send_telegram(chunk)
    else:
        print("No new temp/casual jobs.")

    # Remember everything seen this run (not just the new ones), so results
    # that later drop out of search (e.g. an expired listing) don't cause
    # the seen-list to keep re-growing from scratch.
    save_seen(
        {
            "it": sorted(seen_it | it_jobs.keys()),
            "temp": sorted(seen_temp | temp_jobs.keys()),
        }
    )


if __name__ == "__main__":
    main()
