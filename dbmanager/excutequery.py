from config.config import db_connection

def execute_query(query, params=(), fetchone=False, fetchall=False, commit=False):
    conn = None
    try:
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = None
        if fetchone:
            result = cursor.fetchone()
        elif fetchall:
            result = cursor.fetchall()
        if commit:
            conn.commit()
        return result
    except Exception as e:
        raise e
    finally:
        if conn:
            conn.close()
