import os
from datetime import datetime, timedelta
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("PANDASCORE_API_KEY")
BASE_URL = "https://api.pandascore.co"


def format_match(match):
    opponents = match.get("opponents", [])

    team_1 = "TBD"
    team_2 = "TBD"

    if len(opponents) > 0 and opponents[0].get("opponent"):
        team_1 = opponents[0]["opponent"].get("name", "TBD")

    if len(opponents) > 1 and opponents[1].get("opponent"):
        team_2 = opponents[1]["opponent"].get("name", "TBD")

    begin_at = match.get("begin_at")
    time_text = "Неизвестно"

    if begin_at:
        try:
            dt = datetime.fromisoformat(begin_at.replace("Z", "+00:00"))
            time_text = dt.strftime("%H:%M")
        except ValueError:
            time_text = begin_at

    videogame = match.get("videogame")
    game_name = "Unknown"

    if videogame:
        game_name = videogame.get("name", "Unknown")

    league = match.get("league")
    league_name = "Unknown league"

    if league:
        league_name = league.get("name", "Unknown league")

    return {
        "game": game_name,
        "team_1": team_1,
        "team_2": team_2,
        "time": time_text,
        "status": match.get("status", "unknown"),
        "league": league_name
    }


def get_matches_for_day(day_offset):
    target_date = datetime.utcnow().date() + timedelta(days=day_offset)

    start_dt = datetime.combine(target_date, datetime.min.time())
    end_dt = datetime.combine(target_date, datetime.max.time())

    url = f"{BASE_URL}/matches"
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    params = {
        "range[begin_at]": f"{start_dt.isoformat()}Z,{end_dt.isoformat()}Z",
        "sort": "begin_at",
        "page[size]": 50
    }

    response = requests.get(url, headers=headers, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()

    allowed_games = {
        "Counter-Strike",
        "Dota 2",
        "League of Legends"
    }

    filtered_matches = []

    for match in data:
        videogame = match.get("videogame")
        game_name = "Unknown"

        if videogame:
            game_name = videogame.get("name", "Unknown")

        if game_name in allowed_games:
            filtered_matches.append(format_match(match))

    return filtered_matches


def get_yesterday_matches():
    return get_matches_for_day(-1)


def get_today_matches():
    return get_matches_for_day(0)


def get_tomorrow_matches():
    return get_matches_for_day(1)