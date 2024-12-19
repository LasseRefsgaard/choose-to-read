import sqlite3

DATABASE_FILE_PATH = "database.db"


def create_connection():
    """create a database connection to the SQLite database"""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_FILE_PATH)
    except sqlite3.Error as e:
        print(e)
    return conn


# Chat history


def insert_chat_history(user_id, story_id, role, text):
    """
    Insert chat history into the database.
    """
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO chat_history (story_id, user_id, role, text) "
            "VALUES (?, ?, ?, ?)",
            (story_id, user_id, role, text),
        )
        conn.commit()


def get_chat_history(user_id, story_id):
    """
    Get chat history from the database.
    """
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM chat_history WHERE user_id=? AND story_id=?",
            (user_id, story_id),
        )
        return cur.fetchall()


def get_formatted_chat_history(user_id, story_id):
    """
    Get formatted chat history from the database. Ready to feed the model
    """
    chat_history_db = get_chat_history(user_id, story_id)
    formatted_history = []
    for row in chat_history_db:
        # Extract role and text from the database row
        role = row[3]  # role is at index 3
        text = row[4]  # text is at index 4
        formatted_history.append({"role": role, "parts": [{"text": text}]})
    return formatted_history


def get_new_story_id(user_id):
    """
    Get a new story id.
    """
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT MAX(story_id) FROM chat_history WHERE user_id=?", (user_id,)
        )
        return cur.fetchone()[0] + 1
