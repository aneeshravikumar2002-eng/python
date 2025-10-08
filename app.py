from flask import Flask, render_template_string
from bs4 import BeautifulSoup
import requests
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    """
    Fetches the title of a webpage and displays it beautifully.
    """
    url = "https://example.com"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.RequestException as e:
        return render_template_string(ERROR_TEMPLATE, error=str(e))

    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.string.strip() if soup.title and soup.title.string else "No title found"

    # Render the result in a beautiful HTML page
    return render_template_string(HTML_TEMPLATE, 
                                  url=url, 
                                  title=title, 
                                  timestamp=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"))

# Simple and elegant HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask Web Scraper</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1d3557, #457b9d);
            color: #f1faee;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
        }
        .card {
            background: rgba(255, 255, 255, 0.1);
            padding: 2rem 3rem;
            border-radius: 15px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.3);
            text-align: center;
        }
        h1 {
            font-size: 2rem;
            color: #fbc531;
            margin-bottom: 1rem;
        }
        a {
            color: #00a8ff;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        p {
            font-size: 1.1rem;
            margin: 0.5rem 0;
        }
        footer {
            margin-top: 2rem;
            font-size: 0.9rem;
            opacity: 0.8;
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>🌐 Flask Web Scraper</h1>
        <p><strong>Target URL:</strong> <a href="{{ url }}" target="_blank">{{ url }}</a></p>
        <p><strong>Page Title:</strong> {{ title }}</p>
        <footer>🕓 Last checked: {{ timestamp }}<br> Crafted with ❤️ by Aneesh</footer>
    </div>
</body>
</html>
"""

# Error page template
ERROR_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Error - Flask Web Scraper</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, sans-serif;
            background: linear-gradient(120deg, #c31432, #240b36);
            color: white;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            text-align: center;
        }
        .error-box {
            background: rgba(255,255,255,0.1);
            padding: 2rem 3rem;
            border-radius: 15px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        }
        h1 {
            color: #ffb142;
        }
    </style>
</head>
<body>
    <div class="error-box">
        <h1>⚠️ Oops! Something went wrong.</h1>
        <p>{{ error }}</p>
        <p>Try again later or check your internet connection.</p>
    </div>
</body>
</html>
"""

if __name__ == '__main__':
    print("✨ Launching Beautiful Flask Web Scraper...")
    app.run(host='0.0.0.0', port=5000, debug=True)

