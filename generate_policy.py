import requests
from bs4 import BeautifulSoup

HTML_FILE = "index.html"
DEV_URL = "https://play.google.com/store/apps/dev?id=6473130867112636101"

headers = {"User-Agent": "Mozilla/5.0"}
res = requests.get(DEV_URL, headers=headers)
res.raise_for_status()
soup = BeautifulSoup(res.text, "html.parser")

# Extract game titles
titles = [div.text for div in soup.find_all("div", class_="WsMG1c nnK0zc")]

games_list_html = "\n".join(f"<li>{title}</li>" for title in titles)

# Read template HTML
with open(HTML_FILE, "r", encoding="utf-8") as f:
    html_content = f.read()

# Replace marker
if "<!-- GAME_LIST -->" not in html_content:
    raise ValueError("Marker <!-- GAME_LIST --> not found in index.html")

new_html = html_content.replace("<!-- GAME_LIST -->", games_list_html)

# Write updated HTML
with open(HTML_FILE, "w", encoding="utf-8") as f:
    f.write(new_html)

print(f"✅ Updated {HTML_FILE} with {len(titles)} games.")
