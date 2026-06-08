from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///chinook.db")

def get_schema() -> str:
    schema_info = []

    with engine.connect() as conn:
        # step 1: get all table names
        tables = conn.execute(text(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )).fetchall()

        for table in tables:
            table_name = table[0]

            # step 2: get columns + their types
            columns = conn.execute(text(
                f"PRAGMA table_info({table_name})"
            )).fetchall()
            col_info = [f"{col[1]} ({col[2]})" for col in columns]

            # step 3: get foreign keys automatically
            fks = conn.execute(text(
                f"PRAGMA foreign_key_list({table_name})"
            )).fetchall()
            fk_info = []
            for fk in fks:
                fk_info.append(f"{fk[3]} → {fk[2]}.{fk[4]}")

            # step 4: get 2 sample rows so LLM understands real data
            try:
                sample = conn.execute(text(
                    f"SELECT * FROM {table_name} LIMIT 2"
                )).fetchall()
                sample_rows = [str(dict(row._mapping)) for row in sample]
            except:
                sample_rows = []

            # step 5: build the schema string for this table
            line = f"\nTable: {table_name}"
            line += f"\nColumns: {', '.join(col_info)}"
            if fk_info:
                line += f"\nForeign Keys: {', '.join(fk_info)}"
            if sample_rows:
                line += f"\nSample rows: {'; '.join(sample_rows)}"
            line += "\n"

            schema_info.append(line)

    return "\n".join(schema_info)


def run_query(query: str) -> list:
    with engine.connect() as conn:
        result = conn.execute(text(query))
        return [dict(row._mapping) for row in result]
    

def get_join_hints() -> str:
    """
    Automatically generates JOIN syntax for every 
    foreign key relationship in the database.
    No hardcoding — reads directly from the database.
    """
    join_hints = []

    with engine.connect() as conn:
        tables = conn.execute(text(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )).fetchall()

        for table in tables:
            table_name = table[0]
            fks = conn.execute(text(
                f"PRAGMA foreign_key_list({table_name})"
            )).fetchall()

            for fk in fks:
                from_table = table_name
                from_col = fk[3]
                to_table = fk[2]
                to_col = fk[4]

                hint = (
                    f"{from_table} JOIN {to_table} "
                    f"ON {from_table}.{from_col} = {to_table}.{to_col}"
                )
                join_hints.append(hint)

    return "\n".join(join_hints)

def is_safe_query(sql: str) -> tuple[bool, str]:
    """
    Checks if a SQL query is safe to run.
    Returns (True, "") if safe.
    Returns (False, reason) if dangerous.
    """
    # convert to uppercase for checking
    sql_upper = sql.upper().strip()
    
    # block dangerous keywords
    dangerous = ["DROP", "DELETE", "UPDATE", "INSERT", 
                 "ALTER", "TRUNCATE", "CREATE", "REPLACE"]

    for word in dangerous:
        # check as whole word not substring
        if f" {word} " in f" {sql_upper} ":
            return False, f"Query contains forbidden keyword: {word}"
    if ";" in sql:
        return False, "Query contains semicolon - possible injection attack"

    # must start with SELECT
    if not sql_upper.startswith("SELECT"):
        return False, "Only SELECT queries are allowed"

    return True, ""

    

def clean_sql(sql: str) -> str:
    """
    Basic cleaning to prevent SQL injection.
    This is a simple example and can be expanded.
    """
    sql = sql.replace("```sql", "").replace("```", "")
    sql = sql.strip()
    if sql.lower().startswith("sql"):
        sql = sql[3:].strip()
    return sql