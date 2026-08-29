from app.database import get_db_connection

try:
    connection = get_db_connection()

    print("Database connected successfully!")

    connection.close()

except Exception as error:
    print("Database connection failed:")
    print(error)