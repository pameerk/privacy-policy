import requests
from bs4 import BeautifulSoup

# GitHub root policy file
HTML_FILE = "index.html"

# Your Google Play developer page
DEV_URL = "https://play.google.com/store/apps/dev?id=6473130867112636101"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}

# Fetch page
response = requests.get(DEV_URL, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

# Extract game titles
titles = set()

# Find all app link elements
for link in soup.find_all("a", href=True):
    href = link["href"]
    if "/store/apps/details?id=" in href:
        # Use title text (Google Play links often include the app name)
        text = link.get("aria-label") or link.text
        text = text.strip()
        if text:
            titles.add(text)

# Sort and format
sorted_titles = sorted(titles)
games_list_html = "\n".join(f"<li>{title}</li>" for title in sorted_titles)

# Read existing HTML
with open(HTML_FILE, "r", encoding="utf-8") as f:
    html_content = f.read()

# Replace marker
if "<!-- GAME_LIST -->" not in html_content:
    raise ValueError("Marker <!-- GAME_LIST --> not found in index.html")

new_html = html_content.replace("<!-- GAME_LIST -->", games_list_html)

# Write updated HTML
with open(HTML_FILE, "w", encoding="utf-8") as f:
    f.write(new_html)

print(f"✅ Updated {HTML_FILE} with {len(sorted_titles)} games.")
