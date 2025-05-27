from config.config import db_connection

conn = db_connection()
cursor = conn.cursor()

cursor.execute(""" 
        SELECT
               *
        FROM 
               "tbUserRole"
""")

result = cursor.fetchall()
print(result[0][1])   