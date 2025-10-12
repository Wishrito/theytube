import os

from flask import redirect, render_template, request, session, url_for
from youtube_search import YoutubeSearch
from yt_dlp import YoutubeDL
from yt_dlp.utils import YoutubeDLError

from modules.classes import YTBVideo, app, history_bp
from modules.database import init_db

app.secret_key = os.environ.get("FLASK_SECRET_KEY", "development_key")

sqlite_connected = False


def get_video_data(youtube_url: str, cookie: str):
    ydl_opts = {
        "cookiesfrombrowser": ("chrome",),
        "headers": {"Cookie": cookie},
        "quiet": True,
        "format": "best[ext=mp4][protocol=https]",
        "noplaylist": True,
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            return YTBVideo(
                url=info.get("url", ""),
                title=info.get("title", ""),
                duration=info.get("duration", 0),
                thumbnail=info.get("thumbnail", ""),
                channel=info.get("uploader", ""),
                id=info.get("id", ""),
            )
    except YoutubeDLError:
        app.get_cookies()
        get_video_data(youtube_url, app.webCookies)


def history_add(entry: dict):
    try:
        session["history"].append(entry)
    except KeyError:
        session["history"] = [entry]
    session.modified = True


def search_videos(query):
    results = YoutubeSearch(query, max_results=10).to_dict()
    return results


@app.route("/", methods=["GET", "POST"])
def index():
    if "history" not in session:
        session["history"] = []
    match request.method:
        case "GET":
            return render_template("index.j2")
        case "POST":
            query = request.form.get("query")
            return redirect(url_for("search", query=query))
        case _:
            return render_template("index.j2")


@history_bp.route("/", methods=["GET"])
def watch_history():

    history_resolve = session["history"]
    return render_template("history.j2", history=history_resolve)


@history_bp.route("/clear", methods=["POST"])
def clear_history():
    session["history"] = []
    return redirect(url_for("history.watch_history"))


@app.route("/search/<query>", methods=["GET"])
def search(query: str):
    results = search_videos(query)
    return render_template("results.j2", results=results, query=query)


@app.route("/play/<video_id>", methods=["GET", "POST"])
def play(video_id: str):
    video = get_video_data(video_id, app.webCookies)
    query = request.form.get("query", "")
    results = search_videos(query) if query else []
    entry = {
        "title": video.title,
        "video_url": video.url,
        "id": video.id,
        "thumbnail": video.thumbnail,
        "channel": video.channel,
        "duration": video.duration.to_dict(),
    }

    if len(session["history"]) > 0:
        if session["history"][-1]["id"] != video.id:
            history_add(entry)
    else:
        history_add(entry)

    return render_template(
        "player.j2",
        title=video.title,
        video_url=video.url,
        query=query,
        results=results,
    )


# si l'application n'est pas lancée sur Vercel, lancement en mode debug
if app.localhost:
    try:
        init_db()
    except Exception as err:
        print(err)
    app.register_blueprint(history_bp)
    app.run(host="localhost", port=5000, debug=True)
