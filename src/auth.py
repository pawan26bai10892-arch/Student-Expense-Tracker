"""Registration and login using salted PBKDF2 password hashes."""
import hashlib
import os
import sqlite3

from .logger import get_logger
from .validators import validate_password, validate_username

log = get_logger()


def _hash(password, salt):
    return hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), 100_000).hex()


def register(conn, username, password):
    username, password = validate_username(username), validate_password(password)
    salt = os.urandom(16).hex()
    try:
        cur = conn.execute("INSERT INTO users(username,salt,password_hash) VALUES(?,?,?)",
                           (username, salt, _hash(password, salt)))
        conn.commit()
    except sqlite3.IntegrityError:
        raise ValueError("Username already taken.")
    log.info("registered user %s", username)
    return cur.lastrowid


def login(conn, username, password):
    row = conn.execute("SELECT * FROM users WHERE username=?", ((username or "").strip(),)).fetchone()
    if row and _hash(password or "", row["salt"]) == row["password_hash"]:
        log.info("login ok %s", username)
        return row["id"]
    log.warning("login failed %s", username)
    raise ValueError("Invalid username or password.")
