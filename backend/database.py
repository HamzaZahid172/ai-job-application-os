import sqlite3
from pathlib import Path
from typing import List
from backend.models import ApplicationCreate, ApplicationOut

DB_PATH = Path("data/applications.db")

def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            '''
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company TEXT NOT NULL,
                role TEXT NOT NULL,
                match_score INTEGER NOT NULL,
                status TEXT NOT NULL,
                notes TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(company, role)
            )
            '''
        )

def create_application(item: ApplicationCreate) -> ApplicationOut:
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        try:
            cur = conn.execute(
                '''
                INSERT INTO applications(company, role, match_score, status, notes)
                VALUES (?, ?, ?, ?, ?)
                ''',
                (item.company, item.role, item.match_score, item.status, item.notes),
            )
            conn.commit()
        except sqlite3.IntegrityError:
            raise ValueError("Duplicate application: this company and role already exist.")
        row = conn.execute(
            "SELECT * FROM applications WHERE id = ?", (cur.lastrowid,)
        ).fetchone()
    return ApplicationOut(**dict(row))

def list_applications() -> List[ApplicationOut]:
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM applications ORDER BY id DESC"
        ).fetchall()
    return [ApplicationOut(**dict(row)) for row in rows]
