import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for
from fetcher import get_today_matches, get_yesterday_matches, get_tomorrow_matches
from datetime import datetime

load_dotenv()

API_KEY = os.getenv("PANDASCORE_API_KEY")

app = Flask(__name__)

last_updated = None

schema_org = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "Esports Matches",
    "url": "http://127.0.0.1:5000",
    "logo": "http://127.0.0.1:5000/static/logo.png"
}


@app.route("/")
def home():
    return render_template(
        "index.html",
        meta_description="Главная страница сайта с киберспортивными матчами за вчера, сегодня и завтра.",
        schema_org=schema_org,
        last_updated=last_updated
    )


@app.route("/matches/today")
def today():
    matches = get_today_matches()
    return render_template(
        "today.html",
        title="Матчи за сегодня",
        matches=matches,
        meta_description="Киберспортивные матчи за сегодня: Counter-Strike, Dota 2 и League of Legends.",
        schema_org=schema_org
    )


@app.route("/matches/yesterday")
def yesterday():
    matches = get_yesterday_matches()
    return render_template(
        "today.html",
        title="Матчи за вчера",
        matches=matches,
        meta_description="Результаты и завершённые киберспортивные матчи за вчера.",
        schema_org=schema_org
    )


@app.route("/matches/tomorrow")
def tomorrow():
    matches = get_tomorrow_matches()
    return render_template(
        "today.html",
        title="Матчи за завтра",
        matches=matches,
        meta_description="Предстоящие киберспортивные матчи за завтра.",
        schema_org=schema_org
    )

@app.route("/generate", methods=["POST"])
def generate():
    global last_updated

    get_yesterday_matches()
    get_today_matches()
    get_tomorrow_matches()

    last_updated = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)