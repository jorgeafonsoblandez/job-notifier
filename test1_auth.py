"""
Test 1 — confirm the Trade Me Jobs API sandbox credentials work.

Trade Me uses OAuth 1.0a with the PLAINTEXT signature method, which is safe
here because everything goes over HTTPS. That means we don't need a special
OAuth-signing library — we can build the Authorization header by hand.

pip install requests
"""

import urllib.parse
import requests

# --- Sandbox credentials (swap for production ones later) ---
CONSUMER_KEY = "6930B5025815833B77317809FA27F50B"
CONSUMER_SECRET = "A63CD75E17F1A81A1A4FEC5C6E316041"
OAUTH_TOKEN = "BDFD0ADFA97F677F9A7F2D8E7AEF8AAA"
OAUTH_TOKEN_SECRET = "6FD8F76475D5D038B440404834217CA8"

# Sandbox base URL — swap "tmsandbox.co.nz" for "trademe.co.nz" for production
BASE_URL = "https://api.tmsandbox.co.nz/v1/Search/Jobs.json"


def build_auth_header() -> str:
    # PLAINTEXT signature = urlencoded(consumer_secret) & urlencoded(token_secret)
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


def main():
    headers = {"Authorization": build_auth_header()}
    params = {
        "search_string": ".NET Developer",
        "rows": 10,
    }
    resp = requests.get(BASE_URL, headers=headers, params=params, timeout=20)
    print("Status:", resp.status_code)
    print(resp.text[:2000])


if __name__ == "__main__":
    main()
