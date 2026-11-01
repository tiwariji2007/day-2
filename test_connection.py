from database import engine
from sqlalchemy import text

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Connection successful!")
        print("Database returned:", result.scalar())

except Exception as error:
    print("Connection failed!")
    print("Error:", error)