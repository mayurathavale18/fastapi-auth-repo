from app.utils.database import engine
from app.models.user import User, UserHoldings

# Create all tables in the database
def create_database():
    User.metadata.create_all(bind=engine)
    UserHoldings.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_database()
