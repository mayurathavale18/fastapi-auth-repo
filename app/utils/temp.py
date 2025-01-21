from .database import engine, Base

# Recreate all tables
Base.metadata.create_all(bind=engine)

print("Tables recreated successfully.")
