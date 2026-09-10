"""
Test 2 — find the region/district IDs for Auckland and North Shore.

This endpoint is public (no OAuth needed) so it's a simple GET.
"""

import requests

resp = requests.get("https://api.trademe.co.nz/v1/localities.json", timeout=20)
print("Status:", resp.status_code)
localities = resp.json()

for locality in localities:
    name = locality.get("Name", "")
    if "auckland" in name.lower():
        print(f"\nRegion: {name}  (LocalityId: {locality['LocalityId']})")
        for district in locality.get("Districts", []):
            print(f"  District: {district['Name']}  (DistrictId: {district['DistrictId']})")
