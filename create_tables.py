from sqlmodel import SQLModel
from database import engine
from models import User, MoodEntry, JournalEntry

SQLModel.metadata.create_all(engine)

print("Tables created successfully!")