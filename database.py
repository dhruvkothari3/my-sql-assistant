from sqlalchemy import create_engine, text

# connects to the local SQLite database file
engine = create_engine("sqlite:///chinook.db")

def get_schema() -> str:
    """
    Reads all table names and their columns from the database.
    This gets injected into the LLM prompt so it knows
    what tables and columns exist.
    """
    schema_info = []
    with engine.connect() as conn:
        # get all table names
        tables = conn.execute(text(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )).fetchall()

        for table in tables:
            table_name = table[0]
            # get columns for each table
            columns = conn.execute(text(
                f"PRAGMA table_info({table_name})"
            )).fetchall()
            col_names = [col[1] for col in columns]
            schema_info.append(f"{table_name}: {', '.join(col_names)}")

    return "\n".join(schema_info)

def run_query(query: str) -> list:
    """
    Executes a SQL query and returns results.
    """
    with engine.connect() as conn:
        result = conn.execute(text(query))
        return [dict(row._mapping) for row in result]