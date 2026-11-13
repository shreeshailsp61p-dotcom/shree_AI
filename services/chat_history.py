
import sqlite3
from pathlib import Path
from datetime import datetime


# ==========================================
# DATABASE CONFIGURATION
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATABASE_FOLDER = PROJECT_ROOT / "database"

DATABASE_FOLDER.mkdir(exist_ok=True)

DATABASE_PATH = DATABASE_FOLDER / "chat_history.db"


# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_connection():

    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    return connection


# ==========================================
# INITIALIZE DATABASE
# ==========================================

def initialize_database():

    with get_connection() as connection:

        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (conversation_id)
                    REFERENCES conversations(id)
                    ON DELETE CASCADE
            )
        """)

        connection.commit()


# ==========================================
# CREATE NEW CONVERSATION
# ==========================================

def create_conversation(title="New Chat"):

    current_time = datetime.now().isoformat(timespec="seconds")

    with get_connection() as connection:

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO conversations
            (title, created_at, updated_at)
            VALUES (?, ?, ?)
            """,
            (title, current_time, current_time)
        )

        conversation_id = cursor.lastrowid

        connection.commit()

        return conversation_id


# ==========================================
# SAVE MESSAGE
# ==========================================

def save_message(conversation_id, role, content):

    current_time = datetime.now().isoformat(timespec="seconds")

    with get_connection() as connection:

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO messages
            (conversation_id, role, content, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (conversation_id, role, content, current_time)
        )

        cursor.execute(
            """
            UPDATE conversations
            SET updated_at = ?
            WHERE id = ?
            """,
            (current_time, conversation_id)
        )

        connection.commit()


# ==========================================
# GET CONVERSATIONS
# ==========================================

def get_all_conversations():

    with get_connection() as connection:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM conversations
            ORDER BY updated_at DESC
        """)

        return [dict(row) for row in cursor.fetchall()]


# ==========================================
# GET CONVERSATION MESSAGES
# ==========================================

def get_messages(conversation_id):

    with get_connection() as connection:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT role, content, created_at
            FROM messages
            WHERE conversation_id = ?
            ORDER BY id ASC
            """,
            (conversation_id,)
        )

        return [dict(row) for row in cursor.fetchall()]


# ==========================================
# RENAME CONVERSATION
# ==========================================

def rename_conversation(conversation_id, new_title):

    current_time = datetime.now().isoformat(timespec="seconds")

    with get_connection() as connection:

        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE conversations
            SET title = ?, updated_at = ?
            WHERE id = ?
            """,
            (new_title, current_time, conversation_id)
        )

        connection.commit()


# ==========================================
# DELETE CONVERSATION
# ==========================================

def delete_conversation(conversation_id):

    with get_connection() as connection:

        cursor = connection.cursor()

        cursor.execute("PRAGMA foreign_keys = ON")

        cursor.execute(
            "DELETE FROM conversations WHERE id = ?",
            (conversation_id,)
        )

        connection.commit()
