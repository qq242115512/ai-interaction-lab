"""
SQLite-based session store — replaces in-memory dict for session persistence.
Community standard: PostgreSQL or SQLite for production data storage.

Benefits over memory dict:
  - Survives server restarts
  - No data loss on deploy
  - Can query/backup session data
  - Same API as dict for minimal code changes
"""

import json
import sqlite3
import threading
import time

from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "sessions.db"


class SessionStore:
    """Thread-safe SQLite-backed session store with dict-like interface.

    Usage — drop-in replacement for `sessions: dict[str, dict]`:
        store = SessionStore()
        store["session_id"] = {...}
        session = store.get("session_id")
        del store["session_id"]
    """

    def __init__(self, db_path: str | Path | None = None, ttl: int = 3600):
        self._db_path = Path(db_path or DB_PATH)
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._ttl = ttl
        self._local = threading.local()
        self._init_db()

    def _get_conn(self) -> sqlite3.Connection:
        if not hasattr(self._local, "conn") or self._local.conn is None:
            self._local.conn = sqlite3.connect(str(self._db_path))
            self._local.conn.row_factory = sqlite3.Row
            self._local.conn.execute("PRAGMA journal_mode=WAL")
            self._local.conn.execute("PRAGMA busy_timeout=5000")
            self._local.conn.isolation_level = None  # Auto-commit mode
        return self._local.conn

    def _retry_write(self, fn, max_retries=3):
        """Retry on SQLite lock with exponential backoff."""
        for attempt in range(max_retries):
            try:
                return fn()
            except sqlite3.OperationalError as e:
                if "locked" in str(e).lower() and attempt < max_retries - 1:
                    time.sleep(0.1 * (2 ** attempt))
                else:
                    raise

    def _init_db(self):
        conn = self._get_conn()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                data TEXT NOT NULL,
                created_at REAL NOT NULL,
                accessed_at REAL NOT NULL
            )
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_sessions_accessed
            ON sessions(accessed_at)
        """)
        conn.commit()

    def __getitem__(self, session_id: str) -> dict:
        session = self.get(session_id)
        if session is None:
            raise KeyError(session_id)
        return session

    def __setitem__(self, session_id: str, data: dict):
        def _write():
            conn = self._get_conn()
            now = time.time()
            json_data = json.dumps(data, ensure_ascii=False)
            conn.execute(
                """INSERT OR REPLACE INTO sessions (id, data, created_at, accessed_at)
                   VALUES (?, ?, COALESCE((SELECT created_at FROM sessions WHERE id=?), ?), ?)""",
                (session_id, json_data, session_id, now, now),
            )
        self._retry_write(_write)

    def __delitem__(self, session_id: str):
        conn = self._get_conn()
        conn.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
        conn.commit()

    def __contains__(self, session_id: str) -> bool:
        return self.get(session_id) is not None

    def __len__(self) -> int:
        conn = self._get_conn()
        self._cleanup(conn)
        row = conn.execute("SELECT COUNT(*) as c FROM sessions").fetchone()
        return row["c"]

    def get(self, session_id: str) -> dict | None:
        conn = self._get_conn()
        row = conn.execute(
            "SELECT data, created_at FROM sessions WHERE id = ?", (session_id,)
        ).fetchone()
        if row is None:
            return None

        # Check TTL
        if time.time() - row["created_at"] > self._ttl:
            conn.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
            conn.commit()
            return None

        # Update access time
        conn.execute(
            "UPDATE sessions SET accessed_at = ? WHERE id = ?",
            (time.time(), session_id),
        )
        conn.commit()

        data = json.loads(row["data"])
        data["_created_at"] = row["created_at"]
        return data

    def cleanup(self) -> int:
        """Remove expired sessions. Returns count of removed sessions."""
        conn = self._get_conn()
        cutoff = time.time() - self._ttl
        cursor = conn.execute("DELETE FROM sessions WHERE created_at < ?", (cutoff,))
        conn.commit()
        return cursor.rowcount

    def items(self):
        """Dict-compatible iteration over (key, value) pairs."""
        conn = self._get_conn()
        self._cleanup(conn)
        conn.commit()
        rows = conn.execute(
            "SELECT id, data, created_at FROM sessions WHERE created_at > ?",
            (time.time() - self._ttl,),
        ).fetchall()
        result = []
        for row in rows:
            data = json.loads(row["data"])
            data["_created_at"] = row["created_at"]
            result.append((row["id"], data))
        return result

    def keys(self):
        """Dict-compatible: list of session IDs."""
        return [k for k, v in self.items()]

    def values(self):
        """Dict-compatible: list of session data dicts."""
        return [v for k, v in self.items()]

    def __iter__(self):
        return iter(self.keys())

    def _cleanup(self, conn: sqlite3.Connection):
        cutoff = time.time() - self._ttl
        conn.execute("DELETE FROM sessions WHERE created_at < ?", (cutoff,))

    def close(self):
        if hasattr(self._local, "conn") and self._local.conn:
            self._local.conn.close()
            self._local.conn = None


# Global store instance
store = SessionStore()
