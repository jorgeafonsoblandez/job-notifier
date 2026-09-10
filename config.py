"""
Search keyword lists. Edit these to tune what you get notified about.
"""

IT_KEYWORDS = [
    ".NET Developer",
    "IT Support",
    "IT Engineer",
    "Shopify Developer",
    "Ecommerce Manager",
    "SQL Server",
    "API Integrations",
]

TEMP_KEYWORDS = [
    "Warehousing",
    "Events",
    "No experience required",
    "Airport jobs",
    "Trolley boy",
    "Entry level",
]

# Words that mark a listing as remote-friendly, checked against title/body
# for the IT category (which isn't restricted to the Auckland region param).
REMOTE_HINTS = ["remote", "work from home", "wfh"]

# Words that mark a listing as Auckland/North Shore for the IT category.
LOCATION_HINTS = ["auckland", "north shore"]
