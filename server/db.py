import psycopg2

def get_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="ai_notes",
        user="postgres",
        password="12345678"
    )
    return conn