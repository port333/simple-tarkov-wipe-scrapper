import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template_string, request

app = Flask(__name__)

# Scraper function (unchanged)
def check_for_wipe_posts():
    url = "https://old.reddit.com/r/EscapefromTarkov/search/?q=wipe&restrict_sr=on&t=day"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    wipe_posts = []
    posts = soup.select("div.search-result.search-result-link")
    for post in posts:
        title_elem = post.find("a", class_="search-title")
        if not title_elem:
            continue
        title = title_elem.text.strip()
        
        url_elem = post.find("a", class_="search-title")
        post_url = url_elem["href"].replace("old.reddit.com", "www.reddit.com")  # Convert to regular Reddit
        
        time_elem = post.find("time")
        if not time_elem:
            continue
        post_time = time_elem["datetime"]
        
        wipe_posts.append({
            "title": title,
            "url": post_url,
            "created": post_time
        })
    
    return wipe_posts

# HTML template with added CSS for a fancier look
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Tarkov Wipe Checker</title>
    <style>
        body {
            background-color: #1a1a1a;
            color: #d9d9d9;
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
        }
        h1 {
            color: #ff9900;
            text-align: center;
            text-shadow: 2px 2px 4px #000;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background-color: #2b2b2b;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
        }
        button {
            background-color: #ff9900;
            color: #1a1a1a;
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
            border-radius: 5px;
            transition: background-color 0.3s;
        }
        button:hover {
            background-color: #e68a00;
        }
        h2 {
            color: #ff9900;
            margin-top: 20px;
        }
        ul {
            list-style-type: none;
            padding: 0;
        }
        li {
            background-color: #3c3c3c;
            margin: 10px 0;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #ff9900;
        }
        a {
            color: #ffcc66;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        .no-results {
            color: #999;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Tarkov Wipe Checker</h1>
        <form method="POST">
            <button type="submit">Check for Wipe Posts</button>
        </form>
        {% if results %}
            <h2>Results</h2>
            {% if results|length > 0 %}
                <p>Found {{ results|length }} post(s):</p>
                <ul>
                {% for post in results %}
                    <li>
                        <strong>{{ post.title }}</strong><br>
                        URL: <a href="{{ post.url }}" target="_blank">{{ post.url.replace('https://old.reddit.com', '') }}</a><br>
                        Posted: {{ post.created }}
                    </li>
                {% endfor %}
                </ul>
            {% else %}
                <p class="no-results">No posts found with 'wipe' in title from the last 24 hours.</p>
            {% endif %}
        {% endif %}
    </div>
</body>
</html>
"""

# Flask route (unchanged)
@app.route("/", methods=["GET", "POST"])
def home():
    results = None
    if request.method == "POST":
        results = check_for_wipe_posts()
    return render_template_string(html_template, results=results)

if __name__ == "__main__":
    app.run(debug=True)
