"""
Trade Me Jobs API client.

Uses OAuth 1.0a with the PLAINTEXT signature method — safe here because
everything goes over HTTPS, and it avoids needing a full OAuth-signing
library for what is otherwise a simple read-only GET request.
"""

import os
import urllib.parse
import requests

CONSUMER_KEY = os.environ.get("TRADEME_CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("TRADEME_CONSUMER_SECRET")
OAUTH_TOKEN = os.environ.get("TRADEME_OAUTH_TOKEN")
OAUTH_TOKEN_SECRET = os.environ.get("TRADEME_OAUTH_TOKEN_SECRET")

# Swap "trademe.co.nz" for "tmsandbox.co.nz" to test against the sandbox.
BASE_URL = os.environ.get("TRADEME_API_BASE", "https://api.tmsandbox.co.nz/v1")

AUCKLAND_REGION_ID = 1  # covers Auckland City, North Shore City, etc.


def _auth_header() -> str:
    signature = (
        f"{urllib.parse.quote(CONSUMER_SECRET, safe='')}"
        f"&{urllib.parse.quote(OAUTH_TOKEN_SECRET, safe='')}"
    )
    return (
        f'OAuth oauth_consumer_key="{CONSUMER_KEY}", '
        f'oauth_token="{OAUTH_TOKEN}", '
        f'oauth_signature_method="PLAINTEXT", '
        f'oauth_signature="{signature}"'
    )


def search_jobs(search_string: str, region: int | None = None, rows: int = 50) -> list[dict]:
    """Returns the raw list of Job dicts from the API for one search term."""
    if not all([CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET]):
        raise RuntimeError("Missing one or more TRADEME_* environment variables.")

    params = {
        "search_string": search_string, 
        "rows": rows,
        "sort_order": "ListedDateDesc"
    }
    if region is not None:
        params["locality"] = region

    resp = requests.get(
        f"{BASE_URL}/Search/Jobs.json",
        headers={"Authorization": _auth_header()},
        params=params,
        timeout=20,
    )
    resp.raise_for_status()
    return resp.json().get("List", [])
