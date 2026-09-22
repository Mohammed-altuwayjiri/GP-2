from pathlib import Path
import sqlite3

# Project paths
base_dir = Path(__file__).parent
db_dir = base_dir / "database"
db_path = db_dir / "opinion_ai.db"
schema_path = base_dir / "schema.sql"

# Ensure database folder exists
db_dir.mkdir(exist_ok=True)

# Create database from schema file
conn = sqlite3.connect(db_path)

with open(schema_path, "r", encoding="utf-8") as f:
    schema_sql = f.read()

conn.executescript(schema_sql)
conn.close()

print(f"Database created successfully at: {db_path}")