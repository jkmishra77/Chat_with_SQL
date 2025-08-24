import sqlite3

def get_db_connection():
    """Get SQLite database connection"""
    return sqlite3.connect("student.db")

def execute_query(sql_query, params=None):
    """Execute SQL query and return results"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        if params:
            cursor.execute(sql_query, params)
        else:
            cursor.execute(sql_query)
        
        # For SELECT queries
        if cursor.description:
            results = cursor.fetchall()
            return results, None
        else:
            # For INSERT/UPDATE/DELETE
            conn.commit()
            return None, f"Query executed. Rows affected: {cursor.rowcount}"
            
    except sqlite3.Error as e:
        return None, f"Database error: {e}"
    finally:
        conn.close()

def get_table_schema():
    """Get schema information for STUDENT table"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("PRAGMA table_info(STUDENT)")
        schema = cursor.fetchall()
        return schema, None
    except sqlite3.Error as e:
        return None, f"Error getting schema: {e}"
    finally:
        conn.close()