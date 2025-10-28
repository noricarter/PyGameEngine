import os
import sqlite3
import sys
from pathlib import Path
from typing import List, Tuple
from settings import APP_NAME

def user_data_dir() -> Path:
    if sys.platform.startswith("win"):
        base = os.getenv("LOCALAPPDATA") or str(Path.home() / "AppData/Local")
        d = Path(base) / APP_NAME
    elif sys.platform == "darwin":
        d = Path.home() / "Library" / "Application Support" / APP_NAME
    else:
        d = Path.home() / f".{APP_NAME.lower()}"
    Path(d).mkdir(parents=True, exist_ok=True)
    return Path(d)

DB_PATH = user_data_dir() / "scores.db"

def db_connect():
    conn = sqlite3.connect(DB_PATH)
    with conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS scores(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player TEXT NOT NULL,
                points INTEGER NOT NULL,
                ts DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
    return conn

def add_score(player: str, points: int) -> None:
    player = (player or "Player").strip() or "Player"
    with db_connect() as conn:
        conn.execute("INSERT INTO scores(player, points) VALUES (?, ?)", (player, points))

def best_score() -> int:
    with db_connect() as conn:
        cur = conn.execute("SELECT MAX(points) FROM scores")
        (mx,) = cur.fetchone()
        return mx or 0

def top_scores(limit: int = 5) -> List[Tuple[str, int]]:
    with db_connect() as conn:
        cur = conn.execute(
            "SELECT player, points FROM scores ORDER BY points DESC, ts ASC LIMIT ?",
            (limit,),
        )
        return list(cur.fetchall())
