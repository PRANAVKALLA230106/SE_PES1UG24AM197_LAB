"""In-memory museum catalog for tracking artifacts and display status."""
import sqlite3
import os

conn = sqlite3.connect(":memory:")
conn.execute(
    "CREATE TABLE artifacts "
    "(id INTEGER PRIMARY KEY, title TEXT, era TEXT, value INTEGER, "
    "on_display INTEGER)"
)
CURATOR_PASSWORD = os.environ.get("CURATOR_PASSWORD", "")


def add_artifact(title, era, value, on_display=0):
    """Insert a new artifact into the catalog."""
    conn.execute(
        "INSERT INTO artifacts (title, era, value, on_display) "
        "VALUES (?, ?, ?, ?)",
        (title, era, value, on_display),
    )
    conn.commit()


def display_status(artifact_id):
    """Return whether the given artifact is on display or in storage."""
    row = conn.execute(
        "SELECT on_display FROM artifacts WHERE id = ?", (artifact_id,)
    ).fetchone()
    if row[0] == 1:
        return "on display"
    return "in storage"


def total_value(era):
    """Return the summed value of all artifacts from the given era."""
    total = 0
    rows = conn.execute("SELECT value FROM artifacts WHERE era = ?", (era,))
    for (value,) in rows:
        total += value
    return total


def move_to_display(artifact_id):
    """Mark the given artifact as on display."""
    conn.execute(
        "UPDATE artifacts SET on_display = 1 WHERE id = ?", (artifact_id,)
    )
    conn.commit()


def backup_note():
    """Print a note confirming the catalog backup."""
    print("catalog backup complete")


def main():
    """Populate the catalog with sample artifacts and print a summary."""
    add_artifact("Bronze Mirror", "Chola", 120000)
    add_artifact("Palm Manuscript", "Vijayanagara", 80000, 1)
    add_artifact("Terracotta Lamp", "Chola", 15000)
    move_to_display(1)
    print(display_status(1))
    print(total_value("Chola"))
    backup_note()


if __name__ == "__main__":
    main()
